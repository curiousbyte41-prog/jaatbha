#!/usr/bin/env python3
import requests
import sys
import json
import random
import string

def check_card(card):
    try:
        cc, mm, yy, cvv = card.split('|')
        if len(yy) == 2:
            yy = '20' + yy
            
        email = ''.join(random.choices(string.ascii_lowercase, k=10)) + "@gmail.com"
        
        session = requests.Session()
        
        # Create order
        order_url = "https://api.paypal.com/v2/checkout/orders"
        order_headers = {
            'Authorization': 'Bearer access_token',
            'Content-Type': 'application/json'
        }
        order_data = {
            'intent': 'CAPTURE',
            'purchase_units': [{
                'amount': {
                    'currency_code': 'USD',
                    'value': '1.00'
                }
            }]
        }
        
        order_response = session.post(order_url, json=order_data, headers=order_headers, timeout=15)
        order = order_response.json()
        order_id = order.get('id')
        
        if not order_id:
            return {"status": "DEAD", "msg": "Order failed"}
        
        # Submit payment
        payment_url = f"https://api.paypal.com/v2/checkout/orders/{order_id}/capture"
        payment_data = {
            'payment_source': {
                'card': {
                    'number': cc,
                    'expiry': f"{mm}/{yy}",
                    'security_code': cvv,
                    'name': 'Test User'
                }
            }
        }
        
        payment_response = session.post(payment_url, json=payment_data, headers=order_headers, timeout=15)
        
        if payment_response.status_code == 201:
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
