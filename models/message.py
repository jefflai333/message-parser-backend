from datetime import datetime, timezone


class Message:
    def __init__(self):
        self.sender_name = None
        self.date = None
        self.content = None

    def add_sender_name(self, sender_name):
        self.sender_name = sender_name

    def add_date(self, timestamp_ms):
        self.date = self.getDate(timestamp_ms)

    def add_content(self, content):
        self.content = content

    def getDate(self, timestamp_ms):
        try:
            date = datetime.fromtimestamp(timestamp_ms/1000, timezone.utc)
        except:
            date = None
        return date