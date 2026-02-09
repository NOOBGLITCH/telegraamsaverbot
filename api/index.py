from flask import Flask, request, jsonify
from .handle import handle_update

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def index():
    """Main webhook endpoint"""
    if request.method == "POST":
        # Handle Telegram webhook update
        update_data = request.json
        handle_update(update_data)
        return "ok"
    
    # GET request - health check
    return jsonify({
        "status": "running",
        "bot": "MindVault",
        "version": "2.0"
    })
