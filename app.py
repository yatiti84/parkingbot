import flask
import webhook
import parkingPayment
import event
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
    if webhook_manager.signatureValidation() and webhook_manager.requestEventsCheck():
        for raw_event in webhook_manager.request_events:
            if raw_event['type'] == 'message':
                request_event = event.MessageEvent(raw_event)
                action = request_event.parseText(request_event.message_text)
                if action['is_start']:
                    print("start to send reply")
                    payment_manager = parkingPayment.ParkingPayment(
                        action['carrier_type'])
                    payment_url = payment_manager.callParkingApi()
                    webhook_manager.sendReply(
                        request_event.replyToken, payment_url)
            else:
                print("not a message event")
            return

        # webhook_manager.requestBodyCheck()

    return "received"
    # params = flask.request.args
    # print(params)


if __name__ == '__main__':
    app.run(port=5000)
