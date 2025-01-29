import random
import string
import time
import os
import requests

# Color codes for terminal output
rd, gn, lgn, yw, lrd, be, pe = '\033[00;31m', '\033[00;32m', '\033[01;32m', '\033[01;33m', '\033[01;31m', '\033[94m', '\033[01;35m'
cn, k, g = '\033[00;36m', '\033[90m', '\033[38;5;130m'
true = f'{rd}[{lgn}+{rd}]{gn} '
false = f'{rd}[{lrd}-{rd}] '

# Proxy configuration
proxies = {
    "http": "http://username:password@na.f15df02e5d366174.abcproxy.vip:4950",
    "https": "http://username:password@na.f15df02e5d366174.abcproxy.vip:4950",
}

# Check for the 'names' package, if not found, install it
try:
    import names
except ImportError:
    os.system("pip install names")

def get_headers(Country, Language):
    while True:
        try:
            an_agent = f'Mozilla/5.0 (Linux; Android {random.randint(9, 13)}; {"".join(random.choices(string.ascii_uppercase, k=3))}{random.randint(111, 999)}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36'
            res = requests.get("https://www.instagram.com/", headers={'user-agent': an_agent}, proxies=proxies, timeout=30)

            if res.status_code != 200:
                print(f'{false}Error: Unable to connect to Instagram. Status code: {res.status_code}')
                continue
            
            js_datr = res.text.split('["_js_datr","')[1].split('",')[0]
            r = requests.get('https://www.instagram.com/api/v1/web/accounts/login/ajax/', headers={'user-agent': an_agent}, proxies=proxies, timeout=30).cookies

            if 'csrftoken' not in r or 'mid' not in r or 'ig_did' not in r:
                print(f'{false}Error: Missing required cookies. Response cookies: {r}')
                continue

            headers1 = {
                'authority': 'www.instagram.com',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': f'{Language}-{Country},en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
                'cookie': f'dpr=3; csrftoken={r["csrftoken"]}; mid={r["mid"]}; ig_nrcb=1; ig_did={r["ig_did"]}; datr={js_datr}',
                'user-agent': an_agent,
            }
            response1 = requests.get('https://www.instagram.com/', headers=headers1, proxies=proxies, timeout=30)

            appid = response1.text.split('APP_ID":"')[1].split('"')[0]
            rollout = response1.text.split('rollout_hash":"')[1].split('"')[0]

            headers = {
                'authority': 'www.instagram.com',
                'accept': '*/*',
                'accept-language': f'{Language}-{Country},en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
                'content-type': 'application/x-www-form-urlencoded',
                'cookie': f'dpr=3; csrftoken={r["csrftoken"]}; mid={r["mid"]}; ig_nrcb=1; ig_did={r["ig_did"]}; datr={js_datr}',
                'origin': 'https://www.instagram.com',
                'referer': 'https://www.instagram.com/accounts/signup/email/',
                'user-agent': an_agent,
                'x-asbd-id': '198387',
                'x-csrftoken': r["csrftoken"],
                'x-ig-app-id': str(appid),
                'x-instagram-ajax': str(rollout),
                'x-requested-with': 'XMLHttpRequest',
                'x-web-device-id': r["ig_did"],
            }
            return headers
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
        print(f'{false}Error in Set Username: {E}')

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
        print(f'{false}Error In Send Code: {E}')

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
        print(f'{false}Invalid Code: {E}')

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
            print(f'''{true}UserName: {UserName}\n{true}PassWord: {Password}\n{true}Sessionid: {response.cookies['sessionid']}\n{true}Csrftoken: {response.cookies['csrftoken']}\n{true}Ds_user_id: {response.cookies['ds_user_id']}\n{true}Ig_did: {response.cookies['ig_did']}\n{true}Rur: {response.cookies['rur']}\n{true}Mid: {Headers['cookie'].split('mid=')[1].split(';')[0]}\n{true}Datr: {Headers['cookie'].split('datr=')[1]}''')            
        else:
            print(f'{false}Account creation failed: {response.text}')
    except Exception as E:
        print(f'{false}Error in Create Account: {E}')

if __import__("platform").system() == "Windows":
    os.system("cls")
else:
    os.system("clear")
    
# Display a welcome message and tool information
print(f"""{gn}
 _____   _____          __  __         _                
|_   _| / ____|        |  \/  |       | |               
  | |  | (___    ___   | \  / |  __ _ | |_   ___   ___  
  | |   \___ \  / _ \  | |\/| | / _` || __| / _ \ / _ \ 
 _| |_  ____) || (_) | | |  | || (_| || |_ |  __/| (_) |
|_____| |_____/  \___/  |_|  |_| \__,_| \__| \___| \___/ 
                                                                                                                 
{yw}Instagram Account Creation Tool {gn}  
""")
print(f'{gn}~' * 65)

# Collect user input for email and sign-up code
Email = input(f'Enter Email: ').strip()  # Using .strip() to remove any extra spaces
SignUpCode = input(f'Enter SignUp Code: ').strip()

# Getting headers with the specified country and language
Headers = get_headers('US', 'en')

# Sending SMS verification code to the provided email
sms_response = Send_SMS(Headers, Email)

# Check if SMS was sent successfully
if sms_response:
    print(f'{true}Verification code sent to {Email}. Please check your inbox.')
else:
    print(f'{false}Failed to send verification code to {Email}. Please try again.')

# Wait for the user to enter the verification code
Code = input(f'Enter Verification Code: ').strip()

# Validate the entered code
validation_response = Validate_Code(Headers, Email, Code)

if validation_response and '"status":"ok"' in validation_response.text:
    print(f'{true}Verification code validated successfully.')
else:
    print(f'{false}Invalid verification code. Please check and try again.')
    exit(1)  # Exit the program if validation fails

# Proceed to create the account
Create_Acc(Headers, Email, SignUpCode)
