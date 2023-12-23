import flask
import webhook
import parkingPayment
app = flask.Flask(__name__)
app.config.from_object('configs.Config')


@app.route('/health')
def health_test():
    return 'ok'


@app.route('/receiver', methods=['GET', 'POST'])
def receiver():
    print(flask.request.data)
    print(flask.request.get_json())
    print(flask.request.headers)
    webhook_manager = webhook.Webhook(flask.request)
    if webhook_manager.signatureValidation():
        for event in webhook_manager.request_events:
            print("start to send reply")
            payment_manager = parkingPayment.ParkingPayment()
            payment_url = payment_manager.callParkingApi()
            webhook_manager.sendReply(event['replyToken'], payment_url)
        # webhook_manager.requestBodyCheck()

    return "received"
    # params = flask.request.args
    # print(params)


if __name__ == '__main__':
    app.run(port=5000)
