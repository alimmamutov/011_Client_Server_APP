# Преобразовать слова «разработка», «администрирование», «protocol», «standard» из строкового представления в байтовое
# и выполнить обратное преобразование (используя методы encode и decode).

w_list = ['разработка', 'администрирование', 'protocol', 'standard']
for element in w_list:
    print(element)
    encoded_word = str.encode(element, encoding='utf-8')
    print(f'Закодирован - {encoded_word}')
    decoded_word = bytes.decode(encoded_word, encoding='utf-8')
    print(f'Декодирован - {decoded_word}')