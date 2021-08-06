import psycopg2


class ParticipantDAO():
    def __init__(self):
        pass

    def save_participant_and_conversation_participant(self, participant, conversation_id):
        conn = psycopg2.connect(dbname="test", user="postgres",
                                password="password", host="localhost", port="5433")
        cur = conn.cursor()
        # insert into participants table
        name = participant.name
        cur.execute(
            "INSERT INTO participants (name) VALUES (%s) RETURNING id", (name))
        participant_id = cur.fetchone()[0]
        # insert into conversations_participants table
        cur.execute(
            "INSERT INTO conversations_participants (conversation_id, participant_id) VALUES (%s, %s)", (conversation_id, participant_id))
        conn.commit()
        cur.close()
        conn.close()
