# Generated by Django 3.1.2 on 2020-10-14 08:49

import datetime
from django.db import migrations, models
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('ussdapi', '0015_auto_20201014_1201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='creation_date',
            field=django_jalali.db.models.jDateTimeField(default=datetime.datetime(2020, 10, 14, 12, 19, 16, 424276), verbose_name='تاریخ ایجاد'),
        ),
        migrations.AlterField(
            model_name='donation',
            name='digital_id',
            field=models.CharField(blank=True, max_length=500, null=True, unique=True, verbose_name='رسید دیجیتالی'),
        ),
        migrations.AlterField(
            model_name='donation',
            name='unique_url_code',
            field=models.CharField(default='612A2C', max_length=6, unique=True, verbose_name='شناسه یکتای اینترنتی'),
        ),
        migrations.AlterField(
            model_name='ussd_call',
            name='date_time',
            field=django_jalali.db.models.jDateTimeField(default=datetime.datetime(2020, 10, 14, 12, 19, 16, 423279), verbose_name='ژمان ارسال'),
        ),
    ]
