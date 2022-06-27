"""Отдельный класс-поток"""

import time
from threading import Thread


class ClockThread(Thread):
    """Класс-наследник потока"""
    def __init__(self, interval):
        super().__init__()
        self.daemon = True
        self.interval = interval

    def run(self): # Эта функция отрабатывает, когда мы запускаем объект  start
        while True:
            print(f"Текущее время: {time.ctime()}")
            self.test()
            time.sleep(self.interval)

    def test(self):
        print(1)


THR = ClockThread(1)
THR.start()
time.sleep(5)
# THR.join()
