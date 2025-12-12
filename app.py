import os
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    version = os.environ.get("APP_VERSION", "unknown")
    return f"Hello from Jenkins + Portainer CI/CD! Current build: {version}"

@app.route("/version")
def version():
    version = os.environ.get("APP_VERSION", "unknown")
    return jsonify({"version": version})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

