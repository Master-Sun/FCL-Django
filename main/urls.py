from django.conf.urls import url
from main import views

urlpatterns = [
    url(r'^register/$',views.register),
    url(r'^register_/$',views.register_),
    url(r'^login/$',views.login_in),
    url(r'^login_/$',views.login_),
    url(r'^$',views.index),
    url(r'^logout/$',views.logout_),
    url(r'^match/$',views.match),
    url(r'^query/$',views.query_,name='query'),
    url(r'^qrcode_/$',views.qrcode_),
    url(r'^download/$',views.download_),

]