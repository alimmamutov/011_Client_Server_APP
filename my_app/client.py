"""Программа-клиент"""

import sys
import json
import socket
import time

from my_app.common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, ALERT, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT, AUTH, PASSWORD
from my_app.common.utils import get_message, send_message


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
    '''Загружаем параметы коммандной строки'''
    # client.py -p 192.168.0.100 8079

    # try:
    #     server_address = sys.argv[2]
    #     server_port = int(sys.argv[3])
    #     if server_port < 1024 or server_port > 65535:
    #         raise ValueError
    # except IndexError:
    #     server_address = DEFAULT_IP_ADDRESS
    #     server_port = DEFAULT_PORT
    #     print(IndexError)
    # except ValueError:
    #     print('В качестве порта может быть указано только число в диапазоне от 1024 до 65535.')
    #     sys.exit(1)

    # Инициализация сокета и обмен
    server_address = DEFAULT_IP_ADDRESS
    server_port = DEFAULT_PORT
    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.connect((server_address, server_port))
    if '-pr' in sys.argv:
        message_to_server = create_presence()
    elif '-auth' in sys.argv:
        account_name = sys.argv[sys.argv.index('-auth') + 1]
        psw = str(sys.argv[sys.argv.index('-auth') + 2])
        message_to_server = create_auth(account_name, psw)
    else: # Если параметры не указаны - делаю по умолчанию запрос присутствия
        message_to_server = create_presence()
    send_message(transport, message_to_server)
    try:
        answer = process_ans(get_message(transport))
        print(answer)
    except (ValueError, json.JSONDecodeError):
        print('Не удалось декодировать сообщение сервера.')


if __name__ == '__main__':
    main()
