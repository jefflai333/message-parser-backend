class Message:
    def __init__(self, sender_name, timestamp_ms, content, reactions, type):
        self.sender_name = sender_name
        self.timestamp_ms = timestamp_ms
        self.content = content
        self.reactions = reactions
        self.type = type
