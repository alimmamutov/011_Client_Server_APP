import subprocess
import chardet

# ARGS = ['ping', 'yandex.ru']
#
# YA_PING = subprocess.Popen(ARGS, stdout=subprocess.PIPE)
# for line in YA_PING.stdout:
#     result = chardet.detect(line)
#     encoded_res1 = line.decode(result['encoding'])
#     print(encoded_res1)
#     encoded_res2 = encoded_res1.encode('utf-8')
#     encoded_res3 = encoded_res2.decode('utf-8')
#     a = 0

my_str = 'Алим'
# encoded_str = str.encode(my_str,encoding='utf-8')
encoded_str = my_str.encode(encoding='windows-1251')
# new_str = encoded_str.decode(encoding='utf-8') # тут будет ошибка
new_str_2 = encoded_str.decode(chardet.detect(encoded_str)['encoding'])
a = 0


f = open('text', 'rb')
for line in f:
    print(chardet.detect(line)['encoding'])
    print(line.decode(chardet.detect(line)['encoding']))