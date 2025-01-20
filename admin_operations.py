import json
from locale import currency


def remove_user(user_to_be_deleted: str, bank_path: str = "bank.json", auth_path: str = "auth.json" , clients_path: str = "clients.json"):

    file_paths = {
        "accounts": bank_path,
        "credentials": auth_path,
        "clients": clients_path
    }
    for key, path in file_paths.items():
        with open(path, "r") as f:
            key = json.loads(f.read())

        key.pop(user_to_be_deleted, None)

        with open(path, "w") as f:
            f.write(json.dumps(key, indent=4))


def add_user(user_to_add: str, bank_path: str = "bank.json", auth_path: str = "auth.json" , clients_path: str = "clients.json"):

    user_details = {
        "name": 0,
        "telefon": 0,
        "oras": 0
    }
    for k, v in user_details.items():
        user_details.update({k:input(f"{k}: ")})

    bank_details = {
        "value": 0,
        "currency": 0
    }
    bank_details.update({"currency":input("currency: ")})

    with open(bank_path, "r") as f:
        accounts = json.loads(f.read())

    with open(auth_path, "r") as f:
        credentials = json.loads(f.read())

    with open(clients_path, "r") as f:
        clients = json.loads(f.read())

    accounts.update({user_to_add: bank_details})
    credentials.update({user_to_add: input("Setati o parola: ")})
    clients.update({user_to_add: user_details})

    with open(bank_path, "w") as f:
        f.write(json.dumps(accounts, indent=4))

    with open(auth_path, "w") as f:
        f.write(json.dumps(credentials, indent=4))

    with open(clients_path, "w") as f:
        f.write(json.dumps(clients, indent=4))