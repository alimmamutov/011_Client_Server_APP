# 5. Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать результаты из байтовового в строковый тип на кириллице.
import subprocess
import chardet
args = (['ping', 'yandex.ru'],['ping', 'youtube.com'])
for arg in args:
    subproc_ping = subprocess.Popen(arg, stdout=subprocess.PIPE)
    for line in subproc_ping.stdout:
        print(line.decode(encoding=chardet.detect(line)['encoding']))