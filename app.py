import requests
import os
import json
import flask

app = flask.Flask(__name__)
app.config.from_object('configs.Config')


@app.route('/health')
def health_test():
    return 'ok'


@app.route('/receiver', methods=['GET', 'POST'])
def receiver():
    params = flask.request.args
    return params


def callParkingApi():
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
                       "PaymentType": app.config['paymentType'],
                       "CarrierType": app.config['carrierType'],
                       "CarrierId": carrierId,
                       "redirect_url": redirect_url}

    resp = requests.post(check_url, data=payment_content)
    print(resp.text)


if __name__ == '__main__':
    # callParkingApi()
    app.run(port=5000)
