""" Модуль csv_read """
import csv
full_path = 'D:\\Учеба\\011_Client_Server_APP\\01_csv\\'
# csv.reader - принимает ссылку на объект
# Простое чтение из файла kp_data.csv
# Получаем итератор объекта
with open(full_path + 'kp_data.csv') as f_n:
    F_N_READER = csv.reader(f_n)
    print(type(F_N_READER))
    for row in F_N_READER:
        print(row)

# %%
# Преобразование итератора в список
with open(full_path + 'kp_data.csv') as f_n:
    F_N_READER = csv.reader(f_n)
    print(list(F_N_READER))

# %%
# Разделение строки заголовков от содержимого

with open(full_path + 'kp_data.csv') as f_n:
    F_N_READER = csv.reader(f_n)
    F_N_HEADERS = next(F_N_READER)
    print('Headers: ', F_N_HEADERS)
    for row in F_N_READER:
        print(row)

# %%
# Вывод результата с помощью метода DictReader упорядоченный словарь с версии 3.6
with open(full_path + 'kp_data.csv') as f_n:
    F_N_READER = csv.DictReader(f_n)
    for row in F_N_READER:
        print(row)
        print(row['hostname'], row['model'])
