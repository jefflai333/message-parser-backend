import psycopg2
from datetime import datetime

def message_indexer(jsonData):
    conn = psycopg2.connect(dbname="test", user="postgres", password="password", host="0.0.0.0", port="5433")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS messages (id SERIAL, sender VARCHAR(255) NOT NULL, date TIMESTAMP NOT NULL, message VARCHAR(4095), type VARCHAR(63) NOT NULL, PRIMARY KEY (id));")
    for json_key, json_value in jsonData.items():
        if json_key == "messages":
            messages = json_value
            for message in messages:
                sender = message["sender_name"]
                dt = datetime.fromtimestamp(message["timestamp_ms"]/1000)
                msg = None
                if "content" in message:
                    msg = message["content"]
                type = message["type"]
                cur.execute("INSERT INTO messages (sender, date, message, type) VALUES (%s, %s, %s, %s)", (sender, dt, msg, type))
    conn.commit()
    cur.close()
    conn.close()