from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
# Create your models here.

class User(AbstractUser):
    name = models.CharField('姓名',max_length=30,null=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'user'
        verbose_name = '员工信息表'
        verbose_name_plural = verbose_name


class Product(models.Model):
    product_name = models.CharField('品名',max_length=30,null=False)
    raw_material1 = models.CharField('原料1',max_length=30,null=False)
    raw_material2 = models.CharField('原料2',max_length=30,null=False)
    add_date = models.DateField('添加时间',default=False)

    def __str__(self):
        return self.product_name

    class Meta:
        db_table = 'product'
        verbose_name = '产品信息表'
        verbose_name_plural = verbose_name


class Order_list(models.Model):
    order_no = models.CharField('订单号',max_length=50,null=False)
    product = models.ForeignKey(Product,verbose_name='品名',on_delete=models.CASCADE)
    add_date = models.DateField('添加时间',auto_now=True)

    def __str__(self):
        return self.order_no

    class Meta:
        db_table = 'order_list'
        verbose_name = '订单信息'
        verbose_name_plural = verbose_name


class Recode(models.Model):
    user = models.ForeignKey(User,verbose_name='生产员工', on_delete=models.CASCADE)
    match_time = models.DateTimeField('比对时间',default=False)
    order = models.ForeignKey(Order_list,verbose_name='订单', on_delete=models.CASCADE)
    result = models.BooleanField('比对结果',default=True)
    raw_material1 = models.CharField('物料1',max_length=50,default='')
    raw_material2 = models.CharField('物料2',max_length=50,default='')

    def __repr__(self):
        return self.order.order_no

    class Meta:
        db_table = 'recode'
        verbose_name = '比对记录'
        verbose_name_plural = verbose_name