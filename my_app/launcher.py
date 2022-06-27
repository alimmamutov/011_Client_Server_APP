"""Программа-лаунчер"""
import random
import subprocess
import time

PROCESSES = []
def get_name(i):
    return  f'{random.getrandbits(128)}/{i}'

while True:
    ACTION = input('Выберите действие: q - выход, '
                   's - запустить сервер и клиенты, '
                   'x - закрыть все окна: ')

    if ACTION == 'q':
        break
    elif ACTION == 's':
        # clients_count = int(input('Введите количество тестовых клиентов для запуска: '))
        # Запускаем сервер!
        PROCESSES.append(subprocess.Popen('python server.py', creationflags=subprocess.CREATE_NEW_CONSOLE, shell=False))
        PROCESSES.append(subprocess.Popen('python client.py -m all -u Tom', creationflags=subprocess.CREATE_NEW_CONSOLE, shell=False))
        PROCESSES.append(subprocess.Popen('python client.py -m all -u John', creationflags=subprocess.CREATE_NEW_CONSOLE, shell=False))
        # for i in range(2):
        #     # Добавил так имя так как имена 1-2-3 бывают заняты
        #     # name = get_name(i)
        #     PROCESSES.append(subprocess.Popen(f'gnome-terminal -- python3 client.py -n Test{i}', shell=True))
    elif ACTION == 'x':
        while PROCESSES:
            VICTIM = PROCESSES.pop()
            VICTIM.kill()
