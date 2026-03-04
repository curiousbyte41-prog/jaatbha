#!/usr/bin/env python3
import requests
import sys
import json

def check_card(card):
    try:
        cc, mm, yy, cvv = card.split('|')
        if len(yy) == 2:
            yy = '20' + yy
            
        session = requests.Session()
        
        # Create order
        order_url = "https://api.razorpay.com/v1/orders"
        auth = ('rzp_live_key', 'rzp_live_secret')
        order_data = {
            'amount': 100,
            'currency': 'INR',
            'receipt': 'receipt_1'
        }
        
        order_response = session.post(order_url, auth=auth, data=order_data, timeout=15)
        order = order_response.json()
        order_id = order.get('id')
        
        if not order_id:
            return {"status": "DEAD", "msg": "Order failed"}
        
        # Capture payment
        capture_url = f"https://api.razorpay.com/v1/payments/create/axios"
        capture_data = {
            'order_id': order_id,
            'card[number]': cc,
            'card[expiry_month]': mm,
            'card[expiry_year]': yy,
            'card[cvv]': cvv,
            'card[name]': 'Test User'
        }
        
        capture_response = session.post(capture_url, auth=auth, data=capture_data, timeout=15)
        
        if capture_response.status_code == 200:
            return {"status": "LIVE", "msg": "Charged"}
        else:
            return {"status": "DEAD", "msg": "Declined"}
            
    except Exception as e:
        return {"status": "DEAD", "msg": str(e)}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"status": "DEAD", "msg": "No card"}))
        sys.exit(1)
    
    result = check_card(sys.argv[1])
    print(json.dumps(result))
