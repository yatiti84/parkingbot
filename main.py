import requests
import os
import json


parking_url = os.environ.get('parking_url')
check_url = os.environ.get('check_url')
redirect_url = os.environ.get('check_url')
phone = os.environ.get('phone')
carrierId = os.environ.get('carrierId')
raw_payment_resp = requests.get(parking_url)
payment_resp = json.loads(raw_payment_resp.content.decode('utf-8'))
transaction_token = payment_resp['transaction_token']
payment_content = {"Phone": phone,
                   "Tax": "",
                   "transaction_token": transaction_token,
                   "PaymentType": "linepay",
                   "CarrierType": "mobile",
                   "CarrierId": carrierId,
                   "redirect_url": redirect_url}

resp = requests.post(check_url, data=payment_content)
print(resp.text)

if __name__ == '__main__':

