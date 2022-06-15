"""
Журналирование (логгирование) с использованием модуля logging
Расширенная настройка. Форматирование, обработчики
"""

import sys
import logging

# Создать логгер - регистратор верхнего уроовня
# с именем app
APP_LOG = logging.getLogger('app')
# Установить Общий уровень важности
APP_LOG.setLevel(logging.INFO)

# Создать обработчик который выводит сообщения с уровнем ERROR в поток stderr
STREAM_HANDLER = logging.StreamHandler(sys.stderr)
STREAM_HANDLER.setLevel(logging.ERROR)

# Создать обработчик который выводит сообщения в файл
FILE_HANDLER = logging.FileHandler('app_4.log', encoding='utf-8')
FILE_HANDLER.setLevel(logging.INFO)

# Создать объект Formatter
# Определить формат сообщений
FORMATTER = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s ")

# подключить объект Formatter к обработчикам
STREAM_HANDLER.setFormatter(FORMATTER)
FILE_HANDLER.setFormatter(FORMATTER)

# Добавить обработчики к регистратору
APP_LOG.addHandler(STREAM_HANDLER)
APP_LOG.addHandler(FILE_HANDLER)

# Передать сообщение обработчику
APP_LOG.info('Замечательный день для релиза!') # Это выведется только в файл
APP_LOG.critical('Полный писец настал') # это должно вывестись в Консоль и в файл
APP_LOG.error('Error 404') # это должно вывестись в Консоль и в файл
APP_LOG.warning('Warning')  # это должно вывестись в файл
