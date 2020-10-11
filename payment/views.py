from django.http import HttpResponse
from django.shortcuts import render
from ussdapi.models import Donation


# Create your views here.


def payment(request, payid):
    result=Donation.objects.filter(unique_url_code=payid)
    if result.count() > 0:
        fresult=result.first()
        return HttpResponse(fresult.amount)
    return HttpResponse('Payment Page '+payid)


def notfound(request):
    return HttpResponse('Not Found')
