# API_YaTube


Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Жуки» и вторая сюита Баха. Список категорий может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»). 

## Как запустить проект

1. Клонируйте репозиторий и перейдите в него в командной строке:
   ```
   git clone https://github.com/isko118/api_yamdb.git
   ```
   ```
   cd api_yamdb
   ```

2. Создайте и активируйте виртуальное окружение:
   ```
   python3 -m venv venv
   ```
   ```
   source venv/bin/activate
   ```

3. Установите зависимости проекта из файла requirements.txt:
 
   ```
   pip install -r requirements.txt
   ```

4. Примените миграции базы данных:
   ```
   python3 manage.py migrate
   ```

5. Запустите проект:
   ```
   python3 manage.py runserver
   ```

6. Откройте веб-браузер и перейдите по адресу http://localhost:8000, чтобы получить доступ к приложению API_YamDB.

## Структура проекта

Проект следует стандартной структуре Django проекта. Вот основные компоненты:

- `yatube_api/`: Основная директория проекта.
- `posts/`: Директория приложения для управления моделями проекта.
- `api/`: Директория приложения для настройки сериализаторов и view - функций.
- `templates/`: Содержит HTML-шаблоны для отображения веб-страниц.
- `static/`: Содержит статические файлы, такие как yaml файл.
- `manage.py`: Скрипт управления проектом Django.

## Технологии

[![Python](https://img.shields.io/badge/-Python-blue?style=flat&logo=python&logoColor=yellow)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-092E20?style=flat&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-FF1709?style=flat&logo=django&logoColor=white)](https://www.django-rest-framework.org/)
[![Djoser](https://img.shields.io/badge/-Djoser-FF1709?style=flat&logo=django&logoColor=white)](https://djoser.readthedocs.io/)
[![Pillow](https://img.shields.io/badge/-Pillow-FF1709?style=flat&logo=python&logoColor=yellow)](https://pillow.readthedocs.io/)
[![pip](https://img.shields.io/badge/-pip-3776AB?style=flat&logo=pypi&logoColor=white)](https://pypi.org/project/pip/)
[![json](https://img.shields.io/badge/-JSON-000000?style=flat&logo=json&logoColor=white)](https://www.json.org/)


## Внесение вклада

Если вы хотите внести свой вклад в этот проект, пожалуйста, следуйте этим шагам:

1. Форкните репозиторий и создайте новую ветку для вашей функции или исправления ошибки.
2. Внесите свои изменения и убедитесь, что код проходит все тесты.
3. Сделайте коммит ваших изменений и отправьте их в ваш репозиторий.
4. Отправьте pull request с четким описанием ваших изменений.

## Примеры запросов

1.
```
http://127.0.0.1:8000/api/v1/posts/
```
Если будет получен ответ 200:

```
"results": [
   {
      "id": 0,
      "author": "string",
      "text": "string",
      "pub_date": "2021-10-14T20:41:29.648Z",
      "image": "string",
      "group": 0
   }
]
```
## Лицензия

Этот проект лицензирован в соответствии с лицензией MIT. Подробнее см. в файле [LICENSE](LICENSE).

## Авторы

```
Developer 1 - Oleg Akbashev
```
```
Developer 2 -Georgy Petukhov
```
```
Developer 3 - Iskander Nasyrov
```