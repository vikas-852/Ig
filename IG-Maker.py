import random
import string
import time
import os
import requests
import names

# ANSI color codes for terminal output
rd, gn, lgn, yw, lrd, be, pe = '\033[00;31m', '\033[00;32m', '\033[01;32m', '\033[01;33m', '\033[01;31m', '\033[94m', '\033[01;35m'
cn, k, g = '\033[00;36m', '\033[90m', '\033[38;5;130m'
true = f'{rd}[{lgn}+{rd}]{gn} '
false = f'{rd}[{lrd}-{rd}] '

# Proxy list (replace with working proxies)
proxy_list = [
    "http://user:pass@proxy1.com:port",
    "http://user:pass@proxy2.com:port",
    "http://user:pass@proxy3.com:port",
]

def get_proxy():
    """Selects a random proxy from the list."""
    return random.choice(proxy_list)

def request_with_proxy(url, headers, method="GET", data=None):
    """Sends a request using a random proxy and retries if needed."""
    for _ in range(3):  # Retry up to 3 times
        proxy = get_proxy()
        proxies = {"http": proxy, "https": proxy}
        try:
            if method == "GET":
                response = requests.get(url, headers=headers, proxies=proxies, timeout=10)
            else:
                response = requests.post(url, headers=headers, data=data, proxies=proxies, timeout=10)

            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"{false} Error with proxy {proxy}: {e}")
    
    print(f"{false} All proxies failed after 3 attempts.")
    return None  # Failed after retries

def get_headers():
    """Generates headers with a random user-agent."""
    an_agent = f'Mozilla/5.0 (Linux; Android {random.randint(9, 13)}; SM-{random.randint(100,999)}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36'
    headers = {
        'User-Agent': an_agent,
        'Accept': 'application/json',
        'Referer': 'https://www.instagram.com/',
        'Origin': 'https://www.instagram.com',
    }
    return headers

def send_verification_email(email):
    """Requests a verification email from Instagram."""
    url = "https://www.instagram.com/api/v1/accounts/send_verify_email/"
    headers = get_headers()
    
    # Debug output
    print(f"{true} Attempting to send verification email to {email}...")
    
    response = request_with_proxy(url, headers, method="POST", data={"email": email})
    
    if response and response.status_code == 200:
        print(f"{true} Verification email sent to {email}")
        return True
    else:
        print(f"{false} Failed to send verification email. Status code: {response.status_code if response else 'No response'}")
        return False

# The rest of your functions go here...

# Clear terminal
os.system("cls" if os.name == "nt" else "clear")

print(f"""{gn}
 _____   _____          __  __         _                
|_   _| / ____|        |  \/  |       | |               
  | |  | |  __  ______ | \  / |  __ _ | | __  ___  _ __ 
  | |  | | |_ ||______|| |\/| | / _` || |/ / / _ \| '__|
 _| |_ | |__| |        | |  | || (_| ||   < |  __/| |   
|_____| \_____|        |_|  |_| \__,_||_|\_\ \___||_|   
       
       Instagram Account Creator
""")

email = input(f'{true} Enter your email: {cn}')
if send_verification_email(email):
    code = input(f'{true} Enter verification code: {cn}')
    signup_code = validate_code(email, code)
    
    if signup_code:
        create_instagram_account(email, signup_code)
    else:
        print(f"{false} Invalid code, account creation aborted.")
else:
    print(f"{false} Email verification failed.")
    
