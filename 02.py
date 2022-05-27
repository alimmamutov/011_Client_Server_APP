# 2. Каждое из слов «class», «function», «method» записать в байтовом типе без преобразования в последовательность кодов
# (не используя методы encode и decode) и определить тип, содержимое и длину соответствующих переменных.

w_1_bytes = b'class'
w_2_bytes = b'function'
w_3_bytes = b'method'

print(f'Тип:{type(w_1_bytes)} Содержание: {w_1_bytes} Длина: {len(w_1_bytes)}')
print(f'Тип:{type(w_2_bytes)} Содержание: {w_2_bytes} Длина: {len(w_2_bytes)}')
print(f'Тип:{type(w_3_bytes)} Содержание: {w_3_bytes} Длина: {len(w_3_bytes)}')