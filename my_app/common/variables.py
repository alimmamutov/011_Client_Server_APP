"""Константы"""
# Названия модулей
SERVER_MODULE = 'server.py'
CLIENT_MODULE = 'client.py'

# Порт по умолчанию для сетевого ваимодействия
DEFAULT_PORT = 7777
# IP адрес по умолчанию для подключения клиента
DEFAULT_IP_ADDRESS = 'LocalHost'
# Таймаут
DEFAULT_TIMEOUT = 0.5
# Максимальная очередь подключений
MAX_CONNECTIONS = 5
# Максимальная длинна сообщения в байтах
MAX_PACKAGE_LENGTH = 1024
# Кодировка проекта
ENCODING = 'utf-8'

# Прококол JIM основные ключи:
ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'
SENDER = 'sender'

# Прочие ключи, используемые в протоколе
PRESENCE = 'presence'
AUTH = 'authenticate'
RESPONSE = 'response'
ERROR = 'error'
ALERT = 'alert'
PASSWORD = 'password'
MESSAGE = 'message'
MESSAGE_TEXT = 'mess_text'

