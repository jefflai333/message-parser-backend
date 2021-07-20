from flask import Flask, request
from flask_cors import CORS
from . import message_querer
from . import message_parser

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

@app.route("/add", methods=["POST"])
def add_stats():
    file = request.form["file"]
    return message_parser.parse_json(file)