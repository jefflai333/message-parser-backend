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
                "SELECT id from participants where name = '{0}';".format(name))
        participant_id = cur.fetchone()
        if participant_id is None:
            cur.execute(
                "INSERT INTO participants (name) VALUES ('{0}') RETURNING id;".format(name))
            participant_id = cur.fetchone()[0]
        else:
            participant_id = participant_id[0]
        cur.execute(
                "SELECT * from conversations_participants where conversation_id = {0} and participant_id = {1};".format(conversation_id, participant_id))
        conversations_participants_id = cur.fetchone()
        if conversations_participants_id is None:
            # insert into conversations_participants table
            cur.execute(
                "INSERT INTO conversations_participants (conversation_id, participant_id) VALUES ({0}, {1});".format(conversation_id, participant_id))
        conn.commit()
        cur.close()
        conn.close()
