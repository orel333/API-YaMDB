# API-YaMDB (командный проект)
### Технологии
- Python 3.7.0
- Django 2.2.16
- Djago REST framework 3.12.4
- Simple JWT 5.0.0

## Описание
- Данный сервис собирает отзывы (Review) пользователей на произведения (Titles). Произведения делятся на категории: "Книги", "Фильмы", "Музыка". Список категорий (Category) может быть расширен администратором (например, можно добавить категорию "Ювелирные украшения").
- В сервисе предусмотрены разные наборы разрешений на действия в зависимости от роли пользователя: Аноним, Просто аутентифицированный пользователь, Модератор, Администратор, Суперпользователь. 
  - Аноним может просматривать описания произведений, читать отзывы и комментарии.
  - Аутентифицированный пользователь может читать всё, как и Аноним, может публиковать отзывы и ставить оценки произведениям (фильмам/книгам/песенкам), может комментировать отзывы; может редактировать и удалять свои отзывы и комментарии, редактировать свои оценки произведений, просматривать информацию о своём аккаунте, менять её (кроме роли). Эта роль присваивается по умолчанию каждому новому пользователю.
  - Модератор имеет те же права, что и Аутентифицированный пользователь, плюс право удалять и редактировать любые отзывы и комментарии.
  - Администратор имеет полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может просматривать список зарегистрированных пользователей. Может создавать и назначать роли пользователям. Но администратор не может удалять других администраторов и менять им роли. А также не может удалять и менять суперпользователей (см. ниже).
  - Суперпользователь имеет абсолютно все разрешения вне зависимости от его "витринной" роли (которая может быть любой из перечисленных выше). В том числе может удалять администраторов и менять им роли.
- При регистрации через API-запрос с указанием `username` и `e-mail` пользователь получает на указанный электронный адрес письмо с confirmation_code для подтверждения регистрации.
- Независимо от способа (API-сервис, командная строка, панель администратора) регистрация пользователя происходит с выдачей ему JWT-токенов: access \- для доступа к ресурсам сервиса \- и confirmation_code \- для подтверждения первичной регистрации пользователя через API и ситуаций необходимости выдачи нового access-токена.
  -  acess-токен включает в себя в том числе информацию о роли пользователя и его статусе суперюзера; **таким образом в сервис _заложена_ возможность идентифицации прав пользователя _без обращения к БД_**. **В текущей версии для соответствия условиям поставленной задачи _используется_ идентификация роли _через обращение к БД_.**
  - При изменении информации о пользователе, к которой чувствителен соответствующий токен, вне зависимости от способа изменения, пользователю выдается новый соответствующий токен.

### Запуск проекта в dev-режиме
- Установите и активируйте виртуальное окружение
- Установите зависимости из файла requirements.txt
```
pip install -r requirements.txt
``` 
- В папке с файлом manage.py выполните команду:
```
python3 manage.py runserver
```
#### Распределение задач в команде

- [orel333](https://github.com/orel333/API-YaMDB/commits/master/README.md?author=orel333):
пишет всю часть, касающуюся управления пользователями (Auth и Users): систему регистрации и аутентификации, права доступа, работу с токеном, систему подтверждения через e-mail.
- [Ascurse](https://github.com/orel333/API-YaMDB/commits/master/README.md?author=Ascurse):
пишет категории (Categories), жанры (Genres) и произведения (Titles): модели, представления и эндпойнты для них.»
- [emarpoint](https://github.com/orel333/API-YaMDB/commits/master/README.md?author=emarpoint):
занимается отзывами (Review) и комментариями (Comments): описывает модели, представления, настраивает эндпойнты, определяет права доступа для запросов. Рейтинги произведений тоже достаются третьему разработчику. 
