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
        date = message.date
        sender_name = message.sender_name
        # guaranteed sender name matching name in participants field due to validation of json
        cur.execute("SELECT id from participants WHERE name = '{0}';".format(sender_name))
        participant_id = cur.fetchone()[0]
        cur.execute(
            "INSERT INTO messages (message, date, conversation_id, participant_id) VALUES ('{0}', '{1}', {2}, {3});".format(content, date, conversation_id, participant_id))
        conn.commit()
        cur.close()
        conn.close()
