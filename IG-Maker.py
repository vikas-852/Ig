import random
import string
import time
import os
import requests

# Terminal colors for output formatting
rd, gn, lgn, yw, lrd, be, pe = '\033[00;31m', '\033[00;32m', '\033[01;32m', '\033[01;33m', '\033[01;31m', '\033[94m', '\033[01;35m'
cn, k, g = '\033[00;36m', '\033[90m', '\033[38;5;130m'
true = f'{rd}[{lgn}+{rd}]{gn} '
false = f'{rd}[{lrd}-{rd}] '

# List of working proxies
proxy_list = [
    "http://2aa31SFEZZ-zone-abc-region-US-session-dyMzb3XA-sessTime-1:48665630@na.f15df02e5d366174.abcproxy.vip:4950",
    "http://2aa31SFEZZ-zone-abc-region-US-session-jrNjdJYQ-sessTime-1:48665630@na.f15df02e5d366174.abcproxy.vip:4950",
    "http://2aa31SFEZZ-zone-abc-region-US-session-YXySsKQZ-sessTime-1:48665630@na.f15df02e5d366174.abcproxy.vip:4950",
    "http://2aa31SFEZZ-zone-abc-region-US-session-TNfashC5-sessTime-1:48665630@na.f15df02e5d366174.abcproxy.vip:4950",
    "http://2aa31SFEZZ-zone-abc-region-US-session-KdwM8HQx-sessTime-1:48665630@na.f15df02e5d366174.abcproxy.vip:4950",
    "http://2aa31SFEZZ-zone-abc-region-US-session-ypwdkEpG-sessTime-1:48665630@na.f15df02e5d366174.abcproxy.vip:4950",
    "http://2aa31SFEZZ-zone-abc-region-US-session-kt4y3d8s-sessTime-1:48665630@na.f15df02e5d366174.abcproxy.vip:4950",
    "http://2aa31SFEZZ-zone-abc-region-US-session-GSF82bBd-sessTime-1:48665630@na.f15df02e5d366174.abcproxy.vip:4950",
    "http://2aa31SFEZZ-zone-abc-region-US-session-wTi24MYe-sessTime-1:48665630@na.f15df02e5d366174.abcproxy.vip:4950",
    "http://2aa31SFEZZ-zone-abc-region-US-session-yHQ5Kaen-sessTime-1:48665630@na.f15df02e5d366174.abcproxy.vip:4950"
]

# Function to get a random proxy
def get_proxy():
    return random.choice(proxy_list)

# Function to send a request with a proxy and retry if needed
def send_request(url, headers=None, max_retries=3):
    for attempt in range(max_retries):
        proxy = get_proxy()
        proxies = {"http": proxy, "https": proxy}
        print(f"{true}Using proxy: {proxy}")

        try:
            response = requests.get(url, headers=headers, proxies=proxies, timeout=10)
            response.raise_for_status()
            return response  # Return response if successful
        except requests.exceptions.RequestException as e:
            print(f"{false}Error with proxy {proxy}: {e}")
            time.sleep(2)  # Wait before retrying

    print(f"{false}All proxies failed after {max_retries} attempts.")
    return None

# Function to generate headers for Instagram requests
def get_headers():
    an_agent = f'Mozilla/5.0 (Linux; Android {random.randint(9,13)}; {"".join(random.choices(string.ascii_uppercase, k=3))}{random.randint(111,999)}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36'
    
    response = send_request("https://www.instagram.com/")
    if response:
        appid = response.text.split('APP_ID":"')[1].split('"')[0]
        rollout = response.text.split('rollout_hash":"')[1].split('"')[0]

        headers = {
            'authority': 'www.instagram.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://www.instagram.com',
            'referer': 'https://www.instagram.com/accounts/signup/',
            'sec-ch-ua': '"Chromium";v="111", "Not(A:Brand";v="8"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': an_agent,
            'x-asbd-id': '198387',
            'x-ig-app-id': str(appid),
            'x-ig-www-claim': '0',
            'x-instagram-ajax': str(rollout),
            'x-requested-with': 'XMLHttpRequest',
        }
        return headers
    return None

# Function to send email verification code
def send_sms(headers, email):
    data = {'email': email}
    response = send_request("https://www.instagram.com/api/v1/accounts/send_verify_email/", headers=headers)
    if response and 'email_sent":true' in response.text:
        return True
    return False

# Function to validate the code sent to email
def validate_code(headers, email, code):
    data = {'code': code, 'email': email}
    response = send_request("https://www.instagram.com/api/v1/accounts/check_confirmation_code/", headers=headers)
    if response and 'status":"ok' in response.text:
        return response.json().get('signup_code')
    return None

# Function to create an Instagram account
def create_account(headers, email, signup_code):
    first_name = ''.join(random.choices(string.ascii_lowercase, k=8)).capitalize()
    username = first_name + str(random.randint(100, 999))
    password = first_name + '@' + str(random.randint(111,999))

    data = {
        'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{round(time.time())}:{password}',
        'email': email,
        'username': username,
        'first_name': first_name,
        'month': random.randint(1,12),
        'day': random.randint(1,28),
        'year': random.randint(1990,2001),
        'seamless_login_enabled': '1',
        'tos_version': 'row',
        'force_sign_up_code': signup_code,
    }

    response = send_request("https://www.instagram.com/api/v1/web/accounts/web_create_ajax/", headers=headers)
    if response and '"account_created":true' in response.text:
        print(f"{true}Account created successfully!")
        print(f"{true}Username: {username}")
        print(f"{true}Password: {password}")
    else:
        print(f"{false}Account creation failed!")

# Main execution
if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    
    print(f"{gn}Instagram Account Creator\n")
    email = input(f"{true}Enter Your Email: {cn}")
    
    headers = get_headers()
    if headers and send_sms(headers, email):
        code = input(f"\n{true}Enter Verification Code: {cn}")
        signup_code = validate_code(headers, email, code)
        
        if signup_code:
            create_account(headers, email, signup_code)
        else:
            print(f"{false}Invalid code!")
    else:
        print(f"{false}Failed to send verification email!")
    
