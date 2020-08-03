import datetime
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
from .models import ReadNum, ReadDetail

def read_statistics_once_read(request, obj): # 每次客户端点击在自定义条件下增添某个阅读计数
    ct = ContentType.objects.get_for_model(obj) # 传入一个对象
    key = "%s_%s_read" % (ct.model, obj.pk)
    if not request.COOKIES.get(key):
        # 具体某个博客总阅读数+1 （同个功能两种方法之一）
        readnum, created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
        readnum.read_num += 1 # 计数加1
        readnum.save() # 保存

        # 当天总阅读数+1 （同个功能两种方法之一）
        date = timezone.now().date()
        if ReadDetail.objects.filter(content_type=ct, object_id=obj.pk, date=date).count():
            readDetail = ReadDetail.objects.get(content_type=ct, object_id=obj.pk, date=date)
        else:
            readDetail = ReadDetail(content_type=ct, object_id=obj.pk, date=date)
        readDetail.read_num += 1
        readDetail.save()
    return key

def get_seven_days_read_data(content_type): # 获取七天前的日点击量
    date = timezone.now().date()
    dates = []
    read_nums = []
    for i in range(7, 0, -1):
        date = date - datetime.timedelta(days=1)
        dates.append(date.strftime('%m/%d'))
        read_details = ReadDetail.objects.filter(content_type=content_type, date=date)
        result = read_details.aggregate(read_num_sum=Sum('read_num')) # 一种用于聚合的方法
        read_nums.append(result['read_num_sum'] or 0)
        
    return dates, read_nums

def get_today_hot_data(content_type):
    today = timezone.now().date()
    read_details = ReadDetail.objects.filter(content_type=content_type, date=today).order_by('-read_num')
    return read_details[:7] # limit

def get_yesterday_hot_data(content_type):
    yesterday = timezone.now().date() - datetime.timedelta(days=1)
    read_details = ReadDetail.objects.filter(content_type=content_type, date=yesterday).order_by('-read_num')
    return read_details[:7]

