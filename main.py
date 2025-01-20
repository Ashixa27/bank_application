import os
import json
import time

import pwinput

import admin_operations
from getpass import getpass

OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

USER_MENU = f"""{OKCYAN}
1. Sa ceara bank statement -> valoare contului
2. Sa transfere unui alt utilizator
3. Sa scoata bani din cont
4. Sa adauge bani in cont
5. Sa converteasca banii{ENDC}{FAIL}
6. Sign out
7. Exit{ENDC}

Type in choice: """

ADMIN_MENU = f"""{OKCYAN}
1. Sa se stearga clientul (admin-only)
2. Sa adauge un client nou (admin-only){ENDC}{FAIL}
3. Sign out{ENDC}{OKCYAN}
4. Show users{ENDC}{FAIL}
5. Exit{ENDC}

Type in choice: """

# ENVIRONMENT VARIABLE

# print(os.environ['admin_bank'])

def login(user: str, auth_path: str = "auth.json") -> str:
    if user == "admin":
        for _ in range(3):
            passwd = input("Type in password: ")
            if passwd == os.environ['admin_bank']:
                return user
        return ""
    else:
        with open(auth_path, "r") as f:
            credentials = json.loads(f.read())

        while user not in credentials:
            print(f"{WARNING}User not found in database.{ENDC}")
            user = input("Type in user:")

        # passwd = pwinput.pwinput(prompt='PW: ', mask='*')
        passwd = input("Citeste parola: ")
        while passwd != credentials[user]:
            passwd = input(f"{WARNING}Wrong password: {ENDC}")

        return user


def account_balance(user: str, bank_path: str = "bank.json") -> str:
    with open(bank_path, "r") as f:
        accounts = json.loads(f.read())

    value = accounts[user]["value"]
    currency = accounts[user]["currency"]

    return f"Your account is worth : {value} {currency}"

# un comentariu aici

def convert_account(user: str, to_currency: str, bank_path: str = "bank.json"):
    with open(bank_path, "r") as f:
        accounts = json.loads(f.read())

    account = accounts[user]
    account["value"] = convert_currency(account['value'], account["currency"], to_currency)
    account["currency"] = to_currency

    with open(bank_path, "w") as f:
        f.write(json.dumps(accounts, indent=4))
    
    # return "Account converted from x to y"


def convert_currency(amount: int, from_currency: str, to_currency: str, currencies_json = "currencies.json") -> int:
    with open(currencies_json, "r") as f:
        conversion_rates = json.loads(f.read())

    amount = amount * conversion_rates[from_currency][to_currency]

    return amount


def transfer_money(sender: str, receiver: str, amount: int, bank_path: str = "bank.json"):
    with open(bank_path, "r") as f:
        accounts = json.loads(f.read())

    if amount <= accounts[sender]["value"]:
        if accounts[sender]["currency"] == accounts[receiver]["currency"]:
            accounts[receiver]["value"] += amount
            accounts[sender]["value"] -= amount
        else:
            amount_receiver_currency = convert_currency(amount, accounts[sender]["currency"], accounts[receiver]["currency"])
            accounts[receiver]["value"] += amount_receiver_currency
            accounts[sender]["value"] -= amount

        with open(bank_path, "w") as f:
            f.write(json.dumps(accounts, indent=4))

        print(f"{OKGREEN}Ati transferat cu succes! Cont curent: {accounts[sender]['value']} {accounts[sender]['currency']}{ENDC}")

    else:
        print(f"{WARNING}Not enough money to send{ENDC}")


def get_username_by_phone(phone_number: str, clients_path: str = "clients.json"):
    with open(clients_path, "r") as f:
        clients = json.loads(f.read())

    for user_id, details in clients.items():
        if details['telefon'] == phone_number:
            return user_id

    print(f"{WARNING}Phone number not recognised!{ENDC}")
    return None


def deposit_money(user: str, amount: int, bank_path: str = "bank.json"):
    with open(bank_path, "r") as f:
        accounts = json.loads(f.read())

    accounts[user]["value"] += amount
    currency = accounts[user]["currency"]

    with open(bank_path, "w") as f:
        f.write(json.dumps(accounts, indent=4))

    print(f"{OKGREEN}Ati depus {amount} {currency}.{ENDC}")


def withdraw_money(user: str, amount: int, bank_path: str = "bank.json"):
    with open(bank_path, "r") as f:
        accounts = json.loads(f.read())

    accounts[user]["value"] -= amount
    currency = accounts[user]["currency"]

    with open(bank_path, "w") as f:
        f.write(json.dumps(accounts, indent=4))

    print(f"{WARNING}Ati retras {amount} {currency}.{ENDC}")


if __name__ == '__main__':
    username = input("Please enter your username: ")
    username = login(username)
    menu = USER_MENU if username != "admin" else ADMIN_MENU

    user_pick = input(menu)

    while True:
        if username != "admin":
            match user_pick:
                case "1":
                    print(account_balance(username))
                case "2":
                    amount = int(input("Citeste de la tastatura suma de bani in valuta personala: "))
                    phone_number = input("Cui vrei sa ii trimiti bani? Introdu numarul de telefon: ")
                    receiver_id = get_username_by_phone(phone_number)
                    if receiver_id:
                        transfer_money(username, receiver_id, amount)
                case "3":
                    amount = int(input("Ce suma vrei sa retragi? "))
                    withdraw_money(username, amount)
                case "4":
                    amount = int(input("Ce suma vrei sa depui? "))
                    deposit_money(username, amount)
                case "5":
                    currency = input("Ce vrei sa transformi? ")
                    # verificati sa fie currency corect
                    convert_account(username,currency)
                case "6":
                    username = input("Citeste un nou user: ")
                    username = login(username)
                case "7":
                    exit(0)
                case "8":
                    pass
                case _:
                    pass
            time.sleep(3)
            menu = USER_MENU if username != "admin" else ADMIN_MENU
            user_pick = input(menu)
        else:
            match user_pick:
                case "1":
                    user_to_delete = input("Ce user doresti sa stergi? ")
                    admin_operations.remove_user(user_to_delete)
                case "2":
                    user_to_add = input("Ce user doresti sa adaugi? ")
                    admin_operations.add_user(user_to_add)
                case "3":
                    username = input("Citeste un nou user: ")
                    username = login(username)
                case "4":
                    with open("bank.json", "r") as f:
                        print(f.read())
                case "5":
                    # option 1
                    # break
                    exit(0)

            time.sleep(3)
            menu = USER_MENU if username != "admin" else ADMIN_MENU
            user_pick = input(menu)









