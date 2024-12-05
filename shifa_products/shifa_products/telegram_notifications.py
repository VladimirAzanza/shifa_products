import json
import logging
import requests

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
from telebot import apihelper, TeleBot

from .constants import (
    TELEGRAM_CHAT_ID,
    TELEGRAM_TAWKTO_MESSAGE,
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


@csrf_exempt
def tawkto_webhook(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            event = data.get('event')
            visitor_name = data['visitor'].get('name', 'Anónimo')
            visitor_country = data['visitor'].get('country', 'Anónimo')
            if event == 'chat:start':
                message = TELEGRAM_TAWKTO_MESSAGE.format(
                    status='iniciado',
                    visitor_name=visitor_name,
                    visitor_country=visitor_country
                )
            elif event == "chat:end":
                message = TELEGRAM_TAWKTO_MESSAGE.format(
                    status='finalizado',
                    visitor_name=visitor_name,
                    visitor_country=visitor_country
                )
            send_notification(message)
            return JsonResponse(
                {'status': 'success'}, status=200
            )
        except (json.JSONDecodeError, Exception) as error:
            logger.error(
                f'Error al enviar el mensaje: {error}'
            )
            return JsonResponse(
                {'status': 'error', 'message': str(error)}, status=400
            )
    return JsonResponse(
        {'status': 'invalid request'}, status=400
    )
