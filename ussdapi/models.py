from datetime import datetime

from django.contrib import admin
from django.db import models


# Create your models here.

class ussd_call(models.Model):
    call = models.CharField(max_length=80, verbose_name='کد ارسالی')
    mobile = models.CharField(max_length=15, verbose_name='شماره همراه')
    session_id = models.CharField(max_length=50, verbose_name='شناسه نشست')
    date_time = models.DateTimeField(default=datetime.now(), verbose_name='ژمان ارسال')

    class Meta:
        verbose_name = 'کدهای دریافتی USSD'
        verbose_name_plural = 'کدهای دریافتی USSD'

    def __str__(self):
        return ('{}  -  {}  -  {}  -  {}'.format(self.session_id, self.mobile, self.call, self.date_time))


class ussd_command(models.Model):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     if self.parent.command is not None:
    #         parent_command = self.parent.command
    #         self.command=parent_command+'*'+str(self.command_id)

    parent = models.ForeignKey('ussd_command', on_delete=models.CASCADE, verbose_name='کد مادر', null=True, blank=True)

    command = models.CharField(max_length=100, verbose_name='دستور', null=True, blank=True)
    title = models.CharField(max_length=40, verbose_name='عنوان')
    command_id = models.IntegerField(verbose_name='ردیف دستور', null=True, blank=True)
    message = models.TextField(verbose_name='متن پیام', null=True, blank=True)
    type=(
        (1,'منو'),
        (2,'حمایت'),
        (3,'کمپین'),
        (4,'اطلاعات'),
        (5,'پیامک')
    )
    command_type = models.IntegerField(choices=type,default=1,verbose_name='نوع منو')


    # def get_ussd_command(self):
    #     parent_command=self.parent.command
    #     return parent_command+'*'+str(self.command_id)

    def __str__(self):
        return (self.title)

    class Meta:
        verbose_name = 'لیست دستورات'
        verbose_name_plural = 'لیست دستورات'

# ussd_command Admin class
class ussd_command_admin(admin.ModelAdmin):
    list_display = ('parent','title','command_id','command','command_type')
    search_fields = ['title']
    ordering = ['parent','id']
    list_filter = ['parent','command_type']



class ussd_command_type(models.Model):
    title = models.CharField(max_length=30, verbose_name='نوع دستور')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'انواع منوی دستورات'
        verbose_name_plural = 'انواع منوی دستورات'
