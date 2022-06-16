"""Программа-сервер"""

import socket
import sys
import json
import logging
import my_app.log.server_log_config

from my_app.common.variables import ACTION, ACCOUNT_NAME, RESPONSE, ALERT, \
    MAX_CONNECTIONS, PRESENCE, TIME, USER, ERROR, DEFAULT_PORT, AUTH, PASSWORD
from my_app.common.utils import get_message, send_message

LOG = logging.getLogger('server.logger')


def process_client_message(message):
    '''
    Обработчик сообщений от клиентов, принимает словарь -
    сообщение от клинта, проверяет корректность,
    возвращает словарь-ответ для клиента

    :param message:
    :return:
    '''
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200, ALERT: 'Пользователь {} прислал запрос на присутствие'.format(message[USER][ACCOUNT_NAME])}
    elif ACTION in message and message[ACTION] == AUTH and TIME in message \
            and USER in message:
        if message[USER][ACCOUNT_NAME] == 'Alim' and message[USER][PASSWORD] == '123456':
            return {RESPONSE: 200, ALERT: 'Успешная авторизация пользователя {}'.format(message[USER][ACCOUNT_NAME])}
        else:
            return {RESPONSE: 402,
                    ALERT: 'Неправильный логин/пароль'}
    return {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }


def main():
    '''
    Загрузка параметров командной строки, если нет параметров, то задаём значения по умоланию.
    Сначала обрабатываем порт:
    server.py -p 8079 -a 192.168.0.100
    :return:
    '''
    LOG.info('Запуск сервера')
    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
            LOG.debug(f'Выбран порт: {listen_port}')
        else:
            listen_port = DEFAULT_PORT
            LOG.debug(f'Выбран порт: {listen_port} (по умолчанию)')
        if listen_port < 1024 or listen_port > 65535:
            LOG.error(f'Порт: {listen_port} не доступен для выбора!')
            raise ValueError
    except IndexError:
        LOG.error(f'После параметра -\'p\' необходимо указать номер порта.')
        # print('После параметра -\'p\' необходимо указать номер порта.')
        sys.exit(1)
    except ValueError:
        # print(
        #     'В качастве порта может быть указано только число в диапазоне от 1024 до 65535.')
        LOG.error('В качастве порта может быть указано только число в диапазоне от 1024 до 65535.')
        sys.exit(1)

    # Затем загружаем какой адрес слушать

    try:
        if '-a' in sys.argv:
            listen_address = sys.argv[sys.argv.index('-a') + 1]
            LOG.debug(f'Выбран адрес: {listen_address}')
        else:
            listen_address = ''
            LOG.debug(f'Выбран адрес локального хоста по умолчанию')
    except IndexError:
        # print(
        #     'После параметра \'a\'- необходимо указать адрес, который будет слушать сервер.')
        LOG.error('После параметра \'a\'- необходимо указать адрес, который будет слушать сервер.')
        sys.exit(1)

    # Готовим сокет

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.bind((listen_address, listen_port))

    # Слушаем порт

    transport.listen(MAX_CONNECTIONS)
    LOG.info(f'Сервер успешно запущен {"LocalHost" if listen_address=="" else listen_address}:{listen_port}')
    while True:
        client, client_address = transport.accept()
        try:
            message_from_cient = get_message(client)
            LOG.debug('Соединение открыто')
            # print(message_from_cient)
            LOG.info(f'Получено сообщение от клиента {message_from_cient}')
            # {'action': 'presence', 'time': 1573760672.167031, 'user': {'account_name': 'Guest'}}
            response = process_client_message(message_from_cient)
            LOG.info(f'Подготовлено ответное сообщение {response}')
            send_message(client, response)
            LOG.info('Сообщение успешно отправлено клиенту')
            client.close()
        except (ValueError, json.JSONDecodeError):
            # print('Принято некорретное сообщение от клиента.')
            LOG.critical('Принято некорретное сообщение от клиента.')
            client.close()
        LOG.debug('Соединение закрыто')

if __name__ == '__main__':
    main()
