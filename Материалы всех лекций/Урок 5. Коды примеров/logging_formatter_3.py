"""
Журналирование (логгирование) с использованием модуля logging
Расширенная настройка. Форматирование, обработчики
"""

# Здесь разделил вывод на 2 файла только для критикал и для всех выше дебага(включительно)

import logging

# Создать логгер - регистратор верхнего уроовня
# с именем app.main
LOG = logging.getLogger('app.main')

# Создать обработчик для дебага и выше
FILE_HANDLER = logging.FileHandler("app.log", encoding='utf-8')
# выводит сообщения с уровнем DEBUG
FILE_HANDLER.setLevel(logging.DEBUG)

# Создать обработчик отдельный только для критикал
FILE_HANDLER_2 = logging.FileHandler("app2.log", encoding='utf-8')
# выводит сообщения с уровнем CRITICAL
FILE_HANDLER_2.setLevel(logging.CRITICAL)

# Создать объект Formatter
# Определить формат сообщений
FORMATTER = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s ")

# подключить объект Formatter к обработчику
FILE_HANDLER.setFormatter(FORMATTER)
FILE_HANDLER_2.setFormatter(FORMATTER)

# Добавить обработчик к регистратору
LOG.addHandler(FILE_HANDLER)
LOG.addHandler(FILE_HANDLER_2)

# Установим уровень логгера (Закомментирую, ибо все ломает)
LOG.setLevel(logging.CRITICAL) # Эта настройка приоритетнее тех, что находятся в обработчиках

# Передать сообщение обработчику
LOG.debug('Отладка')
LOG.info('Информационное сообщение')
LOG.warning('Предупреждение')
LOG.critical('Конец')