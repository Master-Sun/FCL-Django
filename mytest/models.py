from django.db import models
from main.models import *
from datetime import datetime

# Create your models here.
def file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = datetime.now().strftime('%Y%m%d%H%M%S%f') + '.' + ext
    return 'file/' + filename


class File(models.Model):
    user = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE)
    file = models.ImageField(upload_to=file_name, verbose_name='图片')
    upload_time = models.DateTimeField(verbose_name='上传时间')

    def __str__(self):
        return self.user.name

    class Meta:
        db_table = 'file'
        verbose_name = '上传图片'
        verbose_name_plural = verbose_name