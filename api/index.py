from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        return "ok"
    return jsonify({
        "status": "running",
        "message": "MindVault Bot is live!",
        "test": "If you see this, deployment worked!"
    })
