class Message:
    def __init__(self):
        self.sender_name = None
        self.timestamp_ms = None
        self.content = None

    def __init__(self, sender_name, timestamp_ms, content):
        self.sender_name = sender_name
        self.timestamp_ms = timestamp_ms
        self.content = content

    def add_sender_name(self, sender_name):
        self.sender_name = sender_name

    def add_timestamp_ms(self, timestamp_ms):
        self.timestamp_ms = timestamp_ms

    def add_content(self, content):
        self.content = content
