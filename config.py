from aiogram import Bot
from data.admin import get_proxy


API_TOKEN = 'TOKEN_BOT'
CRYPTO_TOKEN = 'TOKEN_CRYPTO'

ADMIN = 'ADMIN_ID'
CHANNEL_ID = 'CHANNEL_ID'
CHANNEL_URL = 'CHANNEL_URL'

API_ID = 'api_id'
API_HASH = 'api_hash'


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
