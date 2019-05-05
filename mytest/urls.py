from django.conf.urls import url, include
from mytest import views, verify

urlpatterns = [
    url(r'^verify/$', views.verify_),
    url(r'^verifycode/', verify.verifycode),
    url(r'^redis/cache/$',views.redis_),
    url(r'^redis/data/$',views.redis_data),
    url(r'^redis/save/$',views.write_to_redis),
    url(r'^redis/query/$',views.read_from_redis),
    url(r'^qrcode/$',views.qr_code),
    url(r'upload/$',views.upload),
    url(r'upload_/$',views.upload_),
    url(r'^query_file/$',views.query_file),
]