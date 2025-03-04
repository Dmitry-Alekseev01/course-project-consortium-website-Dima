from flask import Blueprint, request, jsonify, send_from_directory, Response, session
from email_validator import validate_email, EmailNotValidError
from sqlalchemy import select as sa_select
from werkzeug.utils import secure_filename
import os
from .models import db, Contact, Event, Project, News, Publications, Organisation, Magazine, Author
from flask_mail import Message
from . import mail
from . import serializers
from .utils import get_current_language
import logging
from datetime import datetime
from enum import Enum, auto
from sqlalchemy import or_
main = Blueprint('main', __name__)

UPLOADS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
os.makedirs(UPLOADS_DIR, exist_ok=True)
from flask_mail import Message

# Маршрут для отдачи файлов
@main.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOADS_DIR, filename)

def send_email(subject, sender, recipients, body):
    try:
        msg = Message(subject, sender=sender, recipients=recipients)
        msg.body = body
        mail.send(msg)
        return True
    except Exception as e:
        logging.error(f"Ошибка при отправке email: {e}")
        return False

@main.route('/api/get_language', methods=['GET'])
def get_language():
    return jsonify({'language': session.get('language', 'ru')}), 200

@main.route('/api/set_language', methods=['POST'])
def set_language():
    data = request.get_json()
    language = data.get('language')
    if language not in ['ru', 'en']:
        return jsonify({'error': 'Invalid language'}), 400

    session['language'] = language
    response = jsonify({'message': 'Language updated successfully'})
    # Добавляем CORS заголовки
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

@main.route('/api/contact', methods=['POST'])
def create_contact():
    print("create_contact --------------------------------------")
    data = request.get_json()

    # Проверка валидности email
    try:
        email_info = validate_email(data['email'], check_deliverability=False)
        data['email'] = email_info.normalized
    except EmailNotValidError as e:
        logging.error(f"Email validation error: {e}")
        return jsonify({'error': 'Invalid email address provided.'}), 400

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
        return jsonify({'error': 'Не удалось отправить сообщение'}), 200


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
#@basic_auth.required
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

@main.route('/api/magazines/<int:magazine_id>', methods=['GET']) 
def get_magazine_by_id(magazine_id):
    magazine = db.session.get(Magazine, magazine_id) 
    if magazine:
        return jsonify({'id': magazine.id, 'name': magazine.name}), 200
    else:
        return jsonify({'error': 'магазин не найден'}), 404
    


# Маршрут для получения всех журналов
@main.route('/api/magazines', methods=['GET'])
def get_magazines():
    magazines = db.session.scalars(sa_select(Magazine)).all()  # ЗАМЕНА: query.all() -> session.scalars(select(...)).all()
    magazines_list = [{'id': mag.id, 'name': mag.name} for mag in magazines]
    return jsonify(magazines_list), 200

@main.route('/api/authors/<int:author_id>', methods=['GET']) 
def get_author_by_id(author_id):
    author = db.session.get(Author, author_id) 
    if author:
        return {'id': author.id, 'first_name': author.first_name, 
                     'last_name': author.last_name, 'middle_name': author.middle_name}, 200
    else:
        return jsonify({'error': 'автор не найден'}), 404

# Маршрут для получения всех авторов
@main.route('/api/authors', methods=['GET'])
def get_authors():
    authors = db.session.scalars(sa_select(Author)).all() 
    authors_list = [{'id': author.id, 'first_name': author.first_name, 
                     'last_name': author.last_name, 'middle_name': author.middle_name} 
                    for author in authors]
    return jsonify(authors_list), 200



# Это старый рабочий метод НЕ УДАЛЯТЬ
# Маршрут для поиска
# @main.route('/api/search', methods=['GET'])
# def search():
#     query = request.args.get('q', '').strip()
#     print(f" Получен запрос на поиск: '{query}'")
#     if not query:
#         return jsonify({"error": "Пустой запрос"}), 400
#     search_pattern = f"%{query}%"  # Поиск подстроки

#     news_results = db.session.scalars(
#         sa_select(News).filter(
#             (News.title.ilike(search_pattern)) | 
#             (News.description.ilike(search_pattern)) | 
#             (News.content.ilike(search_pattern))
#         )
#     ).all()

#     publications_results = db.session.scalars(
#         sa_select(Publications).filter(
#             (Publications.title.ilike(search_pattern)) | 
#             (Publications.annotation.ilike(search_pattern))
#         )
#     ).all()

#     projects_results = db.session.scalars(
#         sa_select(Project).filter(
#             (Project.title.ilike(search_pattern)) | 
#             (Project.description.ilike(search_pattern)) | 
#             (Project.content.ilike(search_pattern))
#         )
#     ).all()

#     events_results = db.session.scalars(
#         sa_select(Event).filter(
#             (Event.title.ilike(search_pattern)) | 
#             (Event.description.ilike(search_pattern)) | 
#             (Event.location.ilike(search_pattern))
#         )
#     ).all()

#     organisations_results = db.session.scalars(
#         sa_select(Organisation).filter(
#             Organisation.link.ilike(search_pattern)
#         )
#     ).all()

#     authors_results = db.session.scalars(
#         sa_select(Author).filter(
#             (Author.first_name.ilike(search_pattern)) | 
#             (Author.last_name.ilike(search_pattern)) | 
#             (Author.middle_name.ilike(search_pattern))
#         )
#     ).all()

#     magazines_results = db.session.scalars(
#         sa_select(Magazine).filter(
#             Magazine.name.ilike(search_pattern)
#         )
#     ).all()

#     results = {
#         "news": [{"id": n.id, "title": n.title, "link": f"/news/{n.id}"} for n in news_results],
#         "publications": [{"id": p.id, "title": p.title, "link": f"/publications/{p.id}"} for p in publications_results],
#         "projects": [{"id": pr.id, "title": pr.title, "link": f"/projects/{pr.id}"} for pr in projects_results],
#         "events": [{"id": e.id, "title": e.title, "link": f"/events/{e.id}"} for e in events_results],
#         "organisations": [{"id": o.id, "link": o.link, "link": f"/organisations/{o.id}"} for o in organisations_results],
#         "authors": [{"id": a.id, "name": f"{a.last_name} {a.first_name} {a.middle_name or ''}".strip()} for a in authors_results],
#         "magazines": [{"id": m.id, "name": m.name} for m in magazines_results]
#     }
#     return jsonify(results)



# @main.route('/api/search', methods=['GET'])
# def search():
#     query = request.args.get('q', '').strip()
#     sort_type_str = request.args.get('sort', '').strip()

#     if not query:
#         return jsonify({"error": "Пустой запрос"}), 400

#     # Преобразуем строку в значение enum
#     try:
#         sort_type = SortType[sort_type_str.upper()]
#     except KeyError:
#         sort_type = None

#     # Получаем параметры сортировки
#     sort_params = get_sort_params(sort_type)
#     sort_key = sort_params["sort_key"]
#     reverse = sort_params["reverse"]

#     search_pattern = f"%{query}%"


#     # Получение и сортировка данных для каждой категории
#     news_results = get_and_sort_results(
#         News,
#         [
#             (News.title.ilike(search_pattern)) |
#             (News.description.ilike(search_pattern)) |
#             (News.content.ilike(search_pattern))
#         ],
#         sort_key=sort_key,
#         reverse=reverse
#     )

#     publications_results = get_and_sort_results(
#         Publications,
#         [
#             (Publications.title.ilike(search_pattern)) |
#             (Publications.annotation.ilike(search_pattern))
#         ],
#         sort_key=sort_key,
#         reverse=reverse
#     )

#     events_results = get_and_sort_results(
#         Event,
#         [
#             (Event.description.ilike(search_pattern)) |
#             (Event.location.ilike(search_pattern)) |
#             (Event.title.ilike(search_pattern))
#         ],
#         sort_key=sort_key,
#         reverse=reverse
#     )

#     projects_results = get_and_sort_results(
#         Project,
#         [
#             (Project.description.ilike(search_pattern)) |
#             (Project.content.ilike(search_pattern)) |
#             (Project.title.ilike(search_pattern))
#         ],
#         sort_key=sort_key,
#         reverse=reverse
#     )

#     organisations_results = db.session.scalars(
#         sa_select(Organisation).filter(
#             Organisation.link.ilike(search_pattern)
#         )
#     ).all()

#     authors_results = db.session.scalars(
#         sa_select(Author).filter(
#             (Author.first_name.ilike(search_pattern)) | 
#             (Author.last_name.ilike(search_pattern)) | 
#             (Author.middle_name.ilike(search_pattern))
#         )
#     ).all()

#     magazines_results = db.session.scalars(
#         sa_select(Magazine).filter(
#             Magazine.name.ilike(search_pattern)
#         )
#     ).all()


#     results = {
#          "news": [{"id": n.id, "title": n.title, "link": f"/news/{n.id}"} for n in news_results],
#          "publications": [{"id": p.id, "title": p.title, "link": f"/publications/{p.id}"} for p in publications_results],
#          "projects": [{"id": pr.id, "title": pr.title, "link": f"/projects/{pr.id}"} for pr in projects_results],
#          "events": [{"id": e.id, "title": e.title, "link": f"/events/{e.id}"} for e in events_results],
#          "organisations": [{"id": o.id, "link": o.link, "link": f"/organisations/{o.id}"} for o in organisations_results],
#          "authors": [{"id": a.id, "name": f"{a.last_name} {a.first_name} {a.middle_name or ''}".strip()} for a in authors_results],
#          "magazines": [{"id": m.id, "name": m.name} for m in magazines_results]
#     }
#     return jsonify(results)



# @main.route('/api/search', methods=['GET'])
# def search():
#     query = request.args.get('q', '').strip()
#     sort_type_str = request.args.get('sort', '').strip()
#     authors = request.args.getlist('authors[]')
#     magazines = request.args.getlist('magazines[]')
#     date_from = request.args.get('date_from', type=lambda x: datetime.strptime(x, '%Y-%m-%d') if x else None)
#     date_to = request.args.get('date_to', type=lambda x: datetime.strptime(x, '%Y-%m-%d') if x else None)

#     if not query:
#         return jsonify({"error": "Пустой запрос"}), 400

#     try:
#         sort_type = SortType[sort_type_str.upper()]
#     except KeyError:
#         sort_type = None

#     sort_params = get_sort_params(sort_type)
#     sort_key = sort_params["sort_key"]
#     reverse = sort_params["reverse"]
#     search_pattern = f"%{query}%"

#     # Базовые фильтры
#     base_filters = {
#         "news": [
#             (News.title.ilike(search_pattern)) |
#             (News.description.ilike(search_pattern)) |
#             (News.content.ilike(search_pattern))
#         ],
#         "publications": [
#             (Publications.title.ilike(search_pattern)) |
#             (Publications.annotation.ilike(search_pattern))
#         ],
#         "events": [
#             (Event.description.ilike(search_pattern)) |
#             (Event.location.ilike(search_pattern)) |
#             (Event.title.ilike(search_pattern))
#         ],
#         "projects": [
#             (Project.description.ilike(search_pattern)) |
#             (Project.content.ilike(search_pattern)) |
#             (Project.title.ilike(search_pattern))
#         ],
#         "organisations": [
#             Organisation.link.ilike(search_pattern)
#         ],
#         "authors": [
#             (Author.first_name.ilike(search_pattern)) | 
#             (Author.last_name.ilike(search_pattern)) | 
#             (Author.middle_name.ilike(search_pattern))
#         ],
#         "magazines": [
#             Magazine.name.ilike(search_pattern)
#         ]
#     }

#     # Дполнительные фильтры
#     if authors:
#         base_filters["news"].append(News.authors.any(Author.id.in_(authors)))
#         base_filters["publications"].append(Publications.authors.any(Author.id.in_(authors)))
#         base_filters["projects"].append(Project.authors.any(Author.id.in_(authors)))

#     if magazines:
#         base_filters["news"].append(News.magazine_id.in_(magazines))
#         base_filters["publications"].append(Publications.magazine_id.in_(magazines))

#     if date_from and date_to:
#         base_filters["news"].append(News.publication_date.between(date_from, date_to))
#         base_filters["publications"].append(Publications.publication_date.between(date_from, date_to))
#         base_filters["events"].append(Event.publication_date.between(date_from, date_to))
#         base_filters["projects"].append(Project.publication_date.between(date_from, date_to))

#     # Получение и сортировка данных для каждой категории
#     news_results = get_and_sort_results(News, base_filters["news"], sort_key=sort_key, reverse=reverse)
#     publications_results = get_and_sort_results(Publications, base_filters["publications"], sort_key=sort_key, reverse=reverse)
#     events_results = get_and_sort_results(Event, base_filters["events"], sort_key=sort_key, reverse=reverse)
#     projects_results = get_and_sort_results(Project, base_filters["projects"], sort_key=sort_key, reverse=reverse)
#     organisations_results = db.session.scalars(sa_select(Organisation).filter(*base_filters["organisations"])).all()
#     authors_results = db.session.scalars(sa_select(Author).filter(*base_filters["authors"])).all()
#     magazines_results = db.session.scalars(sa_select(Magazine).filter(*base_filters["magazines"])).all()

#     results = {
#          "news": [{"id": n.id, "title": n.title, "link": f"/news/{n.id}"} for n in news_results],
#          "publications": [{"id": p.id, "title": p.title, "link": f"/publications/{p.id}"} for p in publications_results],
#          "projects": [{"id": pr.id, "title": pr.title, "link": f"/projects/{pr.id}"} for pr in projects_results],
#          "events": [{"id": e.id, "title": e.title, "link": f"/events/{e.id}"} for e in events_results],
#          "organisations": [{"id": o.id, "link": o.link, "link": f"/organisations/{o.id}"} for o in organisations_results],
#          "authors": [{"id": a.id, "name": f"{a.last_name} {a.first_name} {a.middle_name or ''}".strip()} for a in authors_results],
#          "magazines": [{"id": m.id, "name": m.name} for m in magazines_results]
#     }
#     return jsonify(results)


def get_and_sort_results(model, filters, sort_key=None, reverse=False):
    results = db.session.scalars(sa_select(model).filter(*filters)).all()
    if sort_key:
        results = sorted(results, key=lambda x: getattr(x, sort_key), reverse=reverse)
    return results

class SortType(Enum):
    ALPHABETICAL = auto()  # Сортировка по алфавиту
    REVERSE_ALPHABETICAL = auto()  # Сортировка в обратном алфавитном порядке
    DATE_ASC = auto()  # Сортировка по дате (по возрастанию)
    DATE_DESC = auto()  # Сортировка по дате (по убыванию)

def get_sort_params(sort_type):
    sort_mapping = {
        SortType.ALPHABETICAL: {"sort_key": "title", "reverse": False},
        SortType.REVERSE_ALPHABETICAL: {"sort_key": "title", "reverse": True},
        SortType.DATE_ASC: {"sort_key": "publication_date", "reverse": False},
        SortType.DATE_DESC: {"sort_key": "publication_date", "reverse": True},
    }
    return sort_mapping.get(sort_type, {"sort_key": None, "reverse": False})

# def build_filters(search_pattern, authors, magazines, date_from, date_to):
#     """
#     Формирует словарь базовых фильтров для каждой категории поиска.
#     Добавляет дополнительные фильтры (авторы, журналы, диапазон дат) только если они заданы.
#     """
#     filters = {
#         "news": [
#             (News.title.ilike(search_pattern)) |
#             (News.description.ilike(search_pattern)) |
#             (News.content.ilike(search_pattern))
#         ],
#         "publications": [
#             (Publications.title.ilike(search_pattern)) |
#             (Publications.annotation.ilike(search_pattern))
#         ],
#         "events": [
#             (Event.description.ilike(search_pattern)) |
#             (Event.location.ilike(search_pattern)) |
#             (Event.title.ilike(search_pattern))
#         ],
#         "projects": [
#             (Project.description.ilike(search_pattern)) |
#             (Project.content.ilike(search_pattern)) |
#             (Project.title.ilike(search_pattern))
#         ],
#         "organisations": [
#             Organisation.link.ilike(search_pattern)
#         ]
#     }

#     # Добавляем фильтр по авторам, если они заданы
#     if authors:
#         filters["news"].append(News.authors.any(Author.id.in_(authors)))
#         filters["publications"].append(Publications.authors.any(Author.id.in_(authors)))
#         filters["projects"].append(Project.authors.any(Author.id.in_(authors)))

#     # Фильтр по журналам
#     if magazines:
#         filters["news"].append(News.magazine_id.in_(magazines))
#         filters["publications"].append(Publications.magazine_id.in_(magazines))

#     # Фильтр по диапазону дат
#     if date_from and date_to:
#         filters["news"].append(News.publication_date.between(date_from, date_to))
#         filters["publications"].append(Publications.publication_date.between(date_from, date_to))
#         filters["events"].append(Event.publication_date.between(date_from, date_to))
#         filters["projects"].append(Project.publication_date.between(date_from, date_to))

#     return filters


def build_filters(query, authors, magazines, date_from, date_to):
    words = query.strip()#.split()
    filters = {
        "news": [],
        "publications": [],
        "events": [],
        "projects": [],
        "organisations": [],
    }

    word_pattern = f"%{words}%"
        
    filters["news"].append(
        or_(
            News.title.ilike(word_pattern),
            News.description.ilike(word_pattern),
            News.content.ilike(word_pattern)
        )
    )
    
    # Публикации
    filters["publications"].append(
        or_(
            Publications.title.ilike(word_pattern),
            Publications.annotation.ilike(word_pattern)
        )
    )
    
    # События
    filters["events"].append(
        or_(
            Event.description.ilike(word_pattern),
            Event.location.ilike(word_pattern),
            Event.title.ilike(word_pattern)
        )
    )
    
    # Проекты
    filters["projects"].append(
        or_(
            Project.description.ilike(word_pattern),
            Project.content.ilike(word_pattern),
            Project.title.ilike(word_pattern)
        )
    )
    
    # Организации
    filters["organisations"].append(
        Organisation.link.ilike(word_pattern)
    )

    # Условия для каждого слова
    # for word in words:
    #     word_pattern = f"%{word}%"
        
    #     # Новости
    #     filters["news"].append(
    #         or_(
    #             News.title.ilike(word_pattern),
    #             News.description.ilike(word_pattern),
    #             News.content.ilike(word_pattern)
    #         )
    #     )
        
    #     # Публикации
    #     filters["publications"].append(
    #         or_(
    #             Publications.title.ilike(word_pattern),
    #             Publications.annotation.ilike(word_pattern)
    #         )
    #     )
        
    #     # События
    #     filters["events"].append(
    #         or_(
    #             Event.description.ilike(word_pattern),
    #             Event.location.ilike(word_pattern),
    #             Event.title.ilike(word_pattern)
    #         )
    #     )
        
    #     # Проекты
    #     filters["projects"].append(
    #         or_(
    #             Project.description.ilike(word_pattern),
    #             Project.content.ilike(word_pattern),
    #             Project.title.ilike(word_pattern)
    #         )
    #     )
        
    #     # Организации
    #     filters["organisations"].append(
    #         Organisation.link.ilike(word_pattern)
    #     )

    # Объединяем условия для слов через OR внутри каждой категории
    for category in filters:
        if filters[category]:
            combined_condition = or_(*filters[category])
            filters[category] = [combined_condition]
        else:
            filters[category] = []

    # Добавление фильтров по авторам, журналам и датам
    if authors:
        filters["news"].append(News.authors.any(Author.id.in_(authors)))
        filters["publications"].append(Publications.authors.any(Author.id.in_(authors)))
        filters["projects"].append(Project.authors.any(Author.id.in_(authors)))

    if magazines:
        filters["news"].append(News.magazine_id.in_(magazines))
        filters["publications"].append(Publications.magazine_id.in_(magazines))

    if date_from and date_to:
        filters["news"].append(News.publication_date.between(date_from, date_to))
        filters["publications"].append(Publications.publication_date.between(date_from, date_to))
        filters["events"].append(Event.publication_date.between(date_from, date_to))
        filters["projects"].append(Project.publication_date.between(date_from, date_to))

    return filters


@main.route('/api/search', methods=['GET'])
def search():
    query = request.args.get('q', '').strip()
    sort_type_str = request.args.get('sort', '').strip()
    # Отфильтровываем пустые значения и преобразуем в int, если требуется
    authors = [int(a) for a in request.args.getlist('authors[]') if a.strip().isdigit()]
    magazines = [int(m) for m in request.args.getlist('magazines[]') if m.strip().isdigit()]
    date_from = request.args.get('date_from', type=lambda x: datetime.strptime(x, '%Y-%m-%d') if x else None)
    date_to = request.args.get('date_to', type=lambda x: datetime.strptime(x, '%Y-%m-%d') if x else None)

    if not query:
        return jsonify({"error": "Пустой запрос"}), 400

    try:
        sort_type = SortType[sort_type_str.upper()]
    except KeyError:
        sort_type = None

    sort_params = get_sort_params(sort_type)
    sort_key = sort_params["sort_key"]
    reverse = sort_params["reverse"]
    search_pattern = query #f"%{query}%"

    # Получаем базовые фильтры через отдельную функцию
    base_filters = build_filters(search_pattern, authors, magazines, date_from, date_to)

    # Получение результатов с использованием корректных фильтров
    news_results = get_and_sort_results(News, base_filters["news"], sort_key=sort_key, reverse=reverse)
    publications_results = get_and_sort_results(Publications, base_filters["publications"], sort_key=sort_key, reverse=reverse)
    events_results = get_and_sort_results(Event, base_filters["events"], sort_key=sort_key, reverse=reverse)
    projects_results = get_and_sort_results(Project, base_filters["projects"], sort_key=sort_key, reverse=reverse)
    organisations_results = db.session.scalars(sa_select(Organisation).filter(*base_filters["organisations"])).all()

    # Сбор авторов и журналов из найденных записей
    authors_results = set()
    magazines_results = set()

    for news in news_results:
        authors_results.update(news.authors)
        if news.magazine:
            magazines_results.add(news.magazine)

    for publication in publications_results:
        authors_results.update(publication.authors)
        if publication.magazine:
            magazines_results.add(publication.magazine)

    for project in projects_results:
        authors_results.update(project.authors)

    results = {
        "news": [{"id": n.id, "title": n.title, "link": f"/news/{n.id}"} for n in news_results],
        "publications": [{"id": p.id, "title": p.title, "link": f"/publications/{p.id}"} for p in publications_results],
        "projects": [{"id": pr.id, "title": pr.title, "link": f"/projects/{pr.id}"} for pr in projects_results],
        "events": [{"id": e.id, "title": e.title, "link": f"/events/{e.id}"} for e in events_results],
        "organisations": [{"id": o.id, "link": f"/organisations/{o.id}"} for o in organisations_results],
        # "authors": [{"id": a.id, "name": f"{a.last_name} {a.first_name} {a.middle_name or ''}".strip()} for a in authors_results],
        # "magazines": [{"id": m.id, "name": m.name} for m in magazines_results]
    }

    return jsonify(results)
