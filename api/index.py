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
    
    # GET request - check if setting webhook
    set_webhook = request.args.get("setWebhook")
    if set_webhook:
        from .config import BOT_TOKEN
        import requests
        host = request.headers.get('host', '')
        url = f"https://{host}/"
        tg_url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={url}"
        res = requests.get(tg_url).json()
        return jsonify({
            "status": "webhook_attempt",
            "url": url,
            "telegram_response": res
        })

    # Default GET request - health check
    return jsonify({
        "status": "running",
        "bot": "MindVault",
        "version": "2.0",
        "setup": "Visit /?setWebhook=true to configure Telegram webhook"
    })
