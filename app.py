from flask import Flask
from flask_cors import CORS
import message_querer

app = Flask(__name__)
CORS(app)


@app.route("/table", methods=["GET"])
def show_stats():
    stats = message_querer.query_aggregate_data_from_db()
    return {
        "count": stats[0],
        "received_messages": stats[1],
        "sent_messages": stats[2],
        "title": stats[3]
    }
