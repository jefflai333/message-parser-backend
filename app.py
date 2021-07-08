from flask import Flask
import message_querer

app = Flask(__name__)

@app.route("/")
def show_stats():
    count = message_querer.query_aggregate_data_from_db()
    return "<p>" + str(count) + "</p>"