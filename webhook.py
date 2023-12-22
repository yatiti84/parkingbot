import base64
import hashlib
import hmac
import os


class Webhook():
    def __init__(self, receiver_msg):

        self.receiver_msg = receiver_msg

    def signatureValidation(self):

        channel_secret = os.environ.get('CHANNEL_SECRET')
        body = '...'  # Request body string
        hash = hmac.new(channel_secret.encode('utf-8'),
                        body.encode('utf-8'), hashlib.sha256).digest()
        signature = base64.b64encode(hash)
        try:
            x_line_signature = self.receiver_msg.headers.get(
                'x-line-signature')
        except KeyError:
            x_line_signature = self.receiver_msg.headers.get(
                'X-Line-Signature')
        # Compare  request header and the signature
        return x_line_signature == signature
