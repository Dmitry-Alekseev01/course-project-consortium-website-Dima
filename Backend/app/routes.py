# from flask import Blueprint, request, jsonify, send_from_directory, Response
# from sqlalchemy import select as sa_select
# from werkzeug.utils import secure_filename
# import os
# from .models import db, Contact, Event, Project, News, Publications, Organisation, Magazine, Author
# from flask_mail import Message
# from . import mail
# from . import serializers
# import logging
# main = Blueprint('main', __name__)

# UPLOADS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
# os.makedirs(UPLOADS_DIR, exist_ok=True)

# # Маршрут для создания контакта
# @main.route('/api/contact', methods=['POST'])
# def create_contact():
#     print("create_contact --------------------------------------")
#     data = request.get_json()
#     new_contact = Contact(
#         name=data['name'],
#         email=data['email'],
#         phone=data['phone'],
#         company=data.get('company'),
#         message=data['message']
#     )
#     db.session.add(new_contact)
#     db.session.commit()

#     msg = Message(
#         subject=f'Новое сообщение от {data["name"]}',
#         sender=data['email'],
#         recipients=['maxweinsberg25@gmail.com'],
#         body=f"Имя: {data['name']}\nEmail: {data['email']}\nТелефон: {data['phone']}\nКомпания: {data.get('company')}\nСообщение: {data['message']}"
#     )
#     try:
#         mail.send(msg)
#         return jsonify({'message': 'Сообщение отправлено успешно!'}), 201
#     except Exception as e:
#         logging.error(f"Ошибка при отправке email: {e}")
#         return jsonify({'error': 'Не удалось отправить сообщение'}), 500

#     return jsonify({'message': 'Сообщение отправлено успешно!'}), 201

# # Маршрут для получения всех событий
# @main.route('/api/events', methods=['GET'])
# def get_events():
#     events = db.session.scalars(sa_select(Event)).all()
#     #events = Event.query.all()
#     events_list = []
#     for event in events:
#         events_list.append(serializers.serialize_events(event))
#     return jsonify(events_list), 200

# # Маршрут для создания проекта
# @main.route('/api/projects', methods=['POST'])
# def create_project():
#     if 'materials' not in request.files:
#         return jsonify({'error': 'Файл не найден'}), 400

#     file = request.files['materials']
#     if file.filename == '':
#         return jsonify({'error': 'Файл не выбран'}), 400

#     # Сохраняем файл
#     filename = secure_filename(file.filename)
#     file_path = os.path.join(UPLOADS_DIR, filename)
#     file.save(file_path)

#     # Сохраняем путь к файлу в базе данных
#     new_project = Project(
#         title=request.form['title'],
#         publication_date=request.form['publication_date'],
#         description=request.form['description'],
#         content=request.form['content'],
#         materials=filename  # Сохраняем имя файла
#     )

#     # Добавляем авторов (если переданы их ID)
#     author_ids = request.form.getlist('author_ids')
#     for author_id in author_ids:

#         author = Author.query.get(author_id)
#         if author:
#             new_project.authors.append(author)

#     db.session.add(new_project)
#     db.session.commit()

#     return jsonify({'message': 'Проект успешно создан!'}), 201

# # Маршрут для получения всех проектов
# @main.route('/api/projects', methods=['GET'])
# def get_projects():
#     projects = Project.query.all()
#     projects_list = []
#     for project in projects:
#         projects_list.append(serializers.serialize_projects(project))
#     return jsonify(projects_list), 200

# # Маршрут для отдачи файлов
# @main.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(UPLOADS_DIR, filename)

# @main.route('/api/news', methods=['POST'])
# def create_news():
#     if 'materials' not in request.files:
#         return jsonify({'error': 'Файл не найден'}), 400

#     file = request.files['materials']
#     if file.filename == '':
#         return jsonify({'error': 'Файл не выбран'}), 400

#     # Сохраняем файл
#     filename = secure_filename(file.filename)
#     file_path = os.path.join(UPLOADS_DIR, filename)
#     file.save(file_path)

#     # Сохраняем путь к файлу в базе данных
#     new_news = News(
#         title=request.form['title'],
#         publication_date=request.form['publication_date'],
#         description=request.form['description'],
#         # magazine=request.form['magazine'],
#         content=request.form['content'],
#         materials=filename  # Сохраняем имя файла
#     )

#     # Добавляем авторов (если переданы их ID)
#     author_ids = request.form.getlist('author_ids')
#     for author_id in author_ids:
#         author = Author.query.get(author_id)
#         if author:
#             new_news.authors.append(author)

#     magazine = request.form.getlist('magazine')
#     for magazine_id in magazine:
#         magazine = Magazine.query.get(magazine_id)
#         if magazine:
#             new_news.magazine_id.append(magazine)

#     db.session.add(new_news)
#     db.session.commit()

#     return jsonify({'message': 'Новость успешно создана!'}), 201

# # Маршрут для получения всех новостей
# @main.route('/api/news', methods=['GET'])
# def get_news():
#     all_news = News.query.all()
#     news_list = []
#     for news in all_news:
#         news_list.append(serializers.serialize_news(news))
#     return jsonify(news_list), 200

# # Маршрут для получения всех публикаций
# @main.route('/api/publications', methods=['GET'])
# def get_publications():
#     all_publications = Publications.query.all()
#     publications_list = []
#     for publication in all_publications:
#         publications_list.append(serializers.serialize_publications(publication))
#     return jsonify(publications_list), 200

# # Маршрут для получения всех организаций
# @main.route('/api/organisations', methods=['GET'])
# def get_organisations():
#     all_organisations = Organisation.query.all()
#     organisations_list = []
#     for organisation in all_organisations:
#         organisations_list.append(serializers.serialize_organisations(organisation))
#     return jsonify(organisations_list), 200

# # Маршрут для получения всех журналов
# @main.route('/api/magazines', methods=['GET'])
# def get_magazines():
#     magazines = Magazine.query.all()
#     magazines_list = [{'id': mag.id, 'name': mag.name} for mag in magazines]
#     return jsonify(magazines_list), 200

# # Маршрут для получения всех авторов
# @main.route('/api/authors', methods=['GET'])
# def get_authors():
#     authors = Author.query.all()
#     authors_list = [{'id': author.id, 'first_name': author.first_name, 
#                      'last_name': author.last_name, 'middle_name': author.middle_name} 
#                     for author in authors]
#     return jsonify(authors_list), 200


# @main.route('/api/events/<int:event_id>', methods=['GET'])
# def get_event_by_id(event_id):
#     event = Event.query.get(event_id)
#     if event:
#         return jsonify(
#             serializers.serialize_events(event)
#             ), 200
#     else:
#         return jsonify({'error': 'Событие не найдено'}), 404


# @main.route('/api/projects/<int:project_id>', methods=['GET'])
# def get_project_by_id(project_id):
#     project = Project.query.get(project_id)
#     if project:
#         return jsonify(
#             serializers.serialize_projects(project)
#             ), 200
#     else:
#         return jsonify({'error': 'Проект не найден'}), 404
    
# @main.route('/api/publications/<int:publication_id>', methods=['GET'])
# def get_publication_by_id(publication_id):
#     publication = Publications.query.get(publication_id)
#     if publication:
#         return jsonify(
#             serializers.serialize_publications(publication)
#             ), 200
#     else:
#         return jsonify({'error': 'Публикация не найдена'}), 404
    
# @main.route('/api/news/<int:news_id>', methods=['GET'])
# def get_news_by_id(news_id):
#     news = News.query.get(news_id)
#     if news:
#         return jsonify(
#             serializers.serialize_news(news)
#             ), 200
#     else:
#         return jsonify({'error': 'Новость не найдена'}), 404
    
# @main.route('/api/organisations/<int:organisation_id>', methods=['GET'])
# def get_organisation_by_id(organisation_id):
#     organisation = Organisation.query.get(organisation_id)
#     if organisation:
#         return jsonify(
#             serializers.serialize_organisations(organisation)
#             ), 200
#     else:
#         return jsonify({'error': 'Организация не найдена'}), 404
    

# @main.route('/api/search', methods=['GET'])
# def search():
#     query = request.args.get('q', '').strip()

#     print(f" Получен запрос на поиск: '{query}'")

#     if not query:
#         return jsonify({"error": "Пустой запрос"}), 400

#     search_pattern = f"%{query}%"  # Поиск подстроки
#     # Поиск по названиям и содержимому
#     news_results = News.query.filter(
#         (News.title.ilike(search_pattern)) | 
#         (News.description.ilike(search_pattern)) | 
#         (News.content.ilike(search_pattern))
#     ).all()

#     publications_results = Publications.query.filter(
#         (Publications.title.ilike(search_pattern)) | 
#         (Publications.annotation.ilike(search_pattern))
#     ).all()

#     projects_results = Project.query.filter(
#         (Project.title.ilike(search_pattern)) | 
#         (Project.description.ilike(search_pattern)) | 
#         (Project.content.ilike(search_pattern))
#     ).all()

#     events_results = Event.query.filter(
#         (Event.title.ilike(search_pattern)) | 
#         (Event.description.ilike(search_pattern)) | 
#         (Event.location.ilike(search_pattern))
#     ).all()

#     organisations_results = Organisation.query.filter(
#         (Organisation.link.ilike(search_pattern))
#     ).all()

#     # Поиск по авторам (имя, фамилия, отчество)
#     authors_results = Author.query.filter(
#         (Author.first_name.ilike(search_pattern)) | 
#         (Author.last_name.ilike(search_pattern)) | 
#         (Author.middle_name.ilike(search_pattern))
#     ).all()

#     # Поиск по журналам
#     magazines_results = Magazine.query.filter(
#         Magazine.name.ilike(search_pattern)
#     ).all()

#     # Формируем JSON-ответ
#     results = {
#         "news": [{"id": n.id, "title": n.title, "link" : f"/news/{n.id}"} for n in news_results],
#         "publications": [{"id": p.id, "title": p.title, "link" : f"/publications/{p.id}"} for p in publications_results],
#         "projects": [{"id": pr.id, "title": pr.title, "link" : f"/projects/{pr.id}"} for pr in projects_results],
#         "events": [{"id": e.id, "title": e.title, "link" : f"/events/{e.id}"} for e in events_results],
#         "organisations": [{"id": o.id, "link": o.link, "link" : f"/organisations/{o.id}"} for o in organisations_results],
#         "authors": [{"id": a.id, "name": f"{a.last_name} {a.first_name} {a.middle_name or ''}".strip()} for a in authors_results],
#         "magazines": [{"id": m.id, "name": m.name} for m in magazines_results]
#     }

#     return jsonify(results)


from flask import Blueprint, request, jsonify, send_from_directory, Response
from email_validator import validate_email, EmailNotValidError
from sqlalchemy import select as sa_select  # Импортируем select из SQLAlchemy
from werkzeug.utils import secure_filename
import os
from .models import db, Contact, Event, Project, News, Publications, Organisation, Magazine, Author
from flask_mail import Message
from . import mail
from . import serializers
import logging

main = Blueprint('main', __name__)

UPLOADS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
os.makedirs(UPLOADS_DIR, exist_ok=True)

# # Маршрут для создания контакта
# @main.route('/api/contact', methods=['POST'])
# def create_contact():
#     print("create_contact	")
#     data = request.get_json()
#     new_contact = Contact(
#         name=data['name'],
#         email=data['email'],
#         phone=data['phone'],
#         company=data.get('company'),
#         message=data['message']
#     )
#     db.session.add(new_contact)
#     db.session.commit()
#     msg = Message(
#         subject=f'Новое сообщение от {data["name"]}',
#         sender=data['email'],
#         recipients=['maxweinsberg25@gmail.com'],
#         body=f"Имя: {data['name']}\nEmail: {data['email']}\nТелефон: {data['phone']}\nКомпания: {data.get('company')}\nСообщение: {data['message']}"
#     )
#     try:
#         mail.send(msg)
#         return jsonify({'message': 'Сообщение отправлено успешно!'}), 201
#     except Exception as e:
#         logging.error(f"Ошибка при отправке email: {e}")
#         return jsonify({'error': 'Не удалось отправить сообщение'}), 500

# @main.route('/api/contact', methods=['POST'])
# def create_contact():
#     print("create_contact --------------------------------------")
#     data = request.get_json()

#     # Проверка валидности email
#     try:
#         email_info = validate_email(data['email'], check_deliverability=False)
#         data['email'] = email_info.normalized
#     except EmailNotValidError as e:
#         return jsonify({'error': str(e)}), 400

#     new_contact = Contact(
#         name=data['name'],
#         email=data['email'],
#         phone=data['phone'],
#         company=data.get('company'),
#         message=data['message']
#     )
#     db.session.add(new_contact)
#     db.session.commit()

#     msg = Message(
#         subject=f'Новое сообщение от {data["name"]}',
#         sender=data['email'],
#         recipients=['maxweinsberg25@gmail.com'],
#         body=f"Имя: {data['name']}\nEmail: {data['email']}\nТелефон: {data['phone']}\nКомпания: {data.get('company')}\nСообщение: {data['message']}"
#     )
#     try:
#         mail.send(msg)
#         return jsonify({'message': 'Сообщение отправлено успешно!'}), 201
#     except Exception as e:
#         logging.error(f"Ошибка при отправке email: {e}")
#         return jsonify({'error': 'Не удалось отправить сообщение'}), 500


from flask_mail import Message

def send_email(subject, sender, recipients, body):
    try:
        msg = Message(subject, sender=sender, recipients=recipients)
        msg.body = body
        mail.send(msg)
        return True
    except Exception as e:
        logging.error(f"Ошибка при отправке email: {e}")
        return False


@main.route('/api/contact', methods=['POST'])
def create_contact():
    print("create_contact --------------------------------------")
    data = request.get_json()

    # Проверка валидности email
    try:
        email_info = validate_email(data['email'], check_deliverability=False)
        data['email'] = email_info.normalized
    except EmailNotValidError as e:
        return jsonify({'error': str(e)}), 400

    new_contact = Contact(
        name=data['name'],
        email=data['email'],
        phone=data['phone'],
        company=data.get('company'),
        message=data['message']
    )
    db.session.add(new_contact)
    db.session.commit()

    # Отправка email
    subject = f'Новое сообщение от {data["name"]}'
    body = f"Имя: {data['name']}\nEmail: {data['email']}\nТелефон: {data['phone']}\nКомпания: {data.get('company')}\nСообщение: {data['message']}"
    if send_email(subject, data['email'], ['maxweinsberg25@gmail.com'], body):
        return jsonify({'message': 'Сообщение отправлено успешно!'}), 201
    else:
        return jsonify({'error': 'Не удалось отправить сообщение'}), 500


# Маршрут для получения всех событий
@main.route('/api/events', methods=['GET'])
def get_events():
    events = db.session.scalars(sa_select(Event)).all()  # ЗАМЕНА: query.all() -> session.scalars(select(...)).all()
    events_list = []
    for event in events:
        events_list.append(serializers.serialize_events(event))
    return jsonify(events_list), 200


# Маршрут для получения события по ID
@main.route('/api/events/<int:event_id>', methods=['GET'])  # Добавил <int:event_id> для корректного маршрута
def get_event_by_id(event_id):
    event = db.session.get(Event, event_id)  # ЗАМЕНА: query.get() -> session.get()
    if event:
        return jsonify(serializers.serialize_events(event)), 200
    else:
        return jsonify({'error': 'Событие не найдено'}), 404


# Маршрут для получения всех проектов
@main.route('/api/projects', methods=['GET'])
def get_projects():
    projects = db.session.scalars(sa_select(Project)).all()  # ЗАМЕНА: query.all() -> session.scalars(select(...)).all()
    projects_list = []
    for project in projects:
        projects_list.append(serializers.serialize_projects(project))
    return jsonify(projects_list), 200


# Маршрут для получения проекта по ID
@main.route('/api/projects/<int:project_id>', methods=['GET'])  # Добавил <int:project_id> для корректного маршрута
def get_project_by_id(project_id):
    project = db.session.get(Project, project_id)  # ЗАМЕНА: query.get() -> session.get()
    if project:
        return jsonify(serializers.serialize_projects(project)), 200
    else:
        return jsonify({'error': 'Проект не найден'}), 404


# Маршрут для получения всех новостей
@main.route('/api/news', methods=['GET'])
def get_news():
    all_news = db.session.scalars(sa_select(News)).all()  # ЗАМЕНА: query.all() -> session.scalars(select(...)).all()
    news_list = []
    for news in all_news:
        news_list.append(serializers.serialize_news(news))
    return jsonify(news_list), 200


# Маршрут для получения новости по ID
@main.route('/api/news/<int:news_id>', methods=['GET'])  # Добавил <int:news_id> для корректного маршрута
def get_news_by_id(news_id):
    news = db.session.get(News, news_id)  # ЗАМЕНА: query.get() -> session.get()
    if news:
        return jsonify(serializers.serialize_news(news)), 200
    else:
        return jsonify({'error': 'Новость не найдена'}), 404


# Маршрут для получения всех публикаций
@main.route('/api/publications', methods=['GET'])
def get_publications():
    all_publications = db.session.scalars(sa_select(Publications)).all()  # ЗАМЕНА: query.all() -> session.scalars(select(...)).all()
    publications_list = []
    for publication in all_publications:
        publications_list.append(serializers.serialize_publications(publication))
    return jsonify(publications_list), 200


# Маршрут для получения публикации по ID
@main.route('/api/publications/<int:publication_id>', methods=['GET'])  # Добавил <int:publication_id> для корректного маршрута
def get_publication_by_id(publication_id):
    publication = db.session.get(Publications, publication_id)  # ЗАМЕНА: query.get() -> session.get()
    if publication:
        return jsonify(serializers.serialize_publications(publication)), 200
    else:
        return jsonify({'error': 'Публикация не найдена'}), 404


# Маршрут для получения всех организаций
@main.route('/api/organisations', methods=['GET'])
def get_organisations():
    all_organisations = db.session.scalars(sa_select(Organisation)).all()  # ЗАМЕНА: query.all() -> session.scalars(select(...)).all()
    organisations_list = []
    for organisation in all_organisations:
        organisations_list.append(serializers.serialize_organisations(organisation))
    return jsonify(organisations_list), 200


# Маршрут для получения организации по ID
@main.route('/api/organisations/<int:organisation_id>', methods=['GET'])  # Добавил <int:organisation_id> для корректного маршрута
def get_organisation_by_id(organisation_id):
    organisation = db.session.get(Organisation, organisation_id)  # ЗАМЕНА: query.get() -> session.get()
    if organisation:
        return jsonify(serializers.serialize_organisations(organisation)), 200
    else:
        return jsonify({'error': 'Организация не найдена'}), 404


# Маршрут для получения всех журналов
@main.route('/api/magazines', methods=['GET'])
def get_magazines():
    magazines = db.session.scalars(sa_select(Magazine)).all()  # ЗАМЕНА: query.all() -> session.scalars(select(...)).all()
    magazines_list = [{'id': mag.id, 'name': mag.name} for mag in magazines]
    return jsonify(magazines_list), 200


# Маршрут для получения всех авторов
@main.route('/api/authors', methods=['GET'])
def get_authors():
    authors = db.session.scalars(sa_select(Author)).all()  # ЗАМЕНА: query.all() -> session.scalars(select(...)).all()
    authors_list = [{'id': author.id, 'first_name': author.first_name, 
                     'last_name': author.last_name, 'middle_name': author.middle_name} 
                    for author in authors]
    return jsonify(authors_list), 200


# Маршрут для поиска
@main.route('/api/search', methods=['GET'])
def search():
    query = request.args.get('q', '').strip()
    print(f" Получен запрос на поиск: '{query}'")
    if not query:
        return jsonify({"error": "Пустой запрос"}), 400
    search_pattern = f"%{query}%"  # Поиск подстроки

    # ЗАМЕНА: query.filter() -> session.scalars(select(...).filter(...))
    news_results = db.session.scalars(
        sa_select(News).filter(
            (News.title.ilike(search_pattern)) | 
            (News.description.ilike(search_pattern)) | 
            (News.content.ilike(search_pattern))
        )
    ).all()

    publications_results = db.session.scalars(
        sa_select(Publications).filter(
            (Publications.title.ilike(search_pattern)) | 
            (Publications.annotation.ilike(search_pattern))
        )
    ).all()

    projects_results = db.session.scalars(
        sa_select(Project).filter(
            (Project.title.ilike(search_pattern)) | 
            (Project.description.ilike(search_pattern)) | 
            (Project.content.ilike(search_pattern))
        )
    ).all()

    events_results = db.session.scalars(
        sa_select(Event).filter(
            (Event.title.ilike(search_pattern)) | 
            (Event.description.ilike(search_pattern)) | 
            (Event.location.ilike(search_pattern))
        )
    ).all()

    organisations_results = db.session.scalars(
        sa_select(Organisation).filter(
            Organisation.link.ilike(search_pattern)
        )
    ).all()

    authors_results = db.session.scalars(
        sa_select(Author).filter(
            (Author.first_name.ilike(search_pattern)) | 
            (Author.last_name.ilike(search_pattern)) | 
            (Author.middle_name.ilike(search_pattern))
        )
    ).all()

    magazines_results = db.session.scalars(
        sa_select(Magazine).filter(
            Magazine.name.ilike(search_pattern)
        )
    ).all()

    results = {
        "news": [{"id": n.id, "title": n.title, "link": f"/news/{n.id}"} for n in news_results],
        "publications": [{"id": p.id, "title": p.title, "link": f"/publications/{p.id}"} for p in publications_results],
        "projects": [{"id": pr.id, "title": pr.title, "link": f"/projects/{pr.id}"} for pr in projects_results],
        "events": [{"id": e.id, "title": e.title, "link": f"/events/{e.id}"} for e in events_results],
        "organisations": [{"id": o.id, "link": o.link, "link": f"/organisations/{o.id}"} for o in organisations_results],
        "authors": [{"id": a.id, "name": f"{a.last_name} {a.first_name} {a.middle_name or ''}".strip()} for a in authors_results],
        "magazines": [{"id": m.id, "name": m.name} for m in magazines_results]
    }
    return jsonify(results)