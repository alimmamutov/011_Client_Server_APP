"""Главный поток и дочерний поток (не демон)"""

import threading
import time
from logging import info, basicConfig, INFO


def demo_thr_func(name):
    """Логика функции для дочернего потока"""
    info(f"Дочерний поток {name} стартует")
    time.sleep(8)
    info(f"Дочерний поток {name} завершается")


if __name__ == "__main__":
    basicConfig(
        format="%(asctime)s: %(message)s",
        level=INFO,
        datefmt="%H:%M:%S")
    info("Приложение: до создания дочернего потока")
    THR_OBJ = threading.Thread(target=demo_thr_func, args=(1,))
    info("Приложение: до старта дочернего потока")
    THR_OBJ.start()
    info("Приложение: ждет, пока завершится дочерний поток")
    info("Приложение: ждет, пока завершится дочерний поток")
    info("Приложение: ждет, пока завершится дочерний поток")
    # THR_OBJ.join() # В этом месте основной поток ждет, когда заврешится дочерний поток
    info("????")
    THR_OBJ.join()  # В этом месте основной поток ждет, когда заврешится дочерний поток
    time.sleep(5)
    info('The end')


"""
Приложение ждет завершения дочернего потока, а потом завершается само.
"""
