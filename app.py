import flask
import webhook
import parkingPayment
import event
app = flask.Flask(__name__)


@app.route('/health')
def health_test():
    return 'ok'


@app.route('/receiver', methods=['GET', 'POST'])
def receiver():
    print(flask.request.get_json())
    webhook_manager = webhook.Webhook(flask.request)
    if webhook_manager.signatureValidation() and webhook_manager.requestEventsCheck():
        for raw_event in webhook_manager.request_events:
            if raw_event['type'] == 'message' and raw_event['message']['type'] == 'text':
                request_event = event.MessageEvent(raw_event)
                action = request_event.parseText()
                print(action)
                if action['is_start']:
                    print("start to send reply")
                    payment_manager = parkingPayment.ParkingPayment(
                        action['carrier_type'])
                    payment_url = payment_manager.callParkingApi()
                    webhook_manager.sendReply(
                        request_event.replyToken, payment_url)
            else:
                print("not a message event")
    return "received"
    # params = flask.request.args
    # print(params)


if __name__ == '__main__':
    app.run(port=5000)
