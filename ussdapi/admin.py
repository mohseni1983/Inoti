from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.ussd_call,models.ussd_call_admin)
admin.site.register(models.ussd_command,models.ussd_command_admin)
admin.site.register(models.ussd_command_type)
admin.site.register(models.Campaign,models.Campaign_admin)
admin.site.register(models.Donation,models.donation_admin)
admin.site.register(models.sms_inbox,models.sms_inbox_admin)