from flask import Flask, jsonify
import requests
import time
import json

app = Flask(__name__)

LOCAL_URL = "https://livechannelmm.com/1883/local-data.txt"
MARKET_URL = "https://livechannelmm.com/1883/marketdata.txt"

@app.route('/api/live')
def get_live():
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        res_local = requests.get(LOCAL_URL, headers=headers, timeout=5).text.strip()
        res_market = requests.get(MARKET_URL, headers=headers, timeout=5).text.strip()
        
        # ၁။ Market Data ပိုင်း
        try:
            m_raw = json.loads(res_market)
            combined_twod = str(m_raw.get('mm2d1', '')) + str(m_raw.get('mm2d2', ''))
            market_data = {
                "set": m_raw.get('set', '--'),
                "val": m_raw.get('val', '--'),
                "twod": combined_twod if combined_twod else "--",
                "updated": m_raw.get('updated', '--')
            }
        except:
            market_data = {"raw": res_market}

        # ၂။ Results ပိုင်း (12:00 PM ကို ဖယ်ထုတ်ပြီး ချိန်ညှိခြင်း)
        history_list = []
        rows = res_local.split('\n')
        for row in rows:
            parts = row.split(',')
            if any(x in row for x in ["AM", "PM"]):
                t_val = parts[0].strip()
                
                # ၁၂:၀၀ PM ကို လုံးဝကျော်သွားမယ် (Skip line)
                if t_val == "12:00 PM":
                    continue
                
                # သတ်မှတ်ထားတဲ့ အချိန်တွေအတွက်ပဲ Data ထည့်မယ်
                item = {"time": t_val}
                
                # ၁၂:၀၁ PM နဲ့ ၄:၃၀ PM အတွက် twod ပဲပြမယ်
                if t_val == "12:01 PM" or t_val == "4:30 PM":
                    item["twod"] = parts[1].strip() if len(parts) > 1 else "--"
                    history_list.append(item)
                
                # ၉:၃၀ AM နဲ့ ၂:၀၀ PM အတွက် modern နဲ့ internet ပဲပြမယ်
                elif t_val == "9:30 AM" or t_val == "2:00 PM":
                    item["modern"] = parts[2].strip() if len(parts) > 2 else "--"
                    item["internet"] = parts[3].strip() if len(parts) > 3 else "--"
                    history_list.append(item)

        return jsonify({
            "success": True,
            "server_time": time.strftime("%H:%M:%S"),
            "market": market_data,
            "results": history_list
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run()
    
