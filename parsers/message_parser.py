from typing import Dict
from ..models.message import Message


class MessageParser:
    def __init__(self):
        pass

    def parse_message(self, d):
        message = Message()
        if not isinstance(d, dict):
            return message
        if "sender_name" in d:
            message.add_sender_name(d["sender_name"])
        if "timestamp_ms" in d:
            message.add_date(d["timestamp_ms"])
        if "content" in d:
            message.add_word_count(d["content"])
            message.add_char_count(d["content"])
        return message
