# Generated by Django 3.1.2 on 2020-10-06 11:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ussdapi', '0005_auto_20201006_1230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ussd_call',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 6, 14, 40, 24, 981317), verbose_name='ژمان ارسال'),
        ),
        migrations.RemoveField(
            model_name='ussd_command',
            name='command_type',
        ),
        migrations.AddField(
            model_name='ussd_command',
            name='command_type',
            field=models.IntegerField(choices=[(1, 'منو'), (2, 'حمایت'), (3, 'کمپین'), (4, 'اطلاعات'), (5, 'پیامک')], default=1),
        ),
    ]
