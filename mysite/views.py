import datetime
from django.shortcuts import render_to_response, redirect, render
from django.contrib.contenttypes.models import ContentType
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.cache import cache
from django.utils import timezone
from django.db.models import Sum
from django.urls import reverse
from django.http import JsonResponse
from read_statistics.utils import get_seven_days_read_data, get_today_hot_data, get_yesterday_hot_data
from blog.models import Blog
from .forms import LoginForm, RegForm

# 获取七天热门博客
def get_seven_days_hot_blogs():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    blogs = Blog.objects \
                .filter(read_details__date__lt=today, read_details__date__gte=date) \
                .values('id', 'title') \
                .annotate(read_num_sum=Sum('read_details__read_num')) \
                .order_by('-read_num_sum') # 不加values表示按照id聚合
    return blogs[:7]

def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_days_read_data(blog_content_type) # 获取日期及对应的博客文章点击量

    # 获取7天热门博客的缓存数据
    hot_blogs_for_7_days = cache.get('get_seven_days_hot_blogs')
    if hot_blogs_for_7_days is None:
        hot_blogs_for_7_days = get_seven_days_hot_blogs()
        cache.set('get_seven_days_hot_blogs', hot_blogs_for_7_days, 60*60)
        print('create cache')
    else:
        print('use cache')
    context = {}
    context['dates'] = dates
    context['read_nums'] = read_nums
    context['today_hot_data'] = get_today_hot_data(blog_content_type)
    context['yesterday_hot_data'] = get_yesterday_hot_data(blog_content_type)
    context['get_seven_days_hot_blogs'] = get_seven_days_hot_blogs()
    return render_to_response('home.html', context)

# 登录之后返回之前页面
def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid(): # 引用LoginForm时会自动验证用户是否正确,验证函数在LoginForm类下的方法里
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            print(request.get_full_path)
            return redirect(request.GET.get('from',reverse('home')))

    else:
        login_form = LoginForm()

    context = {}
    context['login_form'] = login_form
    return render(request, 'login.html', context)
def login_form_modal(request):
    login_form = LoginForm(request.POST)
    data = {}
    if login_form.is_valid(): # 引用LoginForm时会自动验证用户是否正确,验证函数在LoginForm类下的方法里
        user = login_form.cleaned_data['user']
        auth.login(request, user)
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)
# 注册之后返回之前页面
def register(request):
    if request.method == 'POST':
        reg_form = RegForm(request.POST) 
        if reg_form.is_valid(): # 引用RegForm时会自动验证用户是否正确,验证函数在RegForm类下的方法里
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            # 创建用户
            user = User.objects.create_user(username, email, password)
            user.save()
            # 登录用户
            user = auth.authenticate(username=username, password=password) # 用户认证的一种方法
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        reg_form = RegForm()

    context = {}
    context['reg_form'] = reg_form
    return render(request, 'register.html', context)