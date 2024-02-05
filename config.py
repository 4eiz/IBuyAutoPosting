from aiogram import Bot
from data.admin import get_proxy


API_TOKEN = '6708966085:AAH8DAOulSOhLHjn6rlL40_MZjcAKekWs9g'
CRYPTO_TOKEN = '150011:AAUcnHTDjxTat2vo9LC9VUTLIXnPaSept7h'

ADMIN = 6489729822
CHANNEL_ID = -1002132546221
CHANNEL_URL = 'https://t.me/MSTR_SERVICES'

API_ID = '28596942'
API_HASH = '7033098f253c5266cc2311fc9a09fab9'


def parse_proxy_string():
    proxy_string = get_proxy()
    parts = proxy_string.split("@")
    login_pass = parts[0].split(":")
    login = login_pass[0]
    password = login_pass[1] if len(login_pass) > 1 else ""
    ip_port = parts[1].split(":")
    ip = ":".join(ip_port[:-1])
    port = ip_port[-1]

    return (login, password, ip, port)

proxy = parse_proxy_string()

PROXY = {
    "scheme": "socks5",
    "hostname": proxy[2],
    "port": int(proxy[3]),
    "username": proxy[0],
    "password": proxy[1]
}

bot = Bot(token=API_TOKEN, parse_mode='HTML')