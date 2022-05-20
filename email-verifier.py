import requests
import argparse
from colorama import Fore, Style
from validate_email import validate_email


def verify_email(users, domain, api_token):
    for user in users:
        email = f'{user}@{domain}'
        if api_token is not None:
            url = f'https://api.hunter.io/v2/email-verifier?email={email}&api_key={api_token}'
            res = requests.get(url)
            if res.status_code == 200:
                res = res.json()
                if res['data']['status'] == 'valid':
                    print(Fore.GREEN + f'{email} is Valid!')
                else:
                    print(Fore.RED + f'{email} is Invalid!')
        else:
            is_valid = validate_email(email, verify=True)
            if is_valid:
                print(Fore.GREEN + f'{email} is Valid!')
            else:
                print(Fore.RED + f'{email} is Invalid!')


if __name__ == '__main__':
    print('''
    __  ___      _ __    _    __         
   /  |/  /___ _(_) /   | |  / /__  _____
  / /|_/ / __ `/ / /____| | / / _ \/ ___/
 / /  / / /_/ / / /_____/ |/ /  __/ /    
/_/  /_/\__,_/_/_/      |___/\___/_/

Version: 0.1
Author: wowtalon(https://github.com/wowtalon/email-verifier)
    ''')
    parser = argparse.ArgumentParser()
    parser.add_argument('--token', required=False, help="Api key of hunter.io")
    parser.add_argument('--user', required=False, help="Username that you want to verify.")
    parser.add_argument('--users', required=False, help="File containing usernames you want to verify.")
    parser.add_argument('--domain', required=True, help="Domain of email account.")
    args = parser.parse_args()
    users = []
    if args.user is not None:
        users.append(args.user)
    if args.users is not None:
        with open(args.users, 'r') as user_file:
            while True:
                line = user_file.readline().replace('\n', '')
                if not line:
                    break
                users.append(line)
    verify_email(users, args.domain, args.token)
    print(Style.RESET_ALL)
