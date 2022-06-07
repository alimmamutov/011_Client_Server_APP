"""
1. Задание на закрепление знаний по модулю CSV. Написать скрипт,
осуществляющий выборку определенных данных из файлов info_1.txt, info_2.txt,
info_3.txt и формирующий новый «отчетный» файл в формате CSV.

Для этого:

Создать функцию get_data(), в которой в цикле осуществляется перебор файлов
с данными, их открытие и считывание данных. В этой функции из считанных данных
необходимо с помощью регулярных выражений или другого инструмента извлечь значения параметров
«Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
Значения каждого параметра поместить в соответствующий список. Должно
получиться четыре списка — например, os_prod_list, os_name_list,
os_code_list, os_type_list. В этой же функции создать главный список
для хранения данных отчета — например, main_data — и поместить в него
названия столбцов отчета в виде списка: «Изготовитель системы»,
«Название ОС», «Код продукта», «Тип системы». Значения для этих
столбцов также оформить в виде списка и поместить в файл main_data
(также для каждого файла);

Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл.
В этой функции реализовать получение данных через вызов функции get_data(),
а также сохранение подготовленных данных в соответствующий CSV-файл;

Пример того, что должно получиться:

Изготовитель системы,Название ОС,Код продукта,Тип системы

1,LENOVO,Windows 7,00971-OEM-1982661-00231,x64-based

2,ACER,Windows 10,00971-OEM-1982661-00231,x64-based

3,DELL,Windows 8.1,00971-OEM-1982661-00231,x86-based

Обязательно проверьте, что у вас получается примерно то же самое.

ПРОШУ ВАС НЕ УДАЛЯТЬ СЛУЖЕБНЫЕ ФАЙЛЫ TXT И ИТОГОВЫЙ ФАЙЛ CSV!!!
"""
import os, re, csv
def regex(headers, data):
    re_mask = r'{}'.format(header + ':\s*(.*)')
    re_string = re.compile(re_mask)
    elem = re_string.findall(data)
    return elem


def get_data(path='.'):
    main_data = []
    headers = ['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']
    files = list(filter(lambda x: re.match(r'info_\d*.txt', x), os.listdir(path)))
    for ind, file in enumerate(files):
        with open(file, 'r', encoding='utf-8') as data:
            dict = {'Номер файла': ind + 1}
            txt = data.read()
            for header in headers:
                reg_mask = header + ':\s*(?P<word>.*)'
                compile_string = re.compile(reg_mask)
                dict ['{}'.format(header)] = compile_string.search(txt).group('word')
            main_data.append(dict)
    return main_data


def write_to_csv(out_file):
    main_data = get_data()
    if len(main_data) > 0:
        headers = []
        for key in main_data[0].keys():
            headers.append(key)
            # headers = ['Номер файла', 'Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']
        with open(out_file, 'w', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(main_data)


write_to_csv('my_custom_data.csv')