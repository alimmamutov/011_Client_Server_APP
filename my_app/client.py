"""Программа-клиент"""

import sys
import json
import socket
import time
import my_app.log.client_log_config
import logging
from my_app.common.decos import LOGGER

from my_app.common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, ALERT, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT, AUTH, PASSWORD
from my_app.common.utils import get_message, send_message


LOG = logging.getLogger('client.logger')


def create_presence(account_name='Guest'):
    '''
    Функция генерирует запрос о присутствии клиента
    :param account_name:
    :return:
    '''
    # {'action': 'presence', 'time': 1573760672.167031, 'user': {'account_name': 'Guest'}}
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    return out


def create_auth(account_name, psw):
    '''
    Функция генерирует запрос о присутствии клиента
    :param account_name:
    :return:
    '''
    # {'action': 'presence', 'time': 1573760672.167031, 'user': {'account_name': 'Guest'}}
    out = {
        ACTION: AUTH,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name,
            PASSWORD: psw
        }
    }
    return out


def process_ans(message):
    '''
    Функция разбирает ответ сервера
    :param message:
    :return:
    '''
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            if ALERT in message:
                return '200 : OK {}'.format(message[ALERT])
            else:
                return '200 : OK'
        return message
    raise ValueError


def main():

    # Инициализация сокета и обмен
    server_address = DEFAULT_IP_ADDRESS
    server_port = DEFAULT_PORT
    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        LOG.info(f'Попытка подключения к серверу адрес:{server_address} порт:{server_port}')
        transport.connect((server_address, server_port))
        LOG.info(f'Успешное подключение к серверу')
    except Exception as error:
        LOG.error(error.strerror)
        sys.exit()
    if '-pr' in sys.argv:
        message_to_server = create_presence()
    elif '-auth' in sys.argv:
        LOG.info('Параметры вызова клиента - Аутентификация ')
        account_name = sys.argv[sys.argv.index('-auth') + 1]
        psw = str(sys.argv[sys.argv.index('-auth') + 2])
        message_to_server = create_auth(account_name, psw)
    else: # Если параметры не указаны - делаю по умолчанию запрос присутствия
        LOG.info('Параметры вызова клиента не указаны - по умолчанию отправляю запрос присутствия')
        message_to_server = create_presence()
    LOG.info(f'Сформирован Запрос: {message_to_server}')
    send_message(transport, message_to_server)
    LOG.info(f'Запрос: {message_to_server} отправлен на сервер')
    try:
        answer = process_ans(get_message(transport))
        LOG.info(f'Получен ответ от сервера: {answer}')
        # print(answer)
    except (ValueError, json.JSONDecodeError):
        # print('Не удалось декодировать сообщение сервера.')
        LOG.error('Не удалось декодировать сообщение сервера')

if __name__ == '__main__':
    main()

