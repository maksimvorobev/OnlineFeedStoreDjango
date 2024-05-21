# Интернет-магазин кормов на Django

Это полноценный проект интернет-магазина кормов, разработанный на Django.

# Установка

Шаг 1. Клонируйте репозиторий
```
https://github.com/maksimvorobev/OnlineFeedStoreDjango.git
```
Если вы не используете Git, то вы можете просто скачать исходный код репозитория в ZIP-архиве и распаковать его на свой компьютер.

Шаг 2. Создайте виртуальное окружение
```
python -m venv venv
```
Шаг 3. Активируйте виртуальное окружение

Windows:
```
venv\Scripts\activate
```
Linux и MacOS:
```
source venv/bin/activate
```
Шаг 4. Установите зависимости
```
pip install -r requirements.txt
```
Шаг 5. Создайте в корне проекта файл .env по образу .env.example

Шаг 6. Запустите миграции и загрузите данные в БД
```
cd onlineFeedStore
python manage.py migrate
python manage.py loaddata ../fixtures/goods/categories.json
python manage.py loaddata ../fixtures/goods/products.json
```
Шаг 7. Создайте администратора магазина
```
python manage.py createsuperuser
```
Шаг 8. Запустите сервер
```
python manage.py runserver
```
Откройте браузер и перейдите по адресу http://127.0.0.1:8000/admin/. Введите имя пользователя и пароль администратора, чтобы войти в панель управления магазином.

# Готово!
Вы успешно установили магазин на Django!

# Вклад в проект
Если у вас есть предложения по улучшению или вы обнаружили баг, не стесняйтесь создать issue, отправить pull request или написать напрямую автору. Ваш вклад приветствуется!

# Автор

[Воробьев Максим](https://github.com/maksimvorobev)