import os
import socket
from datetime import datetime, timezone

from flask import Flask, jsonify, render_template

app = Flask(__name__)

APP_VERSION = os.getenv("APP_VERSION", "0.1.0")
ENVIRONMENT = os.getenv("APP_ENV", "local")


@app.route("/")
def index():
    context = {
        "version": APP_VERSION,
        "environment": ENVIRONMENT,
        "hostname": socket.gethostname(),
        "server_time": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
    }
    return render_template("index.html", **context)


@app.route("/healthz")
def healthz():
    """Liveness probe - is the process up?"""
    return jsonify(status="ok"), 200


@app.route("/readyz")
def readyz():
    """Readiness probe - is the app ready to serve traffic?"""
    return jsonify(status="ready"), 200


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
