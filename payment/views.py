from datetime import datetime

from django.middleware.csrf import get_token
import requests
from django.http import HttpResponse
from django.shortcuts import render
from ussdapi.models import Donation
from .sep import PaymentGatewayAdapter
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect,csrf_exempt
import jdatetime

# Create your views here.

merchant = '11783880'


def payment(request, payid):
    result=Donation.objects.filter(unique_url_code=payid)
    #print('URL = '+request.get_raw_uri)
    redirect_url=request.build_absolute_uri(reverse(viewname='verify'))

    if result.count() > 0:
        fresult=result.first()
        context={
            'data':fresult
        }
        if fresult.payment_status:
            return render(request,'payment/already-payed.html',{'date': fresult.payment_date.date().strftime('%Y/%m/%d') })
        if request.POST:
            amount=request.POST['amount']
            mobile=request.POST['mobile']
            resnum=fresult.id
            gateway=PaymentGatewayAdapter()
            token_resnum=gateway.sep_request_token(resNum=resnum,mid=merchant,amount=fresult.amount,redirectUrl=redirect_url)
            print(token_resnum[0])
            print(token_resnum[1])

            cntx={
                'token': token_resnum[0],
                'resnum':token_resnum[1],
                'amount': fresult.amount
            }
            return render(request,'payment/gotogateway.html',cntx)
            #r=result.json()
            #print(r['token'])


        return render(request,'payment/payment.html',context)
    return HttpResponse('Payment Page '+payid)
@csrf_exempt
def verify(request):
    pay = Donation.objects.get(pk=int(request.POST['ResNum']))

    if request.POST['StateCode']=='-1':
        payId=pay.unique_url_code
        context={
            'data':'شما از پرداخت منصرف شده اید',
            'url' : request.get_raw_uri().replace('/verify/','/{}'.format(payId))
        }
        return render(request,'payment/cancel.html',context)

    ref=request.POST['RefNum']
    gateway=PaymentGatewayAdapter()
    res=gateway.sep_verify_transaction(ref_num=ref,MID=merchant)
    if int(res)<0:
        payId=pay.unique_url_code
        context={
            'data':'خطایی در پرداخت اتفاق افتاده است',
            'url' : request.get_raw_uri().replace('/verify/','/{}'.format(payId))
        }
        return render(request,'payment/cancel.html',context)
    pay.digital_id=request.POST['RefNum']
    pay.card_no=request.POST['SecurePan']
    pay.payment_date=datetime.now()
    pay.payment_gateway='سامان'
    pay.transaction_id=request.POST['TRACENO']
    pay.payment_status=True
    pay.save()
    context={
        'amount':int(res),
        'transaction_id': request.POST['TRACENO'],
        'digital_id' : request.POST['RefNum'],
        'date': jdatetime.date.fromgregorian(date=datetime.now())
    }
    return render(request,'payment/success.html',context)





def notfound(request):
    return render(request,'payment/not-found.html',{})
