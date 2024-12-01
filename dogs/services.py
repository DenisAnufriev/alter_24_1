import requests
from config.settings import TG_BOT_TOKEN, TG_URL


def send_tg_message(chat_id, tg_message):
    params = {
        'text': tg_message,
        'chat_id': chat_id
    }
    response = requests.get(f'{TG_URL}{TG_BOT_TOKEN}/sendMessage', params=params)
