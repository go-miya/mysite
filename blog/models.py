from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from ckeditor_uploader.fields import RichTextUploadingField
from read_statistics.models import ReadNumExpandMethod, ReadDetail
# Create your models here.


class BlogType(models.Model):
    type_name = models.CharField(max_length=20)
    
    def __str__(self):
        return self.type_name

class Blog(models.Model, ReadNumExpandMethod):
    title = models.CharField(max_length=50)
    blog_type = models.ForeignKey(BlogType, on_delete=models.CASCADE)
    content = RichTextUploadingField() # 添加富文本,附带可上传图片功能
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    read_details = GenericRelation(ReadDetail) # Blog.objects.first().read_details.all() 可取到对应的ReadDetaild
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)
         
    def __str__(self):
        return "<Blog: %s>" % self.title
    class Meta:
        ordering = ['-created_time']


# 记录访问量的模型（方法一）
'''class ReadNum(models.Model):
    read_num = models.IntegerField(default=0) # 添加阅读数量字段，以显示每条博客的阅读数量
    blog = models.OneToOneField(Blog, on_delete=models.CASCADE)
'''

