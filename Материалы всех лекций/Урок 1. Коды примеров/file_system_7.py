"""Модуль file_system"""

# получаем кодировку для файла, с которым работаем
F_N = open('test.txt', 'w',)
F_N.write('тест test test')
F_N.close()
print(type(F_N))

# явное указание кодировки при работе с файлом
with open('test.txt', encoding='windows-1251') as f_n:
    for el_str in f_n:
        print(el_str, end='')


# УЗНАТЬ КОДИРОВКУ ФАЙЛА
# перекодировать, rb
# chardet
# dict -> json -> bytes
