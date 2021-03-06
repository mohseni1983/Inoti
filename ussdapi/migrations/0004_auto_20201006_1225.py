# Generated by Django 3.1.2 on 2020-10-06 08:55

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ussdapi', '0003_auto_20201006_1214'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ussd_command',
            options={'verbose_name': 'لیست دستورات', 'verbose_name_plural': 'لیست دستورات'},
        ),
        migrations.AlterModelOptions(
            name='ussd_command_type',
            options={'verbose_name': 'انواع منوی دستورات', 'verbose_name_plural': 'انواع منوی دستورات'},
        ),
        migrations.AddField(
            model_name='ussd_command',
            name='command',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='دستور'),
        ),
        migrations.AlterField(
            model_name='ussd_call',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 6, 12, 25, 48, 895533), verbose_name='ژمان ارسال'),
        ),
        migrations.AlterField(
            model_name='ussd_command',
            name='command_id',
            field=models.IntegerField(blank=True, null=True, verbose_name='ردیف دستور'),
        ),
        migrations.AlterField(
            model_name='ussd_command',
            name='message',
            field=models.TextField(blank=True, null=True, verbose_name='متن پیام'),
        ),
        migrations.AlterField(
            model_name='ussd_command',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ussdapi.ussd_command', verbose_name='کد مادر'),
        ),
    ]
