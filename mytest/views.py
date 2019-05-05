from django.contrib.auth.decorators import login_required
from django.shortcuts import render,HttpResponse
from datetime import datetime
from django.views.decorators.cache import cache_page
from django.core.cache import cache
import qrcode
from django.utils.six import BytesIO
from mytest.models import *

from django.conf import settings
# Create your views here.

def redis_data(request):
    return render(request, 'redis_data.html')

def write_to_redis(request):
    key = request.GET.get('key')
    value = request.GET.get('value')
    cache.set(key,value,10)
    return render(request,'redis_data.html')

def read_from_redis(request):
    key = request.GET.get('key')
    value = cache.get(key)
    return HttpResponse(value)



@cache_page(10)
def redis_(request):
    real_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render(request, 'redis_test.html', {'real_time':real_time})


def verify_(request):
    return render(request,'verfy.html')


def qr_code(request):
    img = qrcode.make('123&3456&我是谁&63acx*!@')
    buf = BytesIO()
    img.save(buf)
    return HttpResponse(buf.getvalue())


@login_required
def upload(request):
    return render(request, 'upload.html')


@login_required
def upload_(request):
    if request.method == 'POST':
        file = File()
        file.user = request.user
        file.file = request.FILES.get('image')
        file.upload_time = datetime.now()
        file.save()
        return HttpResponse('上传成功')

def query_file(request):
    if request.is_ajax():
        user = request.user
        files = File.objects.filter(user=user)
        return render(request,'file_table.html',locals())
