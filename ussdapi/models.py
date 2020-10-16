from datetime import datetime
from enum import IntEnum
import uuid
from django.db import models
from django_jalali.db import models as jmodel
from django.contrib import admin
from django.db import models


# Data model for Campaigns
from jalali_date import datetime2jalali
from jalali_date.admin import TabularInlineJalaliMixin, StackedInlineJalaliMixin, ModelAdminJalaliMixin


class Campaign(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان کمپین')
    short_title = models.CharField(max_length=30, verbose_name='عنوان کوتاه')
    min_donation_amount = models.IntegerField(verbose_name='حداقل مبلغ هر حمایت', default=100000)

    class Meta:
        verbose_name_plural = 'کمپین ها'
        verbose_name = 'کمپین ها'

    def __str__(self):
        return self.title


# Campaing Admin class
class Campaign_admin(admin.ModelAdmin):
    list_display = ['title']
    list_filter = ['title']


# Enum for USSD command types
class CommandType(IntEnum):
    هیچکدام = 0
    منو = 1
    کمپین = 2
    حمایت = 3
    اطلاعات = 4

    @classmethod
    def choice(cls):
        return [(key.value, key.name) for key in cls]


# Data model for history of USSD calls
class ussd_call(models.Model):
    call = models.CharField(max_length=80, verbose_name='کد ارسالی')
    mobile = models.CharField(max_length=15, verbose_name='شماره همراه')
    session_id = models.CharField(max_length=50, verbose_name='شناسه نشست')
    date_time = models.DateTimeField(auto_now_add=True, verbose_name='زمان ارسال')
    command_type = models.IntegerField(choices=CommandType.choice(), default=CommandType.هیچکدام,
                                       verbose_name='نوع منو')

    class Meta:
        verbose_name = 'کدهای دریافتی USSD'
        verbose_name_plural = 'کدهای دریافتی USSD'

    def __str__(self):
        return ('{}  -  {}  -  {}  -  {}'.format(self.session_id, self.mobile, self.call, self.date_time))


class ussd_call_admin(ModelAdminJalaliMixin,admin.ModelAdmin):
    list_display = ['session_id', 'get_jalali_date', 'mobile', 'call', 'command_type']
    search_fields = ['mobile']
    list_filter = ['command_type']
    date_hierarchy = 'date_time'
    def get_jalali_date(self,obj):
        return datetime2jalali(obj.date_time).strftime('%y/%m/%d - %H:%M:%S')
    get_jalali_date.short_description = 'زمان ارسال'
    get_jalali_date.admin_order_field='date_time'


# Data Model for USSD Commands

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
    command_type = models.IntegerField(choices=CommandType.choice(), default=CommandType.هیچکدام,
                                       verbose_name='نوع منو')
    campaign = models.OneToOneField(Campaign, on_delete=models.CASCADE, null=True, blank=True)

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
    list_display = ('parent', 'title', 'command_id', 'command', 'command_type')
    search_fields = ['title']
    ordering = ['parent', 'id']
    list_filter = ['parent', 'command_type']


class ussd_command_type(models.Model):
    title = models.CharField(max_length=30, verbose_name='نوع دستور')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'انواع منوی دستورات'
        verbose_name_plural = 'انواع منوی دستورات'


# Class for USSD Request
class USSDRequest:
    def __init__(self, call, session_id, mobile, command_type=CommandType.هیچکدام):
        self.call = call
        self.session_id = session_id
        self.mobile = mobile
        self.command_type = command_type


# Data model for donations
class Donation(models.Model):
    creation_date = models.DateTimeField(verbose_name='تاریخ ایجاد', auto_now_add=True)
    payment_status = models.BooleanField(verbose_name='وضعیت پرداخت', default=False)
    payment_date = models.DateTimeField(verbose_name='تاریخ پرداخت', null=True, blank=True)
    session_id = models.CharField(max_length=150, verbose_name='شناسه نشست')
    mobile = models.CharField(max_length=20, verbose_name='شماره موبایل')
    campaing = models.ForeignKey(Campaign, on_delete=models.DO_NOTHING, verbose_name='کمپین', null=True, blank=True)
    amount = models.FloatField(verbose_name='مقدار حمایت',null=True,blank=True)
    bill_id = models.CharField(max_length=30, verbose_name='شناسه قبض', null=True, blank=True)
    bill_no = models.CharField(max_length=30, verbose_name='شناسه پرداخت', null=True, blank=True)
    card_no = models.CharField(max_length=20, verbose_name='شماره کارت', blank=True, null=True)
    transaction_id = models.CharField(max_length=50, verbose_name='شناسه تراکنش', blank=True, null=True)
    digital_id=models.CharField(max_length=500,verbose_name='رسید دیجیتالی',blank=True,null=True,unique=True)

    unique_url_code = models.CharField(max_length=6, default=uuid.uuid4().hex[:6].upper(),
                                       verbose_name='شناسه یکتای اینترنتی',unique=True)
    payment_gateway = models.CharField(max_length=30, verbose_name='درگاه پرداخت', null=True, blank=True)

    class Meta:
        verbose_name_plural = 'حمایت های مالی'
        verbose_name = 'حمایت های مالی'


# Admin model for Donations
class donation_admin(admin.ModelAdmin):
    list_display = ['creation_date', 'payment_status', 'payment_date', 'mobile', 'campaing', 'amount', 'transaction_id',
                    'card_no', 'unique_url_code']
    search_fields = ['mobile', 'transaction_id', 'card_no', 'unique_url_code']
    list_filter = ['creation_date', 'payment_status', 'payment_date', 'mobile', 'campaing']

# SMS model
class sms_inbox(models.Model):
    message_id=models.CharField(max_length=20,verbose_name='شناسه پیام')
    sender=models.CharField(max_length=30,verbose_name='شماره درگاه')
    receptor=models.CharField(max_length=15,verbose_name='شماره مخاطب')
    date =models.DateTimeField(verbose_name='تاریخ ارسال')
    message=models.TextField(verbose_name='متن پیام')
    status=models.IntegerField(verbose_name='کد وضعیت')
    status_text=models.CharField(verbose_name='متن وضعیت',max_length=20)
    cost=models.FloatField(verbose_name='هزینه پیامک')

    class Meta:
        verbose_name_plural='لیست پیامک های ارسالی'
        verbose_name='لیست پیامک های ارسالی'
    def __str__(self):
        return '{} --- {}'.format(self.receptor,self.date)

# SMS Admin model
class sms_inbox_admin(admin.ModelAdmin):
    list_display = ['date','receptor','sender','status','status_text']
    search_fields = ['receptor','date']
    list_filter = ['status_text']