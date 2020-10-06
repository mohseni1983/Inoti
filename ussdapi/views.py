from datetime import datetime

from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.views.decorators.http import require_http_methods, require_GET
from .models import ussd_call,ussd_command


# Create your views here.


def USSDApi(request):
    mobile = request.GET.get('mobile', default=None)
    call = request.GET.get('call', default=None)
    sessionId = request.GET.get('sessionid', default=None)
    print(mobile)
    print(call)
    print(sessionId)
    result = ussd_call.objects.filter(session_id=sessionId)
    if result.count() == 0:
        res = ussd_call(call=call, session_id=sessionId, mobile=mobile, date_time=datetime.now())
        res.save()
    else:
        result = result.first()
        result.call = call
        result.save()
    ussd_result=ussd_command.objects.filter(command=call)
    if ussd_result.count()==0:
        return HttpResponse('خطا در وارد کردن دستور')
    else:
        result=ussd_result.first()
        print(result)
        message=getattr(result,'title') + '<br/>'
        sub=result.ussd_command_set.all()
        if sub.count() !=0:
            for item in sub:
                message=message+str(getattr(item,'command_id'))+'-'+getattr(item,'title')+'<br/>'

    return HttpResponse(message)
