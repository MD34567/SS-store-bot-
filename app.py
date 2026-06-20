import os
import threading
from flask import Flask
from bot import run_bot

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

if __name__ == "__main__":
    # Start bot in background
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    # Start web server
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
