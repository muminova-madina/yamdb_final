# yamdb_final
![example branch parameter](https://github.com/madina-zvezda/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=56C0C0&color=008080)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat&logo=Django&logoColor=56C0C0&color=008080)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat&logo=Django%20REST%20Framework&logoColor=56C0C0&color=008080)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat&logo=PostgreSQL&logoColor=56C0C0&color=008080)](https://www.postgresql.org/)
[![JWT](https://img.shields.io/badge/-JWT-464646?style=flat&color=008080)](https://jwt.io/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat&logo=NGINX&logoColor=56C0C0&color=008080)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat&logo=gunicorn&logoColor=56C0C0&color=008080)](https://gunicorn.org/)
[![Docker](https://img.shields.io/badge/-Docker-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/)
[![Docker-compose](https://img.shields.io/badge/-Docker%20compose-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/)
[![Docker Hub](https://img.shields.io/badge/-Docker%20Hub-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/products/docker-hub)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat&logo=GitHub%20actions&logoColor=56C0C0&color=008080)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat&logo=Yandex.Cloud&logoColor=56C0C0&color=008080)](https://cloud.yandex.ru/)


### Адрес сайта
http://51.250.105.140/redoc/
### Пример запроса
http://51.250.105.140/api/admin/
## Описание
Сайт является - базой отзывов о фильмах, книгах и музыке.
Пользователи могут оставлять рецензии на произведения, а также комментировать эти рецензии.
Администрация добавляет новые произведения и категории (книга, фильм, музыка и т.д.)
Также присутствует файл docker-compose, позволяющий , быстро развернуть контейнер базы данных (PostgreSQL), контейнер проекта django + gunicorn и контейнер nginx
## Как запустить

## Необходимое ПО

Docker: https://www.docker.com/get-started <br />
Docker-compose: https://docs.docker.com/compose/install/

## Инструкция по запуску

Для запуска необходимо из корневой папки проекта ввести в консоль(bash или zsh) команду:
```
docker-compose up --build
```
Затем узнать id контейнера, для этого вводим
```
docker container ls
```
В ответ получаем примерно следующее
```
CONTAINER ID   IMAGE                             COMMAND                  CREATED         STATUS         PORTS                    NAMES
ab8cb8741e4a   nginx:1.19.0                      "/docker-entrypoint.…"   7 minutes ago   Up 2 minutes   0.0.0.0:80->80/tcp       madina-nginx-1
f78cc8f246fb   ognennayazvezda/yamdb_final:latest "/bin/sh -c 'gunicor…"   7 minutes ago   Up 2 minutes   0.0.0.0:8000->8000/tcp   madina-web-1
a68243a0a5e2   postgres:12.4                     "docker-entrypoint.s…"   7 minutes ago   Up 2 minutes   5432/tcp                 madina_db_1
```
Нас интересует контейнер madina-web-1, заходим в него командой
```
docker exec -it <CONTAINER ID> sh
```
И делаем миграцию БД, и сбор статики
```
python manage.py migrate
python manage.py collectstatic
```
При желании можно загрузить тестовую бд с контентом
```
python manage.py loaddata fixtures.json
```
## Как пользоваться

После запуска проекта, подробную инструкцию можно будет посмотреть по адресу http://0.0.0.0/redoc/

## Автор
* **Муминова Мадина** - https://github.com/madina-zvezda
