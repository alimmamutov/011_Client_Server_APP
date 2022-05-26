# Клиент-серверные приложения на Python
## Мамутов Алим 
***
***
****Служебное****

*Создание виртуального окружения*

      python -m venv venv

*Для установки нужного venv:*
    
      pip install -r requirements.txt     
      (requirements.txt лежит в корне проекта)

*Для выгрузки venv:*

      pip freeze > requirements.txt

*Для очистки venv:*

      pip uninstall -r requirements.txt

***Для передачи файлов по SSH***

*На сервер:*

      pscp -P 22 “C:\files or docs\filename” root@178.21.11.180:/home/django/09_Django_2_optimization_tools/

*С сервера:*

      pscp -P 22 root@178.21.11.180:/home/django/09_Django_2_optimization_tools/ C:\Users\Алим\Desktop\Geek\009_Django_Optim_Tools
***
