from datetime import datetime
import requests
from kavenegar import *
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.views.decorators.http import require_http_methods, require_GET
from .models import ussd_call, ussd_command, USSDRequest, CommandType, Donation, sms_inbox

# kavenegar API key
kavenegar_api = '46696E71742F7751786C4557447434476B4163775130564A6B2B466D65474F457A74787268414761344E773D'


# Send SMS by kavenegar
def send_sms(reciptant, message):
    try:
        api = KavenegarAPI(kavenegar_api)
        param = {
            'sender': '',  # optional
            'receptor': '{}'.format(reciptant),  # multiple mobile number, split by comma
            'message': '{}'.format(message),

        }
        response = api.sms_send(param)
        print(str(response))

        for jresponse in response:
            save_to_inbox = sms_inbox(receptor=jresponse['receptor'], sender=jresponse['sender'],
                                      message=jresponse['message'],
                                      status=int(jresponse['status']), status_text=jresponse['statustext'],
                                      date=datetime.fromtimestamp(float(jresponse['date'])),
                                      cost=float(jresponse['cost']),message_id=jresponse['messageid'])
            save_to_inbox.save()
        print(str(response))
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)


# Create your views here.
def api(request):
    mobile = request.GET.get('mobile', default=None)
    call = request.GET.get('call', default=None)
    session_id = request.GET.get('sessionid', default=None)
    message = ''
    # Search for command
    result = ussd_command.objects.filter(command=call)
    if result.count() > 0:
        row = result.first()
        message = getattr(row, 'title') + '<br />'
        cmd_type = getattr(row, 'command_type')
        if cmd_type == CommandType.منو.value:
            # update request history
            income_request = USSDRequest(mobile=mobile, session_id=session_id, call=call, command_type=CommandType.منو)
            update_ussd_commands_history(income_request)

            sub_result = row.ussd_command_set.all()
            if sub_result.count() > 0:
                for item in sub_result:
                    message = message + str(getattr(item, 'command_id')) + '-' + getattr(item, 'title') + '<br/>'
        if cmd_type == CommandType.حمایت.value:
            income_request = USSDRequest(mobile=mobile, session_id=session_id, call=call,
                                         command_type=CommandType.حمایت)
            update_ussd_commands_history(income_request)
            message = message + 'مبلغ حمایت را وارد کنید <br> حداقل حمایت 100,000ریال'
        if cmd_type == CommandType.کمپین.value:
            income_request = USSDRequest(mobile=mobile, session_id=session_id, call=call,
                                         command_type=CommandType.کمپین)
            update_ussd_commands_history(income_request)
            message = message + 'مبلغ حمایت را وارد کنید <br> حداقل حمایت 100,000ریال'
    else:
        history_result = ussd_call.objects.filter(session_id=session_id)
        if history_result.count() > 0:
            history_row = history_result.first()
            type = getattr(history_row, 'command_type')
            if type == CommandType.کمپین.value or type == CommandType.حمایت.value:
                last_star = call.rfind('*')
                amount = float(call[last_star + 1:])

                if amount < 100000:
                    message = message + 'مبلغ کمتر از 100000 ریال است دوباره وارد کنید'
                else:
                    shenase = requests.post(url='http://shenase.net/api/bills/create',
                                            json={
                                                "username": "mohseni676",
                                                "password": "ghasem1356",
                                                "billType": 0,
                                                "receiverName": "{}".format(mobile),
                                                "receiverFamily": "{}".format(mobile),
                                                "receiverMobile": "{}".format(mobile),
                                                "title": "قبض کمپین 1",
                                                "price": "{}".format(amount),
                                                "billDescription": "نیکوکاران شریف",
                                                "isWageByCreator": True,
                                                "receiveType": 0,
                                                "billGroupId": 120345
                                            }
                                            )
                    shenase_response = shenase.json()
                    # print
                    # message=message+'<br> با مشخصات ذیل می توانید از درگاه بانک های ملت،شهر،انصار،پاسارگاد پرداخت کنید:'
                    # message=message+'شناسه قبض: {} <br>'.format(shenase_response['billId'])
                    # message=message+'شناسه پرداخت: {} <br>'.format(shenase_response['paymentId'])
                    # message=message+'مبلغ: {} ریال'.format(amount)
                    # message=message+'<br> آدرس اینترنتی پرداخت'
                    # message=message+request.build_absolute_uri()
                    # message=message+'https://sharifngo.com'
                    # ---------------------------
                    cmpn = None
                    if type == CommandType.کمپین.value:
                        cmpn_result = ussd_call.objects.filter(session_id=session_id)
                        cmpn_row = cmpn_result.first()
                        ussd_cmd = cmpn_row.call
                        cmd_index = ussd_cmd.rfind('*')
                        cmd = ussd_cmd[cmd_index + 1:]
                        # print
                        cmd_obj = ussd_command.objects.filter(command_id=int(cmd)).filter(
                            command_type=CommandType.کمپین).first()
                        if cmd_obj.campaign is not None:
                            cmpn = cmd_obj.campaign

                        # print(cmd_obj.first())
                        # cmd_obj_first=cmd_obj.first()
                        # campaing=cmd_obj_first.campaign.title+'*********'
                        # print(campaing)
                        # cmpn=cmd_obj_first.campaign

                    # ---------------------------

                    donation = Donation(mobile=mobile, amount=amount, bill_id=shenase_response['billId'],
                                        bill_no=shenase_response['paymentId'], session_id=session_id, campaing=cmpn)
                    donation.save()

                    sms_message = 'بنیاد نیکوکاران شریف\r\n'
                    sms_message = sms_message + '\r\n با مشخصات ذیل می توانید از درگاه بانک های ملت،شهر،انصار،پاسارگاد پرداخت کنید:'
                    sms_message = sms_message + 'شناسه قبض: {} \r\n'.format(shenase_response['billId'])
                    sms_message = sms_message + 'شناسه پرداخت: {} \r\n'.format(shenase_response['paymentId'])
                    sms_message = sms_message + 'مبلغ: {} ریال'.format(int(amount))
                    #sms_message = sms_message + '\r\nپرداخت مستقیم با USSD'
                    #sms_message = sms_message + '\r\n *720*3*2*{}*{}#'.format(shenase_response['billId'],
                    #                                                          shenase_response['paymentId'])

                    send_sms(reciptant=mobile, message=sms_message)
                    # message=message+request.get_host()+'/'+donation.unique_url_code
                    message = message + 'با سپاس از شما، پیامکی حاوی روش های پرداخت برای شما ارسال گردید'
                    # print(amount)
    # print(request.get_host())

    return HttpResponse(message)


# def add_donation(session_id,mobile,amount):


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
            USSD_Request.command_type = CommandType.منو
            update_ussd_commands_history(USSD_Request)
            sub = result.ussd_command_set.all()
            if sub.count() != 0:
                for item in sub:
                    message = message + str(getattr(item, 'command_id')) + '-' + getattr(item, 'title') + '<br/>'
        if cmd_type == 3:
            USSD_Request.command_type = CommandType.حمایت
            update_ussd_commands_history(USSD_Request)

            message = message + 'مبلغ حمایت را وارد کنید'
    return HttpResponse(message)


def update_ussd_commands_history(req):
    result = ussd_call.objects.filter(session_id=req.session_id)
    if result.count() == 0:
        res = ussd_call(call=req.call, session_id=req.session_id, mobile=req.mobile, date_time=datetime.now(),
                        command_type=req.command_type)
        res.save()
    else:
        res = result.first()
        res.call = req.call
        res.command_type = req.command_type
        res.save()
