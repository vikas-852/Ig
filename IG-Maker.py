import random
import string
import time
import os
import requests

try:
    import names
except ImportError:
    os.system("pip install names")

# Terminal color codes
rd, gn, lgn, yw, lrd, be, pe = '\033[00;31m', '\033[00;32m', '\033[01;32m', '\033[01;33m', '\033[01;31m', '\033[94m', '\033[01;35m'
cn, k, g = '\033[00;36m', '\033[90m', '\033[38;5;130m'
true = f'{rd}[{lgn}+{rd}]{gn} '
false = f'{rd}[{lrd}-{rd}] '

# Proxy settings
proxies = {
    'http': 'http://92mmt5g8:DiHFv6FWO56n@103.157.205.53:3192'
}

def get_headers(Country, Language):
    """
    Generate and return headers for requests to Instagram.
    """
    while True:
        try:
            user_agent = f'Mozilla/5.0 (Linux; Android {random.randint(9, 13)}; {"".join(random.choices(string.ascii_uppercase, k=3))}{random.randint(111, 999)}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36'

            # Request Facebook to extract the required js_datr value
            res = requests.get("https://www.facebook.com/", headers={'user-agent': user_agent}, proxies=proxies, timeout=30)
            res.raise_for_status()

            # Extract js_datr safely
            if '["_js_datr","' in res.text:
                js_datr = res.text.split('["_js_datr","')[1].split('",')[0]
            else:
                print(f"{false}Unable to find js_datr in the response from Facebook.")
                return None

            # Get Instagram cookies
            ig_response = requests.get('https://www.instagram.com/api/v1/web/accounts/login/ajax/',
                                       headers={'user-agent': user_agent},
                                       proxies=proxies,
                                       timeout=30)
            ig_response.raise_for_status()
            cookies = ig_response.cookies

            # Return the headers
            headers = {
                'authority': 'www.instagram.com',
                'accept': '*/*',
                'accept-language': f'{Language}-{Country},en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
                'user-agent': user_agent,
                'cookie': f'dpr=3; csrftoken={cookies["csrftoken"]}; mid={cookies["mid"]}; ig_nrcb=1; ig_did={cookies["ig_did"]}; datr={js_datr}',
                'x-csrftoken': cookies["csrftoken"],
                'x-ig-app-id': '936619743392459',
            }
            return headers
        except requests.exceptions.RequestException as e:
            print(f"{false}Request error: {e}")
        except Exception as e:
            print(f"{false}Unexpected error: {e}")
        time.sleep(5)  # Retry after a delay

def send_sms(headers, email):
    """
    Send verification code to the provided email.
    """
    try:
        data = {
            'device_id': headers['cookie'].split('mid=')[1].split(';')[0],
            'email': email,
        }

        response = requests.post(
            'https://www.instagram.com/api/v1/accounts/send_verify_email/',
            headers=headers,
            data=data,
            proxies=proxies,
            timeout=30
        )
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"{false}Error sending verification email: {e}")
    except Exception as e:
        print(f"{false}Unexpected error: {e}")

def validate_code(headers, email, code):
    """
    Validate the code sent to the email.
    """
    try:
        data = {
            'code': code,
            'device_id': headers['cookie'].split('mid=')[1].split(';')[0],
            'email': email,
        }

        response = requests.post(
            'https://www.instagram.com/api/v1/accounts/check_confirmation_code/',
            headers=headers,
            data=data,
            proxies=proxies,
            timeout=30
        )
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"{false}Error validating code: {e}")
    except Exception as e:
        print(f"{false}Unexpected error: {e}")

def create_account(headers, email, signup_code):
    """
    Create an Instagram account.
    """
    try:
        first_name = names.get_first_name()
        password = first_name + '@' + str(random.randint(111, 999))

        data = {
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{round(time.time())}:{password}',
            'email': email,
            'username': first_name + str(random.randint(1, 99)),
            'first_name': first_name,
            'month': random.randint(1, 12),
            'day': random.randint(1, 28),
            'year': random.randint(1990, 2001),
            'client_id': headers['cookie'].split('mid=')[1].split(';')[0],
            'seamless_login_enabled': '1',
            'tos_version': 'row',
            'force_sign_up_code': signup_code,
        }

        response = requests.post(
            'https://www.instagram.com/api/v1/web/accounts/web_create_ajax/',
            headers=headers,
            data=data,
            proxies=proxies,
            timeout=30
        )
        response.raise_for_status()

        if '"account_created":true' in response.text:
            print(f"{true}Account Created Successfully!")
            print(f"{true}Username: {data['username']}")
            print(f"{true}Password: {password}")
        else:
            print(f"{false}Failed to create account. Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"{false}Error creating account: {e}")
    except Exception as e:
        print(f"{false}Unexpected error: {e}")

# Main script
if __name__ == "__main__":
    if os.name == 'nt':
        os.system("cls")
    else:
        os.system("clear")

    print(f"""{gn}
    _____   _____          __  __         _                
    |_   _| / ____|        |  \/  |       | |               
      | |  | |  __  ______ | \  / |  __ _ | | __  ___  _ __ 
      | |  | | |_ ||______|| |\/| | / _` || |/ / / _ \| '__|
     _| |_ | |__| |        | |  | || (_| ||   < |  __/| |   
    |_____| \_____|        |_|  |_| \__,_||_|\_\ \___||_|   
    
    Instagram Account Creator
    """)

    headers = get_headers(Country='US', Language='en')
    if headers:
        email = input(f"{true}Enter Your Email: {cn}")
        sms_response = send_sms(headers, email)

        if 'email_sent":true' in sms_response:
            print(f"{true}Verification email sent!")
            code = input(f"{true}Enter the code you received: {cn}")
            validation_response = validate_code(headers, email, code)

            if 'status":"ok' in validation_response.text:
                signup_code = validation_response.json()['signup_code']
                create_account(headers, email, signup_code)
            else:
                print(f"{false}Invalid verification code.")
        else:
            print(f"{false}Failed to send verification email.")
    else:
        print(f"{false}Failed to generate headers.")
        
