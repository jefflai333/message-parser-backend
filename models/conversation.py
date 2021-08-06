from .message import Message
from .participant import Participant


class Conversation:
    def __init__(self):
        self.participants = [Participant()]
        self.messages = [Message()]
        self.thread_path = None

    def add_participants(self, participants):
        self.participants = participants

    def add_messages(self, messages):
        self.messages = messages

    def add_thread_path(self, thread_path):
        self.thread_path = thread_path
