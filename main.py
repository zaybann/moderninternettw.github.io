from flask import Flask, jsonify
import requests
import time
import json

app = Flask(__name__)

LOCAL_URL = "https://livechannelmm.com/1883/local-data.txt"
MARKET_URL = "https://livechannelmm.com/1883/marketdata.txt"

@app.route('/')
def home():
    return jsonify({"status": "active", "info": "Lucky Boss 556 API"})

@app.route('/api/live')
def get_live():
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        # ၁။ Data ဆွဲယူခြင်း
        res_local = requests.get(LOCAL_URL, headers=headers, timeout=5).text.strip()
        res_market = requests.get(MARKET_URL, headers=headers, timeout=5).text.strip()
        
        # ၂။ Market Data ကို ပြင်ဆင်ခြင်း
        try:
            m_raw = json.loads(res_market)
            # mm2d1 နဲ့ mm2d2 ကို ပေါင်းပြီး twod အသစ်တစ်ခု ဆောက်မယ်
            # string အနေနဲ့ ပေါင်းမှာမို့လို့ "1" + "0" = "10" ဖြစ်သွားပါမယ်
            combined_twod = str(m_raw.get('mm2d1', '')) + str(m_raw.get('mm2d2', ''))
            
            market_data = {
                "set": m_raw.get('set'),
                "val": m_raw.get('val'),
                "twod": combined_twod if combined_twod else "--", # ပေါင်းထားသော ဂဏန်း
                "updated": m_raw.get('updated')
            }
        except:
            market_data = {"raw": res_market}

        # ၃။ Local History Data ကို ပြင်ဆင်ခြင်း
        history_list = []
        rows = res_local.split('\n')
        for row in rows:
            parts = row.split(',')
            if any(x in row for x in ["AM", "PM"]):
                history_list.append({
                    "time": parts[0].strip(),
                    "twod": parts[1].strip() if len(parts) > 1 else "--",
                    "modern": parts[2].strip() if len(parts) > 2 else "--",
                    "internet": parts[3].strip() if len(parts) > 3 else "--"
                })

        # ၄။ API Output
        return jsonify({
            "success": True,
            "server_time": time.strftime("%H:%M:%S"),
            "market": market_data, # ဒီထဲမှာ mm2d1, mm2d2 မပါတော့ဘဲ twod ပဲ ပါပါတော့မယ်
            "results": history_list
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run()

