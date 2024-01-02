import os
import json
import requests


class ParkingPayment():
    def __init__(self, carrier_type):
        self.parking_url = os.environ.get('parking_url')
        self.check_url = os.environ.get('check_url')
        self.redirect_url = os.environ.get('redirect_url')
        self.phone = os.environ.get('phone')
        self.carrier_id = os.environ.get('carrierId')
        self.payment_type = os.environ.get('payment_type')
        self.carrier_type = carrier_type
        self.npoban = os.environ.get('NPOBAN')

    def carrierTypeDetermination(self):
        if self.carrier_type == 'mobile':
            return {"Phone": self.phone,
                    "Tax": "",
                    "PaymentType": self.payment_type,
                    "CarrierType": self.carrier_type,
                    "CarrierId": self.carrier_id,
                    "redirect_url": self.redirect_url}
        elif self.carrier_type == 'donate':
            return {"Phone": self.phone,
                    "Tax": "",
                    "PaymentType": self.payment_type,
                    "CarrierType": self.carrier_type,
                    "NPOBAN": self.npoban,
                    "redirect_url": self.redirect_url}
        return

    def parsePaymentResponse(self, raw_response: str):
        resp = json.loads(raw_response)
        if 'success' in resp:
            return resp['url']
        elif 'message' in resp:
            return resp['message']
        return raw_response

    def responseCheckAndParse(self, response):
        if response.status_code == 200:
            print(response.content)
            return json.loads(response.content.decode('utf-8'))
        print(f'Request failed with status code: {response.status_code}')
        return None

    def callParkingApi(self) -> str:

        raw_parking_status_resp = requests.get(self.parking_url)
        parking_status_resp = self.responseCheckAndParse(
            raw_parking_status_resp)
        if parking_status_resp and 'in_park' in parking_status_resp and parking_status_resp['in_park']:
            payment_content = self.carrierTypeDetermination()
            payment_content['transaction_token'] = parking_status_resp['transaction_token']
            raw_payment_resp = requests.post(
                self.check_url, data=payment_content)
            payment_resp = self.responseCheckAndParse(raw_payment_resp)
            if payment_resp:
                return self.parsePaymentResponse(payment_resp)

        elif 'in_park' in parking_status_resp and parking_status_resp['in_park'] is False:
            return parking_status_resp
