from flask import Flask, jsonify
import requests
from datetime import datetime, timedelta
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
        
        # ၁။ Market Data ကို "live" key အဖြစ် ပြင်ဆင်ခြင်း
        try:
            m_raw = json.loads(res_market)
            combined_twod = str(m_raw.get('mm2d1', '')) + str(m_raw.get('mm2d2', ''))
            live_data = {
                "set": m_raw.get('set', '--'),
                "val": m_raw.get('val', '--'),
                "twod": combined_twod if combined_twod else "--",
                "updated": m_raw.get('updated', '--')
            }
        except:
            live_data = {"raw": res_market}

        # ၂။ Results ပိုင်း (Logic အတိုင်း သန့်စင်ခြင်း)
        history_list = []
        rows = res_local.split('\n')
        for row in rows:
            parts = row.split(',')
            if any(x in row for x in ["AM", "PM"]):
                t_val = parts[0].strip()
                
                if t_val == "12:00 PM":
                    continue
                
                # ၁၂:၀၁ PM နဲ့ ၄:၃၀ PM (Time + Twod)
                if t_val == "12:01 PM" or t_val == "4:30 PM":
                    history_list.append({
                        "time": t_val,
                        "twod": parts[1].strip() if len(parts) > 1 else "--"
                    })
                
                # ၉:၃၀ AM နဲ့ ၂:၀၀ PM (Time + Modern + Internet)
                elif t_val == "9:30 AM" or t_val == "2:00 PM":
                    history_list.append({
                        "time": t_val,
                        "modern": parts[2].strip() if len(parts) > 2 else "--",
                        "internet": parts[3].strip() if len(parts) > 3 else "--"
                    })

        # ၃။ ထိုင်းစံတော်ချိန် (GMT+7) တွက်ချက်ခြင်း
        # Vercel Server က UTC သုံးတတ်လို့ ၇ နာရီ ပေါင်းပေးရပါမယ်
        thailand_time = datetime.utcnow() + timedelta(hours=7)
        formatted_time = thailand_time.strftime("%H:%M:%S")

        # ၄။ JSON Output (သင့် Format အတိုင်း အတိအကျ)
        return jsonify({
            "live": live_data,
            "results": history_list,
            "server_time": formatted_time,
            "success": True
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run()
    
