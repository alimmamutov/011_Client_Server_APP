# Записываем в массив только четные
from datetime import datetime


# объявление обертки без аргумента (передаем сразу оборачиваемую функцию)
def timeit(func):
    print(f'Вызов декоратора без аргумента')
    def wrapper(*args, **kwargs):
        start = datetime.now()
        result = func(*args, **kwargs)
        print(datetime.now() - start)
        return result
    return wrapper


# объявление обертки с аргументом
def timeit_with_arg(arg):

    def outer(func):
        print(f'Вызов декоратора с аргументом {arg}')
        def wrapper(*args, **kwargs):
            start = datetime.now()
            result = func(*args, **kwargs)
            print(datetime.now() - start)
            return result
        return wrapper
    return outer

# Через цикл
@timeit
def one(n):
    l = []
    for i in range(n):
        if i % 2 == 0:
            l.append(i)
    return l


# Через генератор
@timeit_with_arg('my_arg')
def two(n):
    l = [x for x in range(n) if x % 2 == 0]
    return l


l1 = one(10**5)
# l1 = timeit(one)(10**5) Эквивалентна вызову выше
l2 = two(10**5)

