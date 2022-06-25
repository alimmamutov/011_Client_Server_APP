"""Декорируем класс"""


def mod_bar(cls):
    """декоратор в виде функции"""
    # возвращает модифицированный класс
    def decorate(func):
        """возвращает декорированную функцию"""
        def new_func(self):
            """
            здесь вызываем исходную функцию
            и дополняем ее поведение
            """
            print(self.start_str)
            print("Логика декоратора")
            print(func())
            print(self.end_str)

        return new_func

    cls.show = decorate(cls.show) # Здесь мы заменяем родную функцию класса деорируемой
    return cls



class Test:
    """Простой класс"""
    def __init__(self):
        self.start_str = "Запуск декоратора"
        self.end_str = "Завершение декоратора"

    @classmethod
    def show(cls):
        """Метод класса"""
        return "Какая-то функциональность метода класса"

@mod_bar
class Test2(Test):
    pass

TEST_OBJ = Test()
print(TEST_OBJ.show())

TEST_2 = Test2()
TEST_2.show()




