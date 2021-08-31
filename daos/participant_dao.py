import psycopg2


class ParticipantDAO():
    def __init__(self):
        pass

    def save_participant_and_conversation_participant(self, participant, conversation_id, connection_pool):
        conn = connection_pool.getconn()
        cur = conn.cursor()
        # insert into participants table
        name = participant.name
        cur.execute(
            "SELECT id from participants where name = %s;", (name,))
        participant_id = cur.fetchone()
        if participant_id is None:
            cur.execute(
                "INSERT INTO participants (name) VALUES (%s) RETURNING id;", (name,))
            participant_id = cur.fetchone()[0]
        else:
            participant_id = participant_id[0]
        cur.execute(
            "SELECT * from conversations_participants where conversation_id = %s and participant_id = %s;", (conversation_id, participant_id))
        conversations_participants_id = cur.fetchone()
        if conversations_participants_id is None:
            # insert into conversations_participants table
            cur.execute(
                "INSERT INTO conversations_participants (conversation_id, participant_id) VALUES (%s, %s);", (conversation_id, participant_id))
        conn.commit()
        cur.close()
        connection_pool.putconn(conn)
