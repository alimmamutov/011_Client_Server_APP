"""Декораторы"""

import sys
import logging

import module_name as module_name

import my_app.log.server_log_config
import my_app.log.client_log_config
import traceback
import inspect

if sys.argv[0].find('client') == -1:  # Здесь смотрим полный путь к файлу и ищем в нем "client"
    LOGGER = logging.getLogger('server.logger')
else:
    LOGGER = logging.getLogger('client.logger')


class Log:
    def __init__(self, module_name: str = ''):
        self.module_name = module_name

    def __call__(self, func_to_log):
        def log_saver(*args, **kwargs):
            # ret = func_to_log(*args, **kwargs)
            LOGGER.debug(f'Была вызвана функция {func_to_log.__name__} c параметрами {args}, {kwargs}. '
                         f'Вызов из модуля {func_to_log.__module__ if func_to_log.__module__ != "__main__" else self.module_name}. Вызов из' 
                         f' функции {traceback.format_stack()[0].strip().split()[-1]}.')
                         # f'Вызов из функции {inspect.stack()[1][3]}')
            ret = func_to_log(*args, **kwargs)
            return ret
        return log_saver