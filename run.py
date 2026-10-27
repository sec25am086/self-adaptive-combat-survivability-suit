"""Flask backend for the Self-Adaptive Camouflage Suit dashboard."""
import csv
import os

from flask import Flask, jsonify, request, send_from_directory

from detector import detect

BASE = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE, "sample_sensor_data.csv")

app = Flask(__name__)
state = {"collector": "Stopped", "index": 0}


def read_csv():
    with open(CSV_PATH, newline="") as f:
        return list(csv.DictReader(f))


@app.route("/")
def index():
    return send_from_directory(BASE, "index.html")


@app.route("/style.css")
def css():
    return send_from_directory(BASE, "style.css")


@app.route("/app.js")
def js():
    return send_from_directory(BASE, "app.js")


@app.route("/api/collector/start", methods=["POST"])
def start():
    state["collector"] = "Running"
    return jsonify(status=state["collector"])


@app.route("/api/collector/stop", methods=["POST"])
def stop():
    state["collector"] = "Stopped"
    return jsonify(status=state["collector"])


@app.route("/api/collector/status")
def status():
    return jsonify(status=state["collector"])


@app.route("/api/sensors")
def sensors():
    rows = read_csv()
    row = rows[state["index"] % len(rows)]
    if state["collector"] == "Running":
        state["index"] += 1  # values update on each refresh while running
    return jsonify(row)


@app.route("/api/data")
def data():
    return jsonify(read_csv())


@app.route("/api/detect", methods=["POST"])
def detect_route():
    file = request.files.get("image")
    if not file:
        return jsonify(error="No image uploaded"), 400
    try:
        return jsonify(detect(file.read()))
    except Exception as exc:
        return jsonify(error=f"Could not read image: {exc}"), 400


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
