from django.contrib.auth.hashers import make_password
from django.contrib.sessions.models import Session
from django.shortcuts import render, HttpResponse,redirect
from main.models import *
from django.contrib import auth
import json
import csv, codecs
from datetime import datetime
from django.contrib.auth.decorators import login_required
import qrcode
from django.utils.six import BytesIO
from django.utils import timezone

# Create your views here.

def register(request):
    return render(request,'register.html')

def register_(request):
    if request.method == 'POST':
        new_user = User()
        new_user.username = request.POST.get('username','kong')
        old_user = User.objects.filter(username=new_user.username)
        if len(old_user) > 0:
            return render(request,'register.html',{'message':'用户名已存在'})
        new_user.password = make_password(request.POST.get('password'))
        new_user.name = request.POST.get('name')
        try:
            new_user.save()
        except Exception as e:
            print(e)
            return render(request,'register.html',{'message':'异常'})
        return redirect('/login/')
    else:
        return render(request,'register.html',{'message':'哪来的？'})


def index(request):
    return render(request,'index.html')


def login_in(request):
    resp = render(request,'login.html',{'count':1})
    resp.set_cookie('origin_url',request.META.get('HTTP_REFERER','/'),60*5)
    return resp


def login_(request):
    if request.method == 'POST':
        if int(request.POST.get('count',0)) > 2:
            verify = request.POST.get('verify').lower()
            if verify != request.session['verifycode']:
                return render(request,'login.html',{'message':'验证码错误'})
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username,password=password)
        if user is not None and user.is_active:
            auth.login(request,user)
            #挤掉之前登录的同一个账号
            # 删除非当前用户session_key的记录
            #查出的session，打印出来为session_key，可能是对象,本次登录的用户id并不会存进session中
            for session in Session.objects.filter(expire_date__gte=timezone.now()):
                data = session.get_decoded()
                if data.get('_auth_user_id', None) == str(request.user.id):
                    session.delete()
            return redirect(request.COOKIES['origin_url'])
        else:
            count = int(request.POST.get('count',1)) + 1
            return render(request,'login.html',{'message':'用户名或密码错误','count':count})
    return render(request,'login.html',{'message':'哪来的？','count':1})


def logout_(request):
    auth.logout(request)
    return redirect('/')


# 比对结果记录
def record_(d,request):
    record = Recode()
    record.user = request.user
    record.raw_material1 = d['raw1']
    record.raw_material2 = d['raw2']
    record.order = Order_list.objects.filter(order_no=d['order']).first()
    if d['result'] != '比对成功':
        record.result = False
    record.match_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(record.match_time)
    record.save()

# 比对验证

def match(request):
    if request.is_ajax():
        order_no = request.GET.get('order_no','')
        raw_material1 = request.GET.get('raw_material1','')
        raw_material2 = request.GET.get('raw_material2','')
        d = {'result':'','order':order_no,'raw1':raw_material1,'raw2':raw_material2}
        if order_no and raw_material1 and raw_material2:
            order = Order_list.objects.filter(order_no=order_no)
            if order:
                raw1 = order[0].product.raw_material1
                raw2 = order[0].product.raw_material2
                if raw1 == raw_material1 and raw2 == raw_material2:
                    d['result'] = '比对成功'
                    record_(d,request)
                    d['src'] = '/qrcode_/?text=' + order_no + raw_material1 + raw_material2
                    d = json.dumps(d,request)
                    return HttpResponse(d)
                else:
                    d['result'] = '比对失败，原料错误'
                    record_(d, request)
                    d['raw1'] = raw1
                    d['raw2'] = raw2
                    d = json.dumps(d)
                    return HttpResponse(d)
            else:
                d['result'] = '比对失败，订单号不存在'
                d['order'] = ''
                d = json.dumps(d)
                return HttpResponse(d)
        else:
            d['result'] = '比对失败，有空值'
            record_(d, request)
            d = json.dumps(d)
            return HttpResponse(d)
    if request.method == 'GET':
        return render(request,'match.html')

@login_required
def query_(request):
    if request.is_ajax():
        order_no = request.GET.get('order_no')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        records = Recode.objects.all()
        if order_no:
            order = Order_list.objects.filter(order_no=order_no).first()
            records = Recode.objects.filter(order=order)
        if start_date:
            records = records.filter(match_time__gte=start_date)
        if end_date:
            end_date += ' 23:59:59'
            records = records.filter(match_time__lt=end_date)
        return render(request,'table.html',locals())
    else:
        records = Recode.objects.all()
        return render(request,'query.html',locals())


def qrcode_(request):
    #test为二维码中的内容
    text = request.GET.get('text')
    img = qrcode.make(text)
    # 常见二进制内存对象，存储图片
    buf = BytesIO()
    img.save(buf)
    return HttpResponse(buf.getvalue())

def download_(request):
    records = Recode.objects.all()
    # 申明文档类型
    response = HttpResponse(content_type='text/csv')
    # 添加UTF-8的BOM标记,解决文件中 中文乱码问题
    response.write(codecs.BOM_UTF8)
    # 设置文件名
    response['Content-Disposition'] = 'attachment; filename="%s.csv"'% datetime.now().strftime('%Y%m%d%H%M%S')
    writer = csv.writer(response)
    count = 0
    for record in records:
        if count == 0:
            L = ['序号', '姓名', '订单号', '比对结果', '比对日期']
        else:
            L = [count,record.user.name,record.order.order_no,record.result,record.match_time]
        writer.writerow(L)
        count += 1
    return response