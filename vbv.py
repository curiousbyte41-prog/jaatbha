#!/usr/bin/env python3
import requests
import sys
import json

def check_card(card):
    try:
        cc, mm, yy, cvv = card.split('|')
        bin_num = cc[:6]
        
        url = f"https://lookup.binlist.net/{bin_num}"
        headers = {'Accept-Version': '3'}
        
        response = requests.get(url, headers=headers, timeout=10)
        bin_data = response.json()
        
        # Check if 3DS enabled (simplified logic)
        country = bin_data.get('country', {}).get('alpha2', 'US')
        
        # Countries with high 3DS probability
        high_3ds = ['GB', 'FR', 'DE', 'ES', 'IT', 'NL', 'BR', 'IN']
        
        if country in high_3ds:
            return {"status": "LIVE", "msg": "3DS Enabled"}
        else:
            return {"status": "DEAD", "msg": "Non 3DS"}
            
    except Exception as e:
        return {"status": "DEAD", "msg": str(e)}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"status": "DEAD", "msg": "No card"}))
        sys.exit(1)
    
    result = check_card(sys.argv[1])
    print(json.dumps(result))
