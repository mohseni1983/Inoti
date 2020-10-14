# Generated by Django 3.1.2 on 2020-10-14 08:31

import datetime
from django.db import migrations, models
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('ussdapi', '0014_auto_20201013_1445'),
    ]

    operations = [
        migrations.AddField(
            model_name='donation',
            name='digital_id',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='رسید دیجیتالی'),
        ),
        migrations.AlterField(
            model_name='donation',
            name='creation_date',
            field=django_jalali.db.models.jDateTimeField(default=datetime.datetime(2020, 10, 14, 12, 1, 25, 869499), verbose_name='تاریخ ایجاد'),
        ),
        migrations.AlterField(
            model_name='donation',
            name='transaction_id',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='شناسه تراکنش'),
        ),
        migrations.AlterField(
            model_name='donation',
            name='unique_url_code',
            field=models.CharField(default='7D451A', max_length=6, unique=True, verbose_name='شناسه یکتای اینترنتی'),
        ),
        migrations.AlterField(
            model_name='ussd_call',
            name='date_time',
            field=django_jalali.db.models.jDateTimeField(default=datetime.datetime(2020, 10, 14, 12, 1, 25, 868502), verbose_name='ژمان ارسال'),
        ),
    ]
