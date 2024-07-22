import json
import os

def load_users():
    try:
        with open('data/users.json', 'r') as file:
            users = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        users = {}
    return users

def save_users(users):
    with open('data/users.json', 'w') as file:
        json.dump(users, file, indent=4)

def register_user(username, password):
    users = load_users()
    if username in users:
        return False
    users[username] = password
    save_users(users)
    return True

def check_credentials(username, password):
    users = load_users()
    return users.get(username) == password