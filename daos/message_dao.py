import psycopg2


class MessageDAO():
    def __init__(self):
        pass

    def save_message(self, message, conversation_id):
        conn = psycopg2.connect(dbname="test", user="postgres",
                                password="password", host="localhost", port="5433")
        cur = conn.cursor()
        # insert into messages table
        content = message.content
        timestamp = message.timestamp
        sender_name = message.sender_name
        # guaranteed sender name matching name in participants field due to validation of json
        cur.execute("SELECT id from participants WHERE name = %s", sender_name)
        participant_id = cur.fetchone()[0]
        cur.execute(
            "INSERT INTO messages (content, timestamp, conversation_id, participant_id) VALUES (%s, %s, %s, %s)", (content, timestamp, conversation_id, participant_id))
        conn.commit()
        cur.close()
        conn.close()
