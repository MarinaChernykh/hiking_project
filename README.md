[![HIKING_Status](https://github.com/MarinaChernykh/hiking_project/actions/workflows/main.yml/badge.svg)](https://github.com/MarinaChernykh/hiking_project/actions/workflows/main.yml)
# Проект hi-hiking ("Когда сердце в горах")

Проект доступен по адресу:
<https://hi-hiking.ru/>

## Описание
<https://hi-hiking.ru/> - это сайт для тех, кто любит активный отдых в горах или всегда мечтал о нем, но боялся попробовать. На сайте собрана полезная информацию о хайкинге — однодневных походах — в разных регионах Кавказа (Архыз, Домбай, Приэльбрусье, Безенги), которая поможет выбрать место для отдыха и маршруты, которые захочется пройти. **Комментарии пользователей**, оставленные к трекам, а также **средний рейтинг маршрутов**, сформированный на основе их оценок, поможет выбрать оптимальные варинты.
На сайте реализован **полнотекстовый поиск** по текстовым описаниям треков.

В проекте **оптимизированы запросы к базе данных** (в том числе благодаря **кешированию меню**). Реализовано **покрытие тестами** (Unittest).
Проект **развернут на сервере в контейнерах** (используемые технологии - Docker, Nginx, Gunicorn).
Внедрен **CI / CD**, реализованный на основе GitHub Actions. Настроен **мониторинг проекта** через UptimeRobot.

**Шаблоны страниц адаптивны**, сайт можно удобно использовать как с компьютера, так и с мобильного телефона.

## Пользовательские роли
На сайте реализована возможность **регистрации, аутентификации, смены пароля и его восстановления**, и предусмотрены следующие пользовательские роли:

**Аноним** — может просматривать информацию о регионах, треках, осуществлять поиск по сайту, читать комментарии.

**Аутентифицированный пользователь** — может оставлять к трекам свои комментарии и ставить им оценки. На основе пользовательских оценок треков формируется их средний рейтинг и выдача треков в порядке его убывания.


## Технологии
* Python 3.11
* Django 4.2
* PostgreSQL 15.0
* Gunicorn 21.2
* Nginx


## Как запустить проект на удаленном сервере

1. Сделайте форк и склонируйте репозиторий
```
git clone <адрес-форка-репозитория>
```
2. Создайте файл .env и заполните его переменными окружения.
Список необходимых переменных и пример оформления приведены в файле .env.example.

3. Занесите в раздел Secrets and variables -> actions Настроек вашего репозитория на GitHub переменные и их значения,
необходимые для автоматизированного развертывания проекта на сервере:

* Данные для подключения к вашему аккаунту DockerHub:
```
DOCKER_USERNAME
DOCKER_PASSWORD
```
* Данные для подключения к вашему удаленному серверу:
```
HOST
USER
SSH_KEY
PASSPHRASE
```
* Данные для оповещений в телеграм (опционально. Если оповещения не нужны, удалите блок "send_message" в файле main.yml данного проекта):
```
TELEGRAM_TO
TELEGRAM_TOKEN

# TELEGRAM_TO - это id вашего личного аккаунта, можно узнать у телеграм-бота @userinfobot.
# TELEGRAM_TOKEN - токен вашего телеграм-бота. Получить этот токен можно у телеграм-бота @BotFather.
```


4. Подготовьте сервер. На нем должен быть установлен docker и docker compose, а также nginx. Настройте nginx так, чтобы он пробрасывал все входящие запросы на http://127.0.0.1:8000.
```
location / {
        proxy_pass http://127.0.0.1:8000;
}
```

5. Cкопируйте на свой удаленный сервер файлы:
* docker-compose.yml
* .env
```
scp docker-compose.yml hostname@ip-adress:/home/username/
scp .env hostname@ip-adress:/home/username/
```
6. Сделайте коммит проекта и push на github - это запустит процесс создания необходимых образов, их отправку на ваш DockerHub и развертывание на сервере всех необходимых контейнеров, а также запуск проекта
```
git add .
git commit -m 'комментарий'
git push
```
7. Зайдя на сервер, создайте суперпользователя. Если необходимо, используйте sudo перед началом каждой команды.
```
docker-compose exec web python manage.py createsuperuser
```
8. Соберите статику проекта в предназначенный для нее volume
```
docker-compose exec web python manage.py collectstatic --no-input
```
9. Через админку внесите любую релевантную информацию (регионы, маршруты):
```
<http://ip-adress/admin/>
```
Вы также можете внести в базу информацию о нескольких регионах и треках, приведенные для ознакомления, выполнив команду:
```
docker-compose exec web python manage.py loaddata example.json
```
10. Сайт готов к работе и доступен по адресу:
<http://ip-adress/>


## Как запустить проект на локальном компьютере

1. Склонируйте репозиторий на локальный компьютер. Создайте виртуальное окружение (используйте python 3.11) и установите зависимости из файла requirements.txt
```
git clone git@github.com:MarinaChernykh/hiking_project.git
python -m -3.11 venv venv
. venv/Scripts/activate
python -m pip install --upgrade
pip install -r hiking/requirements.txt
```
2. В корневой папке создайте файл .env и заполните его переменными окружения. Список необходимых переменных и пример оформления приведены в файле .env.example.

3. В файле hiking/hiking/settings.py раскомментируйте строку 124:
```
STATICFILES_DIRS = (BASE_DIR / 'static',)
```
4. Запустите контейнер с базой данных  postgres:
```
docker compose -f docker-compose-local.yml
```
5. После завершения запуска контейнера выполните миграции, создайте суперпользователя
```
cd hiking/
python manage.py migrate
python manage.py createsuperuser
```
6. Через админку внесите информацию о нескольких регионах и маршрутах или же внесите в базу информацию о нескольких регионах и треках, приведенные для ознакомления, выполнив команду:
```
python manage.py loaddata example.json
```
7. Запустите сайт:
```
python manage.py runserver
```
8. Сайт готов к работе и доступен по адресу:
<http://localhost:8000/>


## Автор проекта
### Марина Черных
