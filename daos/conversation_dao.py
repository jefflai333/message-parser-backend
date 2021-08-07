import psycopg2
from .message_dao import MessageDAO
from .participant_dao import ParticipantDAO


class ConversationDAO():
    def __init__(self):
        self.message_dao = MessageDAO()
        self.participant_dao = ParticipantDAO()

    def save_conversation(self, conversation):
        conn = psycopg2.connect(dbname="test", user="postgres",
                                password="password", host="localhost", port="5433")
        cur = conn.cursor()
        # insert into conversations table
        thread_path = conversation.thread_path
        cur.execute(
            "SELECT id from conversations where thread_path = %s;", (thread_path,))
        conversation_id = cur.fetchone()
        if conversation_id is None:
            cur.execute(
                "INSERT INTO conversations (thread_path) VALUES (%s) RETURNING id;", (thread_path,))
            conversation_id = cur.fetchone()[0]
        else:
            conversation_id = conversation_id[0]
        conn.commit()
        cur.close()
        conn.close()
        for participant in conversation.participants:
            self.participant_dao.save_participant_and_conversation_participant(
                participant, conversation_id)
        for message in conversation.messages:
            self.message_dao.save_message(message, conversation_id)

    def get_conversation_id(self, thread_path):
        conn = psycopg2.connect(dbname="test", user="postgres",
                                password="password", host="localhost", port="5433")
        cur = conn.cursor()
        cur.execute(
            "SELECT id from conversations where thread_path = %s;", (thread_path,))
        rows = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        if rows is None:
            return None
        else:
            return rows[0]
