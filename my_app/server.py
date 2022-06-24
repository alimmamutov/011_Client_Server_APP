"""Программа-сервер"""
import time
from socket import socket, AF_INET, SOCK_STREAM
import sys
import json
import logging
import my_app.log.server_log_config
import argparse
import select
from my_app.common.decos import Log

from my_app.common.variables import ACTION, ACCOUNT_NAME, RESPONSE, ALERT, \
    MAX_CONNECTIONS, PRESENCE, TIME, USER, ERROR, DEFAULT_PORT, AUTH, PASSWORD, SERVER_MODULE, DEFAULT_TIMEOUT, \
    MESSAGE_TEXT, MESSAGE, SENDER, DEFAULT_IP_ADDRESS
from my_app.common.utils import get_message, send_message

LOG = logging.getLogger('server.logger')


@Log(SERVER_MODULE)
def process_client_message(message,messages_list=[], client=None):
    '''
    Обработчик сообщений от клиентов, принимает словарь -
    сообщение от клинта, проверяет корректность,
    возвращает словарь-ответ для клиента
    :param message:
    :param messages_list:
    :param client:
    :return:
    '''
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200, ALERT: 'Пользователь {} прислал запрос на присутствие'.format(message[USER][ACCOUNT_NAME])}
    # Если это Авторизация , то отправляем ответ успешной или не успешной авторизации
    elif ACTION in message and message[ACTION] == AUTH and TIME in message \
            and USER in message:
        if message[USER][ACCOUNT_NAME] == 'Alim' and message[USER][PASSWORD] == '123456':
            return {RESPONSE: 200, ALERT: 'Успешная авторизация пользователя {}'.format(message[USER][ACCOUNT_NAME])}
        else:
            return {RESPONSE: 402,
                    ALERT: 'Неправильный логин/пароль'}
    # Если это сообщение, то добавляем его в очередь сообщений. Ответ не требуется.
    elif ACTION in message and message[ACTION] == MESSAGE and \
            TIME in message and MESSAGE_TEXT in message:
        messages_list.append((message[ACCOUNT_NAME], message[MESSAGE_TEXT]))
        return
    return {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }


@Log(SERVER_MODULE)
def arg_parser():
    """Парсер аргументов коммандной строки"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-a', default=DEFAULT_IP_ADDRESS, nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p

    # проверка получения корретного номера порта для работы сервера.
    if not 1023 < listen_port < 65536:
        LOG.critical(
            f'Попытка запуска сервера с указанием неподходящего порта '
            f'{listen_port}. Допустимы адреса с 1024 до 65535.')
        sys.exit(1)

    return listen_address, listen_port


@Log(SERVER_MODULE)
def socket_server_initial(sock):
    listen_address, listen_port = arg_parser()
    sock.bind((listen_address, listen_port))
    sock.settimeout(DEFAULT_TIMEOUT)
    sock.listen(MAX_CONNECTIONS)
    LOG.info(f'Сервер успешно запущен {"LocalHost" if listen_address == "" else listen_address}:{listen_port}')


@Log(SERVER_MODULE)
def prepare_message(mes):
    return {
                ACTION: MESSAGE,
                SENDER: mes[0],
                TIME: time.time(),
                MESSAGE_TEXT: mes[1]
            }

def main():
    LOG.info('Запуск сервера')
    # open socket
    with socket(AF_INET, SOCK_STREAM) as sock:

        # innitial sock settings
        socket_server_initial(sock)

        # список клиентов , очередь сообщений
        clients = []
        while True:
            try:
                client, client_address = sock.accept()
            except OSError:
                pass
            else:
                LOG.info(f'Установлено соедение с ПК {client_address}')
                clients.append(client)

            clients_read = []
            clients_write = []
            err_lst = []

            # Проверяем на наличие ждущих клиентов
            try:
                if clients:
                    clients_read, clients_write, err_lst = select.select(clients, clients, [], 0)
            except OSError:
                pass

            # принимаем сообщения и если там есть сообщения,
            # кладём в словарь, если ошибка, исключаем клиента.
            messages = []
            if clients_read:
                for client_with_message in clients_read:
                    try:
                        response = process_client_message(get_message(client_with_message),
                                               messages, client_with_message)
                    except:
                        LOG.info(f'Клиент {client_with_message.getpeername()} '
                                    f'отключился от сервера.')
                        clients.remove(client_with_message)
                    else:
                        if response:
                            send_message(client_with_message, response)

            # Если есть сообщения для отправки и ожидающие клиенты, отправляем им сообщения.
            if messages:
                for waiting_client in clients_write:
                    for mes in messages:
                        try:
                            send_message(waiting_client, prepare_message(mes))
                            LOG.info(f'Было отправлено сообщение пользователю {waiting_client.getpeername()} ')
                        except:
                            LOG.info(f'Клиент {waiting_client.getpeername()} отключился от сервера.')
                            # clients.remove(waiting_client)

if __name__ == '__main__':
    main()
