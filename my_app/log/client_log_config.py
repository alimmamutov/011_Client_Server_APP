import logging
import os
from my_app.common.variables import ENCODING

# Создаём объект-логгер
LOG = logging.getLogger('client.logger')

# Устанавливаем общий уровень логгирования
LOG.setLevel(logging.DEBUG)

# Создаём объект форматирования:
FORMATTER = logging.Formatter("%(asctime)-30s%(levelname)-10s%(module)-20s %(message)s")

# Подготовка имени файла для логгирования
PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, 'client.log')

# Создаём файловый обработчик логгирования:
FILE_HANDLER = logging.FileHandler(PATH, encoding=ENCODING)
FILE_HANDLER.setFormatter(FORMATTER)
FILE_HANDLER.setLevel(logging.DEBUG)

# Создаём потоковый обработчик логгирования (по умолчанию sys.stderr):
STREAM_HANDLER = logging.StreamHandler()
STREAM_HANDLER.setFormatter(FORMATTER)
STREAM_HANDLER.setLevel(logging.DEBUG)

if __name__ == '__main__':
    
    LOG.addHandler(STREAM_HANDLER)
    # В логгирование передаем имя текущей функции и имя вызвавшей функции
    LOG.debug(f'Проверка логгирования - Будет создан файл {PATH}')
else:
    # Добавляем в логгер обработчик, создающий файл
    LOG.addHandler(FILE_HANDLER)
    # LOG.addHandler(STREAM_HANDLER)