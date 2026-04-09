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

        # ၂။ Results ပိုင်း (Logic အသစ်ဖြင့် ပြင်ဆင်ခြင်း)
        history_list = []
        rows = res_local.split('\n')
        for row in rows:
            parts = row.split(',')
            if any(x in row for x in ["AM", "PM"]):
                t_val = parts[0].strip()
                
                # အခြေအနေအလိုက် Data Structure ကို ပြောင်းလဲခြင်း
                item = {"time": t_val}
                
                # ၁၂ နာရီ နဲ့ ၄ နာရီခွဲဆိုရင် twod ပဲ ထည့်မယ်
                if "12:01 PM" in t_val or "4:30 PM" in t_val:
                    item["twod"] = parts[1].strip() if len(parts) > 1 else "--"
                
                # ၉ နာရီခွဲ နဲ့ ၂ နာရီ ဆိုရင် modern နဲ့ internet ပဲ ထည့်မယ်
                elif "9:30 AM" in t_val or "2:00 PM" in t_val:
                    item["modern"] = parts[2].strip() if len(parts) > 2 else "--"
                    item["internet"] = parts[3].strip() if len(parts) > 3 else "--"
                
                # တခြားအချိန်တွေရှိရင် (ဥပမာ 12:00 PM) အကုန်ပြချင်ရင် ဒီမှာ ထပ်တိုးလို့ရပါတယ်
                # အခုလောလောဆယ် သင်ပေးထားတဲ့ logic အတိုင်းပဲ စစ်ထားပါတယ်
                else:
                    continue # သင်မပြထားတဲ့ 12:00 PM လိုမျိုးကို ဖယ်ထုတ်လိုက်တာပါ

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

