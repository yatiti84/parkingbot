import os
import json
import requests


class ParkingPayment():
    def __init__(self, carrier_type):
        self.parking_url = os.environ.get('parking_url')
        self.check_url = os.environ.get('check_url')
        self.redirect_url = os.environ.get('check_url')
        self.phone = os.environ.get('phone')
        self.carrier_id = os.environ.get('carrierId')
        self.payment_type = os.environ.get('payment_type')
        self.carrier_type = carrier_type
        self.npoban = os.environ.get('NPOBAN')

    def callParkingApi(self) -> str:

        raw_payment_resp = requests.get(self.parking_url)
        payment_resp = json.loads(raw_payment_resp.content.decode('utf-8'))
        transaction_token = payment_resp['transaction_token']
        payment_content = {"Phone": self.phone,
                           "Tax": "",
                           "transaction_token": transaction_token,
                           "PaymentType": self.payment_type,
                           "CarrierType": self.carrier_type,
                           "CarrierId": self.carrier_id,
                           "NPOBAN": self.npoban,
                           "redirect_url": self.redirect_url}

        resp = requests.post(self.check_url, data=payment_content)
        print(resp.content.decode('utf-8'))

        return resp.content.decode('utf-8')
