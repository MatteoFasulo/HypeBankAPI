import argparse

import banking
from hype import Hype
from getpass import getpass  # For interactive password input
from utils import save_json

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="HypeAPI",
        description='Fetch data from Hype API and create JSON folder with profile, balance, card and movements information'
    )
    parser.add_argument('-m', '--email', help='Email address', required=True, type=str)
    parser.add_argument('-p', '--password', action='store_true', help='Hype Password')
    parser.add_argument('-b', '--birthdate', help='Birth date in ISO (YYYY-MM-DD)', required=True)
    parser.add_argument('-v', '--verbose', action='store_true', required=False, default=False)
    args = parser.parse_args()

    if not args.password: 
        args.password = getpass('Hype password: ')

    h = Hype()
    h.login(args.email, args.password, args.birthdate)
    if args.verbose:
        print('Logged in. Waiting for OTP code...\n')

    # Wait for OTP code to arrive via SMS
    h.otp2fa(int(input("OTP code: ")))

    # You are now logged in
    try:
        profile = h.get_profile()
        balance = h.get_balance()
        card = h.get_card()
        movements = h.get_movements(limit=50)

        save_json(profile, 'profile.json')
        save_json(balance, 'balance.json')
        save_json(card, 'card.json')
        save_json(movements, 'movements.json')
        if args.verbose:
            print('JSON folder created.\nNow you can run the Streamlit WebApp!')
    except banking.Banking.AuthenticationFailure:
        # Token has expired
        h.renew()
        print('Renew Token')