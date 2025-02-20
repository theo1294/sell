import requests
import time
import os
import hashlib
import uuid
import random
import string
from colorama import Fore, Style, init

init()

BANNER = f"""
{Fore.CYAN}====================================={Style.RESET_ALL}
{Fore.BLUE}      FACEBOOK SHARE BOT v1.0        {Style.RESET_ALL}
{Fore.CYAN}====================================={Style.RESET_ALL}
"""

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main_menu():
    while True:
        clear_screen()
        print(BANNER)
        print(f"{Fore.GREEN}1. Spam Share{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}2. Token Getter{Style.RESET_ALL}")
        print(f"{Fore.RED}3. Exit{Style.RESET_ALL}")
        choice = input(f"{Fore.CYAN}Select an option: {Style.RESET_ALL}")
        
        if choice == "1":
            spam_share()
        elif choice == "2":
            token_getter()
        elif choice == "3":
            print(f"{Fore.RED}Exiting...{Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.RED}Invalid choice! Try again.{Style.RESET_ALL}")
            time.sleep(2)

def spam_share():
    clear_screen()
    print(BANNER)
    access_token = input("Enter your access token: ")
    share_url = input("Enter your post link: ")
    share_count = int(input("Enter Share Count: "))
    time_interval = 1
    delete_after = 60 * 60
    shared_count = 0

    def share_post():
        nonlocal shared_count
        url = f"https://graph.facebook.com/me/feed?access_token={access_token}"
        data = {
            "link": share_url,
            "privacy": {"value": "SELF"},
            "no_story": "true"
        }
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        
        try:
            response = requests.post(url, json=data, headers=headers)
            response_data = response.json()
            post_id = response_data.get("id", "Unknown")
            
            shared_count += 1
            print(f"{Fore.GREEN}Post shared: {shared_count}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Post ID: {post_id}{Style.RESET_ALL}")
            
            if shared_count == share_count and post_id != "Unknown":
                time.sleep(delete_after)
                delete_post(post_id)
        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}Failed to share post: {e}{Style.RESET_ALL}")

    def delete_post(post_id):
        url = f"https://graph.facebook.com/{post_id}?access_token={access_token}"
        try:
            response = requests.delete(url)
            if response.status_code == 200:
                print(f"{Fore.RED}Post deleted: {post_id}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Failed to delete post: {response.json()}{Style.RESET_ALL}")
        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}Failed to delete post: {e}{Style.RESET_ALL}")

    for _ in range(share_count):
        share_post()
        time.sleep(time_interval)
    print(f"{Fore.GREEN}Finished sharing posts.{Style.RESET_ALL}")
    input("Press Enter to return to the main menu...")

def token_getter():
    clear_screen()
    print(BANNER)
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    twofactor_code = input("Enter your 2-factor authentication code (Enter '0' if not applicable): ")

    result = make_request(email, password, twofactor_code)
    print(result)
    input("Press Enter to return to the main menu...")

def make_request(email, password, twofactor_code):
    deviceID = str(uuid.uuid4())
    adid = str(uuid.uuid4())
    random_str = ''.join(random.choice(string.ascii_lowercase + "0123456789") for _ in range(24))

    form = {
        'adid': adid,
        'email': email,
        'password': password,
        'format': 'json',
        'device_id': deviceID,
        'locale': 'en_US',
        'api_key': '882a8490361da98702bf97a021ddc14d',
        'access_token': '350685531728%7C62f8ce9f74b12f84c123cc23437a4a32',
    }
    form['sig'] = hashlib.md5(("".join(f"{k}={form[k]}" for k in sorted(form)) + '62f8ce9f74b12f84c123cc23437a4a32').encode()).hexdigest()
    headers = { 'content-type': 'application/x-www-form-urlencoded' }
    url = 'https://b-graph.facebook.com/auth/login'
    
    try:
        response = requests.post(url, data=form, headers=headers)
        return response.json()
    except Exception as e:
        return { 'status': False, 'message': 'Please check your account and password again!' }

if __name__ == '__main__':
    main_menu()
