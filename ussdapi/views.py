from datetime import datetime

from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.views.decorators.http import require_http_methods, require_GET
from .models import ussd_call, ussd_command, USSDRequest, CommandType


# Create your views here.


def USSDApi(request):
    mobile = request.GET.get('mobile', default=None)
    call = request.GET.get('call', default=None)
    session_Id = request.GET.get('sessionid', default=None)
    USSD_Request = USSDRequest(mobile=mobile, call=call, session_id=session_Id)
    print(mobile)
    print(call)
    print(session_Id)
    update_ussd_commands_history(USSD_Request)

    ussd_result = ussd_command.objects.filter(command=call)
    if ussd_result.count() == 0:
        return HttpResponse('خطا در وارد کردن دستور')
    else:
        result = ussd_result.first()
        print(result)
        message = getattr(result, 'title') + '<br/>'
        cmd_type = getattr(result, 'command_type')
        # print(cmd_type.name)
        # print(cmd_type.value)
        if cmd_type == 1:
            USSD_Request.command_type=CommandType.منو
            update_ussd_commands_history(USSD_Request)
            sub = result.ussd_command_set.all()
            if sub.count() != 0:
                for item in sub:
                    message = message + str(getattr(item, 'command_id')) + '-' + getattr(item, 'title') + '<br/>'
        if cmd_type == 3:
            USSD_Request.command_type=CommandType.حمایت
            update_ussd_commands_history(USSD_Request)

            message = message + 'مبلغ حمایت را وارد کنید'
    return HttpResponse(message)


def update_ussd_commands_history(req):
    result = ussd_call.objects.filter(session_id=req.session_id)
    if result.count() == 0:
        res = ussd_call(call=req.call, session_id=req.session_id, mobile=req.mobile, date_time=datetime.now(),command_type=req.command_type)
        res.save()
    else:
        res = result.first()
        res.call = req.call
        res.command_type=req.command_type
        res.save()
