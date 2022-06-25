"""Программа-клиент"""
import argparse
import sys
import json
from socket import socket, AF_INET, SOCK_STREAM
import time
import my_app.log.client_log_config
import logging
from my_app.common.decos import Log

from my_app.common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, ALERT, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT, AUTH, PASSWORD, CLIENT_MODULE, MESSAGE, MESSAGE_TEXT, SENDER
from my_app.common.utils import get_message, send_message
from my_app.errors import ServerError, ReqFieldMissingError

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
    if client_mode not in ('listen', 'send'):
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
        send_message(sock, create_presence())
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
    message = input('Введите сообщение для отправки или \'!!!\' для завершения работы: ')
    if message == '!!!':
        sock.close()
        LOG.info('Завершение работы по команде пользователя.')
        print('Спасибо за использование нашего сервиса!')
        sys.exit(0)
    message_dict = {
        ACTION: MESSAGE,
        TIME: time.time(),
        ACCOUNT_NAME: account_name,
        MESSAGE_TEXT: message
    }
    LOG.debug(f'Сформирован словарь сообщения: {message_dict}')
    return message_dict


@Log(CLIENT_MODULE)
def message_from_server(message):
    """Функция - обработчик сообщений других пользователей, поступающих с сервера"""
    if ACTION in message and message[ACTION] == MESSAGE and \
            SENDER in message and MESSAGE_TEXT in message:
        print(f'Получено сообщение от пользователя '
              f'{message[SENDER]}:\n{message[MESSAGE_TEXT]}')
        LOG.info(f'Получено сообщение от пользователя '
                    f'{message[SENDER]}:\n{message[MESSAGE_TEXT]}')
    else:
        LOG.error(f'Получено некорректное сообщение с сервера: {message}')


def main():
    LOG.info('Запуск клиента')
    # open socket
    with socket(AF_INET, SOCK_STREAM) as sock:
        client_mode, user_name = socket_client_initial(sock)
        # Если соединение с сервером установлено корректно,
        # начинаем обмен с ним, согласно требуемому режиму.
        if client_mode == 'send':
            print('Режим работы - отправка сообщений.')
        else:
            print('Режим работы - приём сообщений.')
        while True:
            # режим работы - отправка сообщений
            if client_mode == 'send':
                try:
                    send_message(sock, create_message(sock, user_name))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    LOG.error(f'Соединение с сервером было потеряно.')
                    sys.exit(1)
                    # Режим работы приём:
            if client_mode == 'listen':
                try:
                    message_from_server(get_message(sock))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    LOG.error(f'Соединение с сервером было потеряно.')
                    sys.exit(1)


if __name__ == '__main__':
    main()

