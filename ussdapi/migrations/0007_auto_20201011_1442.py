# Generated by Django 3.1.2 on 2020-10-11 11:12

import datetime
from django.db import migrations, models
import ussdapi.models


class Migration(migrations.Migration):

    dependencies = [
        ('ussdapi', '0006_auto_20201006_1440'),
    ]

    operations = [
        migrations.AddField(
            model_name='ussd_call',
            name='command_type',
            field=models.IntegerField(choices=[(0, 'هیچکدام'), (1, 'منو'), (2, 'کمپین'), (3, 'حمایت'), (4, 'اطلاعات')], default=ussdapi.models.CommandType['هیچکدام'], verbose_name='نوع منو'),
        ),
        migrations.AlterField(
            model_name='ussd_call',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 11, 14, 42, 38, 708282), verbose_name='ژمان ارسال'),
        ),
        migrations.AlterField(
            model_name='ussd_command',
            name='command_type',
            field=models.IntegerField(choices=[(0, 'هیچکدام'), (1, 'منو'), (2, 'کمپین'), (3, 'حمایت'), (4, 'اطلاعات')], default=ussdapi.models.CommandType['هیچکدام'], verbose_name='نوع منو'),
        ),
    ]