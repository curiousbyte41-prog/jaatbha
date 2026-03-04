#!/usr/bin/env python3
import requests
import sys
import json

def check_card(card):
    try:
        cc, mm, yy, cvv = card.split('|')
        if len(yy) == 2:
            yy = '20' + yy
            
        url = "https://api.stripe.com/v1/charges"
        headers = {
            'Authorization': 'Bearer sk_live_xxx',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'amount': 50,
            'currency': 'usd',
            'source[object]': 'card',
            'source[number]': cc,
            'source[exp_month]': mm,
            'source[exp_year]': yy,
            'source[cvc]': cvv
        }
        
        response = requests.post(url, data=data, headers=headers, timeout=15)
        result = response.json()
        
        if 'id' in result:
            return {"status": "LIVE", "msg": "Charged"}
        else:
            error = result.get('error', {}).get('message', 'Declined')
            if 'insufficient_funds' in error:
                return {"status": "LIVE", "msg": "Insufficient Funds"}
            return {"status": "DEAD", "msg": error}
            
    except Exception as e:
        return {"status": "DEAD", "msg": str(e)}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"status": "DEAD", "msg": "No card"}))
        sys.exit(1)
    
    result = check_card(sys.argv[1])
    print(json.dumps(result))
