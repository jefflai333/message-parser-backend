import psycopg2
from datetime import datetime


def message_indexer(jsonData):
    try:
        conn = psycopg2.connect(dbname="test", user="postgres",
                            password="password", host="localhost", port="5433")
    except Exception as err:
        print("error msg:", err)
        conn = None
    if conn != None:
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS messages (id SERIAL, sender VARCHAR(255) NOT NULL, date TIMESTAMP NOT NULL, message VARCHAR(4095), type VARCHAR(63) NOT NULL, title VARCHAR(255), PRIMARY KEY (id));")
        messages = jsonData["messages"]
        title = jsonData["title"]
        for message in messages:
            sender = message["sender_name"]
            dt = datetime.fromtimestamp(message["timestamp_ms"]/1000)
            msg = None
            if "content" in message:
                msg = message["content"]
            type = message["type"]
            cur.execute(
                "INSERT INTO messages (sender, date, message, type, title) VALUES (%s, %s, %s, %s, %s)", (sender, dt, msg, type, title))
        conn.commit()
        cur.close()
        conn.close()
