# 6. Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое программирование», «сокет», «декоратор».
# Проверить кодировку файла по умолчанию. Принудительно открыть файл в формате Unicode и вывести его содержимое.
import locale
def_coding = locale.getpreferredencoding()

with open('test_file.txt', 'w') as f:
    f.writelines(['сетевое программирование\n','сокет\n','декоратор\n'])

print(f'Дефолтная кодировка: {def_coding}')
print(f'\nОткрытие файла в Юникоде принудительно:')
with open('test_file.txt', 'r', encoding='utf-8', errors='replace') as f:
    print(f.read())
print(f'Открытие файла в дефолтной кодировке:')
with open('test_file.txt', 'r', encoding=def_coding, errors='replace') as f:
    print(f.read())

