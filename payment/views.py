from django.http import HttpResponse
from django.shortcuts import render
from ussdapi.models import Donation


# Create your views here.


def payment(request, payid):
    result=Donation.objects.filter(unique_url_code=payid)
    if result.count() > 0:
        fresult=result.first()
        context={
            'data':fresult
        }
        return render(request,'payment/payment.html',context)
    return HttpResponse('Payment Page '+payid)


def notfound(request):
    return render(request,'payment/not-found.html',{})
