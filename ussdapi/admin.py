from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.ussd_call,models.ussd_call_admin)
admin.site.register(models.ussd_command,models.ussd_command_admin)
admin.site.register(models.ussd_command_type)