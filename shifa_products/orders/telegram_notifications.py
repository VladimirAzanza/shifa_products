import requests

from dotenv import load_dotenv
from telebot import apihelper, TeleBot

from .exceptions import MissingTokenException
from shifa_products.constants import (
    TELEGRAM_CHAT_ID,
    TELEGRAM_TOKEN
)

load_dotenv()


def check_tokens():
    missing_tokens = [
        token_name for token, token_name in [
            (TELEGRAM_CHAT_ID, 'Telegram chat ID'),
            (TELEGRAM_TOKEN, 'Telegram token'),
        ] if not token
    ]
    if missing_tokens:
        print(
            f'Revisa la existencia de los tokens:'
            f'{", ".join(missing_tokens)}'
        )
        raise MissingTokenException(
            f'Revisa la existencia de los tokens:'
            f'{", ".join(missing_tokens)}'
        )


def send_notification(message):
    try:
        check_tokens()
        bot = TeleBot(token=TELEGRAM_TOKEN)
        bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=message
        )
    except (requests.RequestException, apihelper.ApiException) as error:
        message = f'Failed to send message: {error}'
        print(message)
