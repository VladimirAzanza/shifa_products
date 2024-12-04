import logging
import requests

from dotenv import load_dotenv
from telebot import apihelper, TeleBot

from shifa_products.constants import (
    TELEGRAM_CHAT_ID,
    TELEGRAM_TOKEN
)

load_dotenv()
logger = logging.getLogger('telegram_notifications')


def check_tokens():
    missing_tokens = [
        token_name for token, token_name in [
            (TELEGRAM_CHAT_ID, 'Telegram chat ID'),
            (TELEGRAM_TOKEN, 'Telegram token'),
        ] if not token
    ]
    if missing_tokens:
        logger.error(
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
        logger.error(
            f'Error al enviar el mensaje: {error}'
        )
