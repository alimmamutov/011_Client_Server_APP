"""Лаунчер"""

import subprocess
import time

PROCESS = []

while True:
    ACTION = input('Выберите действие: q - выход, '
                   's - запустить сервер и клиенты, x - закрыть все окна: ')

    if ACTION == 'q':
        break
    elif ACTION == 's':
        clients_count = int(input('Введите количество тестовых клиентов для запуска: '))
        PROCESS.append(subprocess.Popen('python time_server.py',
                                        creationflags=subprocess.CREATE_NEW_CONSOLE))
        time.sleep(0.5)
        for i in range(clients_count):
            PROCESS.append(subprocess.Popen('python time_client.py',
                                            creationflags=subprocess.CREATE_NEW_CONSOLE))
    elif ACTION == 'x':
        while PROCESS:
            VICTIM = PROCESS.pop()
            VICTIM.kill()
