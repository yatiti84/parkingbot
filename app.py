import flask
import webhook

app = flask.Flask(__name__)
app.config.from_object('configs.Config')


@app.route('/health')
def health_test():
    return 'ok'


@app.route('/receiver', methods=['GET', 'POST'])
def receiver():
    print(flask.request.args)
    print(flask.request.headers)
    webhook_manager = webhook.Webhook(flask.request)
    if webhook_manager.signatureValidation():
        print("Sign Validation")
    return 
        # webhook_manager.requestBodyCheck()
    # params = flask.request.args
    # print(params)


if __name__ == '__main__':
    # callParkingApi()
    app.run(port=5000)
