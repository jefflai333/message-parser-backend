from flask import Flask
import message_querer

app = Flask(__name__)

@app.route("/table", methods=["GET"])
def show_stats():
    count = message_querer.query_aggregate_data_from_db()
    return str(count)