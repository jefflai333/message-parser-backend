import psycopg2


class MessageDAO():
    def __init__(self):
        pass

    def save_message(self, message, conversation_id, connection_pool):
        conn = connection_pool.getconn()
        cur = conn.cursor()
        # insert into messages table
        word_count = message.word_count
        char_count = message.char_count
        date = message.date
        sender_name = message.sender_name
        # guaranteed sender name matching name in participants field due to validation of json
        cur.execute(
            "SELECT id from participants WHERE name = %s;", (sender_name,))
        participant_id = cur.fetchone()[0]
        cur.execute(
            "INSERT INTO messages (word_count, char_count, date, conversation_id, sender_participant_id) VALUES (%s, %s, %s, %s, %s);", (word_count, char_count, date, conversation_id, participant_id))
        conn.commit()
        cur.close()
        connection_pool.putconn(conn)
