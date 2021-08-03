import psycopg2
from datetime import datetime
from .conversation import Conversation


class MessageIndexer():
    def __init__(self, listOfConversations):
        self.listOfConversations = listOfConversations

    def message_indexer(self):
        for i, conversation in enumerate(self.listOfConversations):
            print("indexing " + str(i+1) + " of " +
                  str(len(self.listOfConversations)) + " conversations")
            self.conversation_indexer(conversation)

    def conversation_indexer(self, conversation):
        conn = psycopg2.connect(dbname="test", user="postgres",
                                password="password", host="localhost", port="5433")
        cur = conn.cursor()
        messages = conversation.messages
        title = conversation.title
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
