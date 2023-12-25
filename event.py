class Event():
    def __init__(self, raw_data: dict) -> None:
        self.type = raw_data['type']
        self.timestamp = raw_data['timestamp']
        self.mode = raw_data['mode']
        self.webhookEventId = raw_data['webhookEventId']


class MessageEvent(Event):
    def __init__(self, raw_data: dict) -> None:
        super().__init__(raw_data)
        message = raw_data['message']
        self.replyToken = raw_data['replyToken']
        self.message_type = message['type']
        self.message_text = message['text']

    def parseText(self) -> dict:

        action = {
            "is_start": True if 'start' in self.message_text or '開始' in self. message_text else False,
            "carrier_type": 'donate' if 'donate' in self.message_text or '捐' in self. message_text else 'mobile'
        }

        return action
