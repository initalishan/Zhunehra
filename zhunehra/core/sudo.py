from dotenv import load_dotenv
from os import environ

load_dotenv()
sudo_users_str = environ.get("sudo_users", "")
sudo_users = list(map(int, sudo_users_str.split(","))) if sudo_users_str else []