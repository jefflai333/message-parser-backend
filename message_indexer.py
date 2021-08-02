import psycopg2
from datetime import datetime


class MessageIndexer():
    def __init__(self, conversation):
        self.conversation = conversation

    def message_indexer(self):
        conn = psycopg2.connect(dbname="test", user="postgres",
                                password="password", host="localhost", port="5433")
        cur = conn.cursor()
        messages = self.conversation.messages
        title = self.conversation.title
        for message in messages:
            sender = message.sender_name
            dt = datetime.fromtimestamp(message.timestamp_ms/1000)
            msg = message.content
            type = message.type
            cur.execute(
                "INSERT INTO messages (sender, date, message, type, title) VALUES (%s, %s, %s, %s, %s)", (sender, dt, msg, type, title))
        conn.commit()
        cur.close()
        conn.close()
