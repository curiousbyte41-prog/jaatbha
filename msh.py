#!/usr/bin/env python3
import requests
import sys
import json
import re
import random

def check_card(card):
    try:
        cc, mm, yy, cvv = card.split('|')
        if len(yy) == 2:
            yy = '20' + yy
            
        sites = [
            "naturallclub.com",
            "brittnetta.com", 
            "brunekitchen.com",
            "brightland.co"
        ]
        
        site = random.choice(sites)
        session = requests.Session()
        
        # Add to cart
        cart_data = {
            'id': random.choice(['123456', '789012']),
            'quantity': '1'
        }
        session.post(f"https://{site}/cart/add.js", json=cart_data, timeout=10)
        
        # Get checkout
        checkout = session.get(f"https://{site}/checkout", timeout=10)
        
        # Check for token
        token_match = re.search(r'checkout_token[:\s]+["\']([^"\']+)["\']', checkout.text)
        
        if token_match:
            return {"status": "LIVE", "msg": "Processed"}
        else:
            return {"status": "DEAD", "msg": "No token"}
        
    except Exception as e:
        return {"status": "DEAD", "msg": str(e)}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"status": "DEAD", "msg": "No card"}))
        sys.exit(1)
    
    result = check_card(sys.argv[1])
    print(json.dumps(result))
