"""Программа-клиент"""
import argparse
import sys
import json
import threading
from socket import socket, AF_INET, SOCK_STREAM
import time
import my_app.log.client_log_config
import logging
from my_app.common.decos import Log

from my_app.common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, ALERT, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT, AUTH, PASSWORD, CLIENT_MODULE, MESSAGE, MESSAGE_TEXT, SENDER, \
    DESTINATION_USER
from my_app.common.utils import get_message, send_message
from my_app.errors import ServerError, ReqFieldMissingError, IncorrectDataRecivedError

LOG = logging.getLogger('client.logger')

@Log(CLIENT_MODULE)
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
    LOG.debug(f'Сформировано {PRESENCE} сообщение для пользователя {account_name}')
    return out


@Log(CLIENT_MODULE)
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


@Log(CLIENT_MODULE)
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


@Log(CLIENT_MODULE)
def arg_parser():
    """Парсер аргументов коммандной строки"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-a', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('-m', '--mode', default='listen', nargs='?')
    parser.add_argument('-u', '--user', default='Guest', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p
    client_mode = namespace.mode
    user_name = namespace.user

    # проверка получения корретного номера порта для работы сервера.
    if not 1023 < listen_port < 65536:
        LOG.critical(
            f'Попытка запуска сервера с указанием неподходящего порта '
            f'{listen_port}. Допустимы адреса с 1024 до 65535.')
        sys.exit(1)

    # Проверим допустим ли выбранный режим работы клиента
    if client_mode not in ('listen', 'send', 'all'):
        LOG.critical(f'Указан недопустимый режим работы {client_mode}, '
                        f'допустимые режимы: listen , send')
        sys.exit(1)
    return listen_address, listen_port, client_mode, user_name


@Log(CLIENT_MODULE)
def socket_client_initial(sock):
    listen_address, listen_port, client_mode, user_name = arg_parser()
    try:
        sock.connect((listen_address, listen_port))
        LOG.info(
            f'Запущен клиент с парамертами: адрес сервера: {listen_address}, '
            f'порт: {listen_port}, режим работы: {client_mode}')
        send_message(sock, create_presence(user_name))
        answer = process_ans(get_message(sock))
        LOG.info(f'Установлено соединение с сервером. Ответ сервера: {answer}')
        print(f'Установлено соединение с сервером.')
        return client_mode, user_name
    except ServerError as error:
        LOG.error(f'При установке соединения сервер вернул ошибку: {error.text}')
        sys.exit(1)
    except ConnectionRefusedError:
        LOG.critical(
            f'Не удалось подключиться к серверу {listen_address}:{listen_port}, '
            f'конечный компьютер отверг запрос на подключение.')
        sys.exit(1)


@Log(CLIENT_MODULE)
def create_message(sock, account_name='Guest'):
    """Функция запрашивает текст сообщения и возвращает его.
    Так же завершает работу при вводе подобной комманды
    """
    time.sleep(1)
    destination_user = input('Введите имя получателя: ')
    message = input('Введите сообщение для отправки:')
    message_dict = {
        ACTION: MESSAGE,
        TIME: time.time(),
        ACCOUNT_NAME: account_name,
        MESSAGE_TEXT: message,
        DESTINATION_USER: destination_user
    }
    LOG.debug(f'Сформирован словарь сообщения: {message_dict}')
    try:
        send_message(sock, message_dict)
        LOG.info(f'Отправлено сообщение для пользователя {destination_user}')
    except:
        LOG.critical('Потеряно соединение с сервером.')
        sys.exit(1)


@Log(CLIENT_MODULE)
def message_from_server(sock, my_username):
    """Функция - обработчик сообщений других пользователей, поступающих с сервера"""
    while True:
        try:
            message = get_message(sock)
            if ACTION in message and message[ACTION] == MESSAGE and SENDER in message:
                print(f'\nПолучено сообщение от пользователя {message[SENDER]}:'
                      f'\n{message[MESSAGE_TEXT]}')
                LOG.info(f'Получено сообщение от пользователя {message[SENDER]}:'
                            f'\n{message[MESSAGE_TEXT]}')
            else:
                LOG.error(f'Получено некорректное сообщение с сервера: {message}')
        except IncorrectDataRecivedError:
            LOG.error(f'Не удалось декодировать полученное сообщение.')
        except (OSError, ConnectionError, ConnectionAbortedError,
                ConnectionResetError, json.JSONDecodeError):
            LOG.critical(f'Потеряно соединение с сервером.')
            break


@Log(CLIENT_MODULE)
def user_interactive(sock, username):
    while True:
        create_message(sock, username)


def main():
    LOG.info('Запуск клиента')
    # open socket
    with socket(AF_INET, SOCK_STREAM) as sock:
        client_mode, user_name = socket_client_initial(sock)
        # Если соединение с сервером установлено корректно,
        # начинаем обмен с ним, согласно требуемому режиму.
        if client_mode == 'send':
            print('Режим работы - отправка сообщений.')
        elif client_mode == 'listen':
            print('Режим работы - приём сообщений.')
        elif client_mode == 'all':
            print(f'Пользователь: {user_name} \n Отправка и получение \n')
            receiver = threading.Thread(target=message_from_server, args=(sock, user_name))
            receiver.daemon = True
            receiver.start()
            user_interface = threading.Thread(target=user_interactive, args=(sock, user_name))
            user_interface.daemon = True
            user_interface.start()
            while True:
                time.sleep(1)
                if user_interface.is_alive() and receiver.is_alive():
                    continue
                break

if __name__ == '__main__':
    main()

