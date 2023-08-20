# Платформа для онлайн приложения - бэкенд-часть LMS веб-приложения

## Описание
* Настроен CORS.
* Настроена интеграция с Stripe.
* Реализована пагинация (с выводом по 1 курсу и уроку на страницу).
* Реализованы валидаторы:
  * Для видео урока можно добавлять ссылку только на контент www.youtube.com
* Описаны права доступа:
    * Каждый пользователь имеет доступ только к своим курсам и урокам по механизму CRUD.
    * Пользователь может изменять только свой профиль.
* Имеется список зависимостей.
* Результат проверки Flake8 равен 100%, при исключении миграций.
* Документация проекта: http://127.0.0.1:8000/swagger/

## Технологии
* Python
* Django, DRF
* JWT, DRF-YASG
* PostgreSQL
* Redis
* Stripe

## Сущности
* Course (курсы)
* Lesson (уроки)
* User (пользователи)
* Payment (платежи)
* Subscription (обновление подписок)

### Запуск приложения в локальной сети: 
_Для начала необходимо настроить виртуальное окружение и установить все необходимые зависимости с помощью команд:_
```
python -m venv venv
```
```
source venv/bin/activate
```
```
pip install -r requirements.txt
```
_Для работы с переменными окружениями необходимо создать файл .env и заполнить его согласно файлу .env.sample_

_Для создания администратора запустить команду:_
```
python3 manage.py csu
```
_Для заполнения БД запустить команду:_
```
python3 manage.py fill
```
_Для запуска celery_: 
```
celery -A config beat --loglevel=info

celery -A config worker --loglevel=info
```
_Для запуска redis_:
```
redis-cli
```
_Для запуска приложения:_
```
python3 manage.py runserver
```
_Для тестирования проекта запустить команду:_
```
python3 manage.py test
```
_Для запуска подсчета покрытия и вывода отчет запустить команды:_
```
coverage run --source='.' manage.py test

coverage report
```
