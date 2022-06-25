"""Модуль strings"""
# star_smile = u'\U00002B50'
# примеры строк
# переменные, объявленные на уровне модуля являются глобальными (константы
# в верхнем регистре)
A = '\u0410'  #Кодовая точка А-русский язык
print(A)

FIRST_STR = 'Программирование'
print(FIRST_STR)
print(type(FIRST_STR))
SECOND_STR = 'Programování'
# SECOND_STR = 'Programování\u041f'
print(SECOND_STR)

# строка, как последовательность юникод-символов
FIRST_WORD = 'Программа'
SECOND_WORD = '\u041f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0430'
print(SECOND_WORD)

print(FIRST_WORD == SECOND_WORD)

print(len(FIRST_WORD) == len(SECOND_WORD))

# функция ord позволяет получить числовое значение юникод-символа
print(ord('ã'))

# ункция chr позволяет получить символ по коду
print(chr(227))
