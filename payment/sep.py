
from requests import Session
from zeep import Client, Transport
class PaymentGatewayAdapter(object):
    def __init__(self):
        pass

    def create_client(self, web_service) -> Client:
        session = Session()
        session.headers = {}
        transport = Transport(session=session)
        transport.session.headers = {}  # DON'T REMOVE THIS LINE.YOU BLOCK FROM SAMAN BANK IF REMOVE THIS LINE
        return Client(web_service, transport=transport)

    def sep_request_token(self, amount,mid,resNum,redirectUrl):
        client = self.create_client('https://sep.shaparak.ir/payments/initpayment.asmx?wsdl')

        res_num = resNum
        #print('{} {} {}'.format(res_num,mid,int(amount)))
        response = client.service.RequestToken(
            '{}'.format(mid),
            '{}'.format(res_num),
            '{}'.format(int(amount)),
            0, 0, 0, 0, 0, 0,
            'additional1',
            'additional2',
            0,
            redirectUrl
        )
        token = str(response)
        print('Token is: {}'.format(token))
        return token, res_num

    def sep_verify_transaction(self, ref_num,MID):
        client = self.create_client('https://verify.sep.ir/Payments/ReferencePayment.asmx?WSDL')
        result = client.service.verifyTransaction(
            '{}'.format(ref_num),
            '{}'.format(MID)
        )
        return result

    def sep_reverse_transaction(self, ref_num):
        client = self.create_client('https://sep.shaparak.ir/payments/referencepayment.asmx?wsdl')
        result = client.service.reverseTransaction(
            ref_num,
            "saman mid",
            "saman mid",
            "saman password"
        )
        return result

