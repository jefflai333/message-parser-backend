from typing import Dict
from ..models.message import Message


class MessageParser:
    def __init__(self):
        pass

    def parse_message(d):
        message = Message()
        if not isinstance(d, dict):
            return message
        if "sender_name" in d:
            message.add_sender_name(d["sender_name"])
        if "timestamp_ms" in d:
            message.add_timestamp_ms(d["timestamp_ms"])
        if "content" in d:
            message.add_content(d["content"])
        return message
