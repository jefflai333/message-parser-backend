from flask import Flask
from flask_cors import CORS
import message_querer

app = Flask(__name__)
CORS(app)


@app.route("/table", methods=["GET"])
def show_stats():
    count = message_querer.query_aggregate_data_from_db()
    return {
        "count": count[0]
    }
