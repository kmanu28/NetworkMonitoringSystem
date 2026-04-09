import sys
import os

sys.path.insert(0, os.path.abspath("server"))

from database import get_events
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def index():
    node_filter = request.args.get("node")
    event_filter = request.args.get("event")

    events = get_events()

    # Apply filters
    if node_filter:
        events = [e for e in events if node_filter.lower() in e[0].lower()]

    if event_filter:
        events = [e for e in events if event_filter.lower() in e[2].lower()]

    return render_template("index.html", events=events)


if __name__ == "__main__":
    app.run(debug=True, port=5000)