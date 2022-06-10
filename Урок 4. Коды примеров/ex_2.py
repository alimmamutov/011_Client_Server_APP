"""
Подключаем Python-файл с разметкой интерфейса.
Этот файл мы получили через утилиту pyuic.
Пример использования этой утилиты:
pyuic5 test.ui -o test1.py
"""

import sys
from PyQt5.QtWidgets import QApplication, QWidget, qApp
import test

APP = QApplication(sys.argv)#создаем приложение
WINDOW_OBJ = QWidget()#создаем виджет
UI = test.Ui_Form()#инициализирукм нашу форму
UI.setupUi(WINDOW_OBJ)#говорим возьми весь контект формы и отправь ее в мое окно
UI.pushButton_2.clicked.connect(qApp.quit)#делаем обработчик закрытия
WINDOW_OBJ.show()#показываем форму
sys.exit(APP.exec_())#делаем корректную чистую обработку закрытия
