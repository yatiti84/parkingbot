import base64
import hashlib
import hmac
import os
import requests
import json


class Webhook():
    def __init__(self, receiver_msg):

        self.channel_secret = os.environ.get('CHANNEL_SECRET')
        self.line_reply_url = os.environ.get('line_reply_url')
        self.channel_access_token = os.environ.get('CHANNEL_ACCESS_TOKEN')
        self.request_header = receiver_msg.headers
        self.receiver_msg = receiver_msg.data
        self.request_user_id = receiver_msg.get_json().get('destination')
        self.request_events = receiver_msg.get_json().get('events')

    def signatureValidation(self):

        hash = hmac.new(self.channel_secret.encode('utf-8'),
                        self.receiver_msg, hashlib.sha256).digest()
        signature = base64.b64encode(hash)
        try:
            x_line_signature = self.request_header.get(
                'x-line-signature')
        except KeyError:
            x_line_signature = self.request_header.get(
                'X-Line-Signature')
        # Compare  request header and the signature
        print(
            f"signatureValidation is{x_line_signature.encode('utf-8') == signature}")
        return x_line_signature.encode('utf-8') == signature

    def requestBodyCheck(self):
        # user_id = self.request_body.get('destination')
        # events = self.request_body.get('events')
        return

    def sendReply(self, reply_token: str) -> None:
        headers = {
            'Content-Type': 'application/json', 
            'Authorization': f'Bearer {self.channel_access_token}'
            }
        reply_data = json.dumps({
            "replyToken": reply_token,
            "messages": [
                {
                    "type": "text",
                    "text": "Hello, user"
                },
                {
                    "type": "text",
                    "text": "May I help you?"
                }
            ]
        })
        print(headers)
        raw_payment_resp = requests.post(
            url=self.line_reply_url, headers=headers, data=reply_data)
        print(raw_payment_resp.status_code)
        print(raw_payment_resp.text)

        return
