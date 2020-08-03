from django.shortcuts import render_to_response, get_object_or_404, render
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType
from mysite.forms import LoginForm
from .models import Blog, BlogType
from read_statistics.utils import read_statistics_once_read
#from datetime import datetime
# 设置一个公共函数
def get_blog_list_common_data(request, blogs_all_list):
    paginator = Paginator(blogs_all_list, settings.EACH_PAGE_BLOGS_NUMBER) # paging per 5
    page_num = request.GET.get('page', 1) # acquire url args of page (GET request)
    page_of_blogs = paginator.get_page(page_num)
    current_page_num = page_of_blogs.number # acquire current page number
    page_range = [current_page_num-3+i for i in range(1,6) \
                    if current_page_num-3+i > 0 and current_page_num-3+i < paginator.num_pages+1] 
    # add tag shows elipsis
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # add head and end page number
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)
    context = {}

    # 获取博客分类的对应博客数量
    '''blog_types = BlogType.objects.all()
                blog_type_list = []
                for blog_type in blog_types:
                    blog_type.blog_count = Blog.objects.filter(blog_type=blog_type).count()
                    blog_type_list.append(blog_type)
    '''
    # 获取日期归档对应的博客数量
    blog_dates = Blog.objects.dates('created_time', 'month', order='DESC')
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year=blog_date.year,\
            created_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count


    context['page_of_blogs'] = page_of_blogs
    context['page_range'] = page_range
    # annotate 获取查询字段
    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog')) # 这句话的效果与上面注释程序一样
    context['blog_dates'] = blog_dates_dict #按年月获取时间列表
    return context

def blog_list(request):
    blogs_all_list = Blog.objects.all()
    context = get_blog_list_common_data(request, blogs_all_list)
    return render_to_response('blog/blog_list.html', context)

def blogs_with_type(request, blog_type_pk):
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)
    context = get_blog_list_common_data(request, blogs_all_list)
    context['blog_type'] = blog_type
    return render_to_response('blog/blogs_with_type.html', context)

def blogs_with_date(request, year, month):
    blogs_all_list = Blog.objects.filter(created_time__year=year, created_time__month=month)
    context = get_blog_list_common_data(request, blogs_all_list)
    context['blogs_with_date'] = '%s年%s月' %(year, month)
    return render_to_response('blog/blogs_with_date.html', context)

def blog_detail(request, blog_pk):
    blog = get_object_or_404(Blog, pk=blog_pk)
    read_cookie_key = read_statistics_once_read(request, blog)
    context = {}
    # 获取当前博客上一条博客和下一条博客
    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()
    context['blog'] = blog
    context['login_form'] = LoginForm()
    # 下面部分放到tags去实现
    #comments = Comment.objects.filter(content_type=blog_content_type, object_id=blog.pk, parent=None)
    #blog_content_type = ContentType.objects.get_for_model(blog) # 获得模块Blog
    #context['comments'] = comments.order_by('-comment_time')
    #context['comment_form'] = CommentForm(initial={'content_type':blog_content_type.model,'object_id':blog_pk, 'reply_comment_id':'0'})
    response =  render(request, 'blog/blog_detail.html', context) # 响应
    # 给客户端添加cookie,可做一些判断操作
    response.set_cookie(read_cookie_key, 'ture') # , max_age=60, expires=datetime) 这两个参数设置有效期，任一设置一个即可

    return response