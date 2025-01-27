import random
import string
import time
import os

# Terminal color codes
rd, gn, lgn, yw, lrd, be, pe = '\033[00;31m', '\033[00;32m', '\033[01;32m', '\033[01;33m', '\033[01;31m', '\033[94m', '\033[01;35m'
cn, k, g = '\033[00;36m', '\033[90m', '\033[38;5;130m'
true = f'{rd}[{lgn}+{rd}]{gn} '
false = f'{rd}[{lrd}-{rd}] '

# Try importing names library, install if it fails
try:
    import names
except ImportError:
    os.system("pip install names")

import requests

# Set up proxy
proxies = {
    'http': 'http://92mmt5g8:DiHFv6FWO56n@103.157.205.53:3192',
    'https': 'http://92mmt5g8:DiHFv6FWO56n@103.157.205.53:3192',
}

def get_headers(Country, Language):
    while True:
        try:
            an_agent = f'Mozilla/5.0 (Linux; Android {random.randint(9,13)}; {"".join(random.choices(string.ascii_uppercase, k=3))}{random.randint(111,999)}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36'
            
            res = requests.get("https://www.facebook.com/", headers={'user-agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}, proxies=proxies, timeout=30)

            print("Facebook Response Text:", res.text)  # Debug print

            parts = res.text.split('["_js_datr","')
            if len(parts) > 1:
                js_datr = parts[1].split('",')[0]
            else:
                print("Expected format not found in Facebook response.")
                js_datr = None  # Handle accordingly

            r = requests.get('https://www.instagram.com/api/v1/web/accounts/login/ajax/', headers={'user-agent': an_agent}, proxies=proxies, timeout=30).cookies

            headers1 = {
                'authority': 'www.instagram.com',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': f'{Language}-{Country},en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
                'cookie': f'dpr=3; csrftoken={r["csrftoken"]}; mid={r["mid"]}; ig_nrcb=1; ig_did={r["ig_did"]}; datr={js_datr}',
                'sec-ch-prefers-color-scheme': 'light',
                'sec-ch-ua': '"Chromium";v="111", "Not(A:Brand";v="8"',
                'sec-ch-ua-mobile': '?1',
                'sec-ch-ua-platform': '"Android"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'none',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': an_agent,
                'viewport-width': '980',
            }
            return headers1
        except Exception as E:
            print(f'{false}Error in Connection: {E}')

def Get_UserName(Headers, Name, Email):
    try:
        updict = {"referer": 'https://www.instagram.com/accounts/signup/birthday/'}
        Headers = {key: updict.get(key, Headers[key]) for key in Headers}
        while True:
            data = {
                'email': Email,
                'name': Name + str(random.randint(1, 99)),
            }

            response = requests.post(
                'https://www.instagram.com/api/v1/web/accounts/username_suggestions/',
                headers=Headers,
                data=data,
                proxies=proxies,
                timeout=30
            )
            if 'status":"fail' in response.text:
                print(response.text)
            elif 'status":"ok' in response.text:
                return random.choice(response.json()['suggestions'])
            else:
                print(response.text)

    except Exception as E:
        print(f'{false}Error in Set Username! Exception: {E}')

def Send_SMS(Headers, Email):
    try:
        data = {
            'device_id': Headers['cookie'].split('mid=')[1].split(';')[0],
            'email': Email,
        }

        response = requests.post(
            'https://www.instagram.com/api/v1/accounts/send_verify_email/',
            headers=Headers,
            data=data,
            proxies=proxies,
            timeout=30
        )
        return response.text
    except Exception as E:
        print(f'{false}Error In Send Code! Exception: {E}')

def Validate_Code(Headers, Email, Code):
    try:
        updict = {"referer": 'https://www.instagram.com/accounts/signup/emailConfirmation/'}
        Headers = {key: updict.get(key, Headers[key]) for key in Headers}

        data = {
            'code': Code,
            'device_id': Headers['cookie'].split('mid=')[1].split(';')[0],
            'email': Email,
        }

        response = requests.post(
            'https://www.instagram.com/api/v1/accounts/check_confirmation_code/',
            headers=Headers,
            data=data,
            proxies=proxies,
            timeout=30
        )
        return response
    except Exception as E:
        print(f'{false}Invalid Code. Exception: {E}')

def Create_Acc(Headers, Email, SignUpCode):
    try:
        firstname = names.get_first_name()
        UserName = Get_UserName(Headers, firstname, Email)
        Password = firstname.strip() + '@' + str(random.randint(111, 999))

        updict = {"referer": 'https://www.instagram.com/accounts/signup/username/'}
        Headers = {key: updict.get(key, Headers[key]) for key in Headers}

        data = {
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{round(time.time())}:{Password}',
            'email': Email,
            'username': UserName,
            'first_name': firstname,
            'month': random.randint(1, 12),
            'day': random.randint(1, 28),
            'year': random.randint(1990, 2001),
            'client_id': Headers['cookie'].split('mid=')[1].split(';')[0],
            'seamless_login_enabled': '1',
            'tos_version': 'row',
            'force_sign_up_code': SignUpCode,
        }

        response = requests.post(
            'https://www.instagram.com/api/v1/web/accounts/web_create_ajax/',
            headers=Headers,
            data=data,
            proxies=proxies,
            timeout=30
        )
        if '"account_created":true' in response.text:
            print(f'''{true}UserName: {UserName}\n{true}PassWord :{Password}\n{true}Sessionid : {response.cookies['sessionid']}\n{true}Csrftoken : {response.cookies['csrftoken']}\n{true}Ds_user_id : {response.cookies['ds_user_id']}\n{true}Ig_did : {response.cookies['ig_did']}\n{true}Rur : {response.cookies['rur']}\n{true}Mid : {Headers['cookie'].split('mid=')[1].split(';')[0]}\n{true}Datr : {Headers['cookie'].split('datr=')[1]}''')            
        else:
            print(f'{false}Failed to create account. Response: {response.text}')
    except Exception as E:
        print(f'{false}Error in Create Account! Exception: {E}')

# Clear terminal
if os.name == "nt":  # Windows
    os.system("cls")
else:  # Unix/Linux
    os.system("clear")

# Display welcome message
print(f"""{gn}
 _____   _____          __  __         _                
|_   _| / ____|        |  \/  |       | |               
  | |  | |  __  ______ | \  / |  __ _ | | __  ___  _ __ 
  | |  | | |_ ||______|| |\/| | / _` || |/ / / _ \| '__|
 _| |_ | |__| |        | |  | || (_| ||   < |  __/| |   
|_____| \_____|        |_|  |_| \__,_||_|\_\ \___||_|   
       
       Account Creator Instagram
""")

# Main flow
headers = get_headers(Country='US', Language='en')
Email = input(f'{true}Enter Your Email: ')
SignUpCode = input(f'{true}Enter Sign Up Code (0 or 1): ')
Create_Acc(headers, Email, SignUpCode)
        
