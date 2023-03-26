# yamdb_final
https://github.com/madina-zvezda/yamdb_final/actions/workflows/yamdb_workflow.yaml/badge.svg

### Адрес сайта
http://http://51.250.105.140/redoc/
### Пример запроса
http://51.250.105.140/api/v1/titles/
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