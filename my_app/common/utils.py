"""Утилиты"""

import json
from .variables import MAX_PACKAGE_LENGTH, ENCODING
import logging
import my_app.log.client_log_config,  my_app.log.server_log_config
from my_app.common.decos import Log

LOG_server = logging.getLogger('server.logger')
LOG_client = logging.getLogger('client.logger')

@Log('utils.py')
def get_message(client):
    '''
    Утилита приёма и декодирования сообщения
    принимает байты выдаёт словарь, если приняточто-то другое отдаёт ошибку значения
    :param client:
    :return:
    '''

    encoded_response = client.recv(MAX_PACKAGE_LENGTH)
    if isinstance(encoded_response, bytes):
        json_response = encoded_response.decode(ENCODING)
        response = json.loads(json_response)
        if isinstance(response, dict):
            return response
        else:
            LOG_client.error(f'Сообщение {response} не является словарем')
            LOG_server.error(f'Сообщение {response} не является словарем')
            raise ValueError
    else:
        LOG_client.error('Сообщение не в байтовом выражении')
        LOG_server.error('Сообщение не в байтовом выражении')
        raise ValueError

@Log('utils.py')
def send_message(sock, message):
    '''
    Утилита кодирования и отправки сообщения
    принимает словарь и отправляет его
    :param sock:
    :param message:
    :return:
    '''
    if not isinstance(message, dict):
        LOG_client.error(f'Сообщение {message} не является словарем')
        LOG_server.error(f'Сообщение {message} не является словарем')
        raise ValueError
    js_message = json.dumps(message)
    encoded_message = js_message.encode(ENCODING)
    sock.send(encoded_message)
