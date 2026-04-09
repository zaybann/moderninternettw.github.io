from flask import Flask, jsonify
import requests
import time

app = Flask(__name__)

LOCAL_URL = "https://livechannelmm.com/1883/local-data.txt"
MARKET_URL = "https://livechannelmm.com/1883/marketdata.txt"

@app.route('/')
def dashboard():
    # ဒီ Route က Browser မှာကြည့်ရင် Dashboard ပုံစံ မြင်ရအောင်လုပ်ပေးမှာပါ
    return "🚀 Lucky Boss 556 API is Online! <br> Go to /api/live to see data."

@app.route('/api/live')
def get_live_data():
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        # ၁။ Data ဆွဲယူခြင်း
        res1 = requests.get(LOCAL_URL, headers=headers, timeout=5).text.strip()
        res2 = requests.get(MARKET_URL, headers=headers, timeout=5).text.strip()
        current_time = time.strftime("%H:%M:%S")

        # ၂။ JSON အဖြစ် ပြောင်းလဲခြင်း
        return jsonify({
            "title": "Lucky Boss 556 - Real-time Data",
            "update_time": current_time,
            "market_data": res2,
            "local_data_raw": res1
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    app.run()
  
