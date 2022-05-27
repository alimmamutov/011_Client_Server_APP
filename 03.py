# Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в байтовом типе.

b_1 = b'attribute'
b_2 = b'класс' # bytes can only contain ASCII literal characters.
b_3 = b'функция' # bytes can only contain ASCII literal characters.
b_4 = b'type'
