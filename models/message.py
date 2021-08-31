from datetime import datetime, timezone


class Message:
    def __init__(self):
        self.sender_name = None
        self.date = None
        self.word_count = 0
        self.char_count = 0

    def add_sender_name(self, sender_name):
        self.sender_name = sender_name

    def add_date(self, timestamp_ms):
        self.date = self.getDate(timestamp_ms)

    def add_word_count(self, content):
        if isinstance(content, str):
            self.word_count = len(content.split())

    def add_char_count(self, content):
        if isinstance(content, str):
            # removes spaces from string in content when counting chars
            self.char_count = len(content) - content.count(" ")

    def getDate(self, timestamp_ms):
        try:
            date = datetime.fromtimestamp(timestamp_ms/1000, timezone.utc)
        except:
            date = None
        return date