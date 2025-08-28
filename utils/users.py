import json
from pathlib import Path

CONFIG_FILE = Path("config.json")


def load_config():
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)


def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)


def create_or_update_user(username: str, password: str, role: str):
    """
    Create a new user or update password of an existing user.
    """
    config = load_config()
    users = config.get("users", {})

    users[username] = {"role": role, "password": password}
    config["users"] = users

    save_config(config)
    print(f"✅ User '{username}' created/updated successfully.")


def delete_user(username: str):
    """
    Delete a user if exists.
    """
    config = load_config()
    users = config.get("users", {})

    if username in users:
        del users[username]
        save_config(config)
        print(f"🗑️ User '{username}' deleted.")
    else:
        print(f"⚠️ User '{username}' not found.")
