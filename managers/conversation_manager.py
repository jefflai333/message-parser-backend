import psycopg2
from psycopg2 import pool
from .message_manager import MessageManager
from .participant_manager import ParticipantManager
from ..daos.conversation_dao import ConversationDAO


class ConversationManager:
    def __init__(self):
        self.message_manager = MessageManager()
        self.participant_manager = ParticipantManager()
        self.connection_pool = self.create_connection_pool()
        self.conversation_dao = ConversationDAO()

    def create_connection_pool(self):
        try:
            connection_pool = psycopg2.pool.SimpleConnectionPool(5, 20, dbname="test", user="postgres",
                                    password="password", host="localhost", port="5433")
            print("Successfully created connection pool to DB")
        except Exception as err:
            print("error msg:", err)
        return connection_pool
    
    def is_conversation_valid(self, conversation):
        # participants are now derived from messages, so the participants array isn't needed anymore
        requiredAttrs = ["messages", "thread_path"]
        for attrs in requiredAttrs:
            if not hasattr(conversation, attrs):
                return False
        if conversation.thread_path is None:
            print("thread_path doesn't exist")
            return False
        participants = set()
        for message in conversation.messages:
            if not self.message_manager.is_valid_message(message):
                print("error with message validation")
                return False
            participants.add(message.sender_name)
        for participant in participants:
            if not self.participant_manager.is_valid_participant(participant):
                print("error with participant validation")
                return False
        return True

    def commit_conversation(self, conversation):
        self.conversation_dao.save_conversation(conversation, self.connection_pool)
        return 1
