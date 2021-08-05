import psycopg2
from .message_dao import MessageDAO
from .participant_dao import ParticipantDAO


class ConversationDAO():
    def __init__(self):
        self.message_dao = MessageDAO()
        self.participant_dao = ParticipantDAO()
