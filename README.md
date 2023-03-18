# api_yamdb
![example workflow](https://github.com/vartexxx/yamdb_final/actions/workflows/yamdb_workflow.yaml/badge.svg)
Проект YaMDb доступен по адресу: http://158.160.37.120/admin/

Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

В каждой категории есть произведения: книги, фильмы или музыка. Например, в категории «Книги» могут быть произведения «Винни Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Насекомые» и вторая сюита Баха. Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). Новые жанры может создавать только администратор.

Благодарные или возмущённые читатели оставляют к произведениям текстовые отзывы (Review) и выставляют произведению рейтинг (оценку в диапазоне от одного до десяти). Из множества оценок автоматически высчитывается средняя оценка произведения.

Полная документация к API находится по эндпоинту /redoc


### Стек технологий использованный в проекте:
- Python
- Django
- Docker

### Запуск проекта в dev-режиме

- Клонировать репозиторий и перейти в него в командной строке.
- Установите и активируйте виртуальное окружение c учетом версии Python 3.7 (выбираем python не ниже 3.7):

```bash
py -3.7 -m venv venv
```

```bash
source venv/Scripts/activate
```

- Затем нужно установить все зависимости из файла requirements.txt

```bash
python -m pip install --upgrade pip
```

```bash
pip install -r requirements.txt
```

- Выполняем миграции:

```bash
python manage.py migrate --run-syncdb
```

Если есть необходимость, заполняем базу тестовыми данными командой:

```bash
python manage.py load_data
```

Создаем суперпользователя, после меняем в админ панели роль с user на admin:

```bash
python manage.py createsuperuser
```

Запускаем проект:

```bash
python manage.py runserver localhost:80
```

### Примеры работы с API для всех пользователей

Подробная документация доступна по эндпоинту /redoc/

Для неавторизованных пользователей работа с API доступна в режиме чтения, что-либо изменить или создать не получится. 

```
Права доступа: Доступно без токена.
GET /api/v1/categories/ - Получение списка всех категорий
GET /api/v1/genres/ - Получение списка всех жанров
GET /api/v1/titles/ - Получение списка всех произведений
GET /api/v1/titles/{title_id}/reviews/ - Получение списка всех отзывов
GET /api/v1/titles/{title_id}/reviews/{review_id}/comments/ - Получение списка всех комментариев к отзыву
Права доступа: Администратор
GET /api/v1/users/ - Получение списка всех пользователей
```

### Пользовательские роли

- Аноним — может просматривать описания произведений, читать отзывы и комментарии.
- Аутентифицированный пользователь (user) — может, как и Аноним, читать всё, дополнительно он может публиковать отзывы и ставить оценку произведениям (фильмам/книгам/песенкам), может комментировать чужие отзывы; может редактировать и удалять свои отзывы и комментарии. Эта роль присваивается по умолчанию каждому новому пользователю.
- Модератор (moderator) — те же права, что и у Аутентифицированного пользователя плюс право удалять любые отзывы и комментарии.
- Администратор (admin) — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
- Суперюзер Django — обладает правами администратора (admin)

### Регистрация нового пользователя
Получить код подтверждения на переданный email.
Права доступа: Доступно без токена.
Использовать имя 'me' в качестве username запрещено.
Поля email и username должны быть уникальными.

Регистрация нового пользователя:

```
POST /api/v1/auth/signup/
```

```json
{
  "email": "string",
  "username": "string"
}

```

Получение JWT-токена:

```
POST /api/v1/auth/token/
```

```json
{
  "username": "string",
  "confirmation_code": "string"
}
```

# Запуск проекта через контейнер Docker
Перейти в раздел infra и выполнить команду для сборки docker-compose:

```
docker-compose up
```
Выполнить миграции:

```
docker-compose exec web python manage.py migrate
```
Создать суперпользователя:

```
docker-compose exec web python manage.py createsuperuser
```
Собрать статику:

```
docker-compose exec web python manage.py collectstatic --no-input
```

### Автор:
Бурлака Владислав
vartexxx29@yandex.ru

![example workflow](https://github.com/vartexxx/yamdb_final/actions/workflows/yamdb_workflow.yaml/badge.svg)
