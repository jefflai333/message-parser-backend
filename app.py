from flask import Flask, request
from flask_cors import CORS
from . import MessageQuerer
from . import MessageParser
from . import MessageIndexer
import psycopg2
import os

app = Flask(__name__)
CORS(app)


@app.before_request
def before_request():
    try:
        conn = psycopg2.connect(dbname="test", user="postgres",
                                password="password", host="localhost", port="5433")
        print("Successfully connected to DB")
    except Exception as err:
        print("error msg:", err)
        os._exit(0)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS messages (id SERIAL, sender VARCHAR(255) NOT NULL, date TIMESTAMP NOT NULL, message VARCHAR(64000), conversation_id INTEGER NOT NULL, participant_id INTEGER NOT NULL, PRIMARY KEY (id), FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE, FOREIGN KEY (participant_id) REFERENCES participants(id) ON DELETE CASCADE);")
    cur.execute(
        "CREATE TABLE IF NOT EXISTS conversations (id SERIAL, thread_path VARCHAR(255) NOT NULL, UNIQUE(thread_path), PRIMARY KEY (id));")
    cur.execute(
        "CREATE TABLE IF NOT EXISTS participants (id SERIAL, name VARCHAR(255) NOT NULL, PRIMARY KEY (id));")
    cur.execute(
        "CREATE TABLE IF NOT EXISTS conversations_participants (conversation_id INTEGER NOT NULL, participant_id INTEGER NOT NULL, PRIMARY KEY (conversation_id, participant_id), FOREIGH KEY (conversation_id) REFERENCES conversations(id) ON UPDATE CASCADE, FOREIGN KEY (participant_id) REFERENCES participants(id) ON UPDATE CASCADE;")
    conn.commit()
    cur.close()
    conn.close()


@app.route("/table", methods=["GET"])
def show_stats():
    stats = MessageQuerer.query_aggregate_data_from_db()
    return {
        "count": stats[0],
        "received_messages": stats[1],
        "sent_messages": stats[2],
        "title": stats[3]
    }


@app.route("/add", methods=["POST"])
def add_stats():
    file = request.form["file"]
    message = MessageParser(file)
    messageIndexer = MessageIndexer(message.listOfConversations)
    messageIndexer.message_indexer()
    return {"status": 200}
