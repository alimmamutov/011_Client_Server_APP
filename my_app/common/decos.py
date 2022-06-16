"""Декораторы"""

import sys
import logging
import my_app.log.server_log_config
import my_app.log.client_log_config
import traceback
import inspect

if sys.argv[0].find('client') == -1:  # Здесь смотрим полный путь к файлу и ищем в нем "client"
     # если не клиент то сервер!
    LOGGER = logging.getLogger('server')
else:
    # ну, раз не сервер, то клиент
    LOGGER = logging.getLogger('client')

