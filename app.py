from flask import Flask, request
import requests

app = Flask(__name__)

# CONFIGURATION - Replace with your real info
TOKEN = "8705048447:AAHF9rxbUMa0gfRvedvRtENVHdHs0bV6l-M"
CHAT_ID = "5964079884"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if not data:
        return "Invalid Data", 400

    ticker = data.get('ticker', 'Unknown')
    entry = float(data.get('price', 0))
    side = data.get('side', 'Buy').capitalize()
    
    # NQ Contract Math for $650 (2 Minis)
    # TP1: +17.5 points ($350) | TP2/3: +32.5 points total (+$300)
    if side == "Buy":
        tp1 = entry + 17.5
        tp_final = entry + 32.5
        sl = entry - 15  # 15 point Stop Loss
    else:
        tp1 = entry - 17.5
        tp_final = entry - 32.5
        sl = entry + 15

    msg = (
        f"🚀 *{side} SIGNAL: {ticker}*\n"
        f"📍 Entry: {entry}\n\n"
        f"🎯 TP 1: {tp1:.2f} (+$350)\n"
        f"🎯 TP 2/3: {tp_final:.2f} (+$300)\n"
        f"🛑 Stop Loss: {sl:.2f}\n\n"
        f"💰 *Total Potential: $650*"
    )
    
    send_telegram(msg)
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)