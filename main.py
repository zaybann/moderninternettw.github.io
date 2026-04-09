from flask import Flask, jsonify
import requests
import time
import json

app = Flask(__name__)

# API Sources
LOCAL_URL = "https://livechannelmm.com/1883/local-data.txt"
MARKET_URL = "https://livechannelmm.com/1883/marketdata.txt"

@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "message": "Lucky Boss 556 API is running. Use /api/live for data."
    })

@app.route('/api/live')
def get_live():
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        # ၁။ Data ဆွဲယူခြင်း
        res_local = requests.get(LOCAL_URL, headers=headers, timeout=5).text.strip()
        res_market = requests.get(MARKET_URL, headers=headers, timeout=5).text.strip()
        
        # ၂။ Market Data ကို JSON သန့်စင်ခြင်း
        try:
            market_data = json.loads(res_market)
        except:
            market_data = {"raw": res_market}

        # ၃။ Local Data ကို Structured JSON (List) ပြောင်းခြင်း
        # စာသားအကြမ်းတွေကို တစ်ကြောင်းချင်းစီခွဲပြီး key တွေနဲ့ သတ်မှတ်ပေးမယ်
        history_list = []
        rows = res_local.split('\n')
        for row in rows:
            parts = row.split(',')
            # အချိန် (AM/PM) ပါတဲ့ စာကြောင်းတွေကိုပဲ စစ်ထုတ်ယူမယ်
            if any(x in row for x in ["AM", "PM"]):
                history_list.append({
                    "time": parts[0].strip(),
                    "twod": parts[1].strip() if len(parts) > 1 else "--",
                    "modern": parts[2].strip() if len(parts) > 2 else "--",
                    "internet": parts[3].strip() if len(parts) > 3 else "--",
                    "key": parts[4].strip() if len(parts) > 4 else "--"
                })

        # ၄။ API Response ထုတ်ပေးခြင်း
        return jsonify({
            "success": True,
            "api_version": "1.0",
            "server_time": time.strftime("%H:%M:%S"),
            "market": market_data,
            "results": history_list
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error_message": str(e)
        }), 500

if __name__ == "__main__":
    app.run()
