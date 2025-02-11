# # conftest.py
# from pytest import fixture
# from datetime import datetime, date, time
# import sys
# from pathlib import Path

# root_dir = Path(__file__).parent.parent
# sys.path.append(str(root_dir))

# from app.models import Author, News, Event, Project, Publications, Organisation, Magazine, Contact, db
# from app import create_app

# @fixture
# def sample_author_with_middle_name():
#     return Author(
#         id=1,
#         last_name="Иванов",
#         first_name="Иван",
#         middle_name="Иванович"
#     )

# @fixture
# def sample_author_without_middle_name():
#     return Author(
#         id=2,
#         last_name="Петров",
#         first_name="Петр",
#         middle_name=None
#     )

# @fixture
# def sample_magazine():
#     return Magazine(id=1, name="Журнал 1")

# @fixture
# def sample_news(sample_author_with_middle_name, sample_author_without_middle_name, sample_magazine):
#     news = News(
#         id=1,
#         title="Новость 1",
#         publication_date=date(2023, 10, 1),
#         description="Описание новости 1",
#         magazine=sample_magazine,
#         content="Контент новости 1",
#         materials="kitchen.jpg"
#     )
#     news.authors.extend([sample_author_with_middle_name, sample_author_without_middle_name])
#     return news

# @fixture
# def sample_event():
#     return Event(
#         id=1,
#         title="Событие 1",
#         date=date(2023, 10, 15),
#         time=time(14, 0),
#         location="Москва",
#         description="Описание события 1"
#     )

# @fixture
# def sample_project(sample_author_with_middle_name):
#     project = Project(
#         id=1,
#         title="Проект 1",
#         publication_date=date(2023, 9, 1),
#         description="Описание проекта 1",
#         content="Контент проекта 1",
#         materials="loqiemean-как-у-людеи.mp3"
#     )
#     project.authors.extend([sample_author_with_middle_name])
#     return project

# @fixture
# def sample_publication(sample_author_with_middle_name, sample_author_without_middle_name, sample_magazine):
#     publication = Publications(
#         id=1,
#         title="Публикация 1",
#         publication_date=date(2023, 8, 1),
#         annotation="Аннотация публикации 1",
#     )
#     publication.authors.extend([sample_author_with_middle_name, sample_author_without_middle_name])
#     publication.magazine = sample_magazine
#     return publication

# @fixture
# def sample_organisation():
#     return Organisation(
#         id=1,
#         image="kitchen.jpg",
#         link="https://t.me/vyshkochka"
#     )



# @fixture
# def app_testing():
#     #app.config['WTF_CSRF_ENABLED'] = False
#     app = create_app('app.config.TestConfig')
#     with app.app_context():
#         #db.create_all()
#         yield app
#         db.session.remove()
#         db.drop_all()

# @fixture
# def client(app_testing):
#     return app_testing.test_client()



# @fixture
# def route_organisation():
#     org = Organisation(image='image1.png', link='https://org1.com')
#     db.session.add(org)
#     db.session.commit()
#     return org

# @fixture
# def route_contact():
#     contact = Contact(
#         name='Leo Livshitz',
#         email='Leolivshitz@gmail.com',
#         phone='1234567890',
#         message='Hello, World!'
#     )
#     db.session.add(contact)
#     db.session.commit()
#     return contact

# @fixture
# def route_event():
#     event = Event(
#         title='Event1',
#         description='Description1',
#         date=date(2023, 10, 1),
#         time=time(10, 0),
#         location='Location1'
#     )
#     db.session.add(event)
#     db.session.commit()
#     return event

# @fixture
# def route_news():
#     news = News(
#         title='News1',
#         description='Description1',
#         publication_date=datetime(2023, 10, 1),
#         content='Content1'
#     )
#     db.session.add(news)
#     db.session.commit()
#     return news

# @fixture
# def route_project():
#     project = Project(
#         title='Project1',
#         description='Description1',
#         publication_date=datetime(2023, 10, 1),
#         content='Content1'
#     )
#     db.session.add(project)
#     db.session.commit()
#     return project

# @fixture
# def route_publication():
#     publication = Publications(
#         title='Publication1',
#         annotation='Annotation1',
#         publication_date=datetime(2023, 10, 1)
#     )
#     db.session.add(publication)
#     db.session.commit()
#     return publication

# @fixture
# def route_author():
#     author = Author(first_name='Leo', last_name='Livshitz')
#     db.session.add(author)
#     db.session.commit()
#     return author

# @fixture
# def route_magazine():
#     magazine = Magazine(name='Magazine1')
#     db.session.add(magazine)
#     db.session.commit()
#     return magazine



from pytest import fixture
from datetime import datetime, date, time
import sys
from pathlib import Path
from sqlalchemy.exc import SQLAlchemyError

root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

from app.models import (
    Author,
    News,
    Event,
    Project,
    Publications,
    Organisation,
    Magazine,
    Contact,
    db,
)
from app import create_app


@fixture
def sample_author_with_middle_name():
    return Author(
        id=1,
        last_name="Иванов",
        first_name="Иван",
        middle_name="Иванович",
    )


@fixture
def sample_author_without_middle_name():
    return Author(
        id=2,
        last_name="Петров",
        first_name="Петр",
        middle_name=None,
    )


@fixture
def sample_magazine():
    return Magazine(id=1, name="Журнал 1")


@fixture
def sample_news(sample_author_with_middle_name, sample_author_without_middle_name, sample_magazine):
    news = News(
        id=1,
        title="Новость 1",
        publication_date=date(2023, 10, 1),
        description="Описание новости 1",
        magazine=sample_magazine,
        content="Контент новости 1",
        materials="kitchen.jpg",
    )
    news.authors.extend([sample_author_with_middle_name, sample_author_without_middle_name])
    return news


@fixture
def sample_event():
    return Event(
        id=1,
        title="Событие 1",
        date=date(2023, 10, 15),
        time=time(14, 0),
        location="Москва",
        description="Описание события 1",
    )


@fixture
def sample_project(sample_author_with_middle_name):
    project = Project(
        id=1,
        title="Проект 1",
        publication_date=date(2023, 9, 1),
        description="Описание проекта 1",
        content="Контент проекта 1",
        materials="loqiemean-как-у-людеи.mp3",
    )
    project.authors.extend([sample_author_with_middle_name])
    return project


@fixture
def sample_publication(sample_author_with_middle_name, sample_author_without_middle_name, sample_magazine):
    publication = Publications(
        id=1,
        title="Публикация 1",
        publication_date=date(2023, 8, 1),
        annotation="Аннотация публикации 1",
    )
    publication.authors.extend([sample_author_with_middle_name, sample_author_without_middle_name])
    publication.magazine = sample_magazine
    return publication


@fixture
def sample_organisation():
    return Organisation(
        id=1,
        image="kitchen.jpg",
        link="https://t.me/vyshkochka",
    )


@fixture
def app_testing():
    app = create_app("app.config.TestConfig")
    with app.app_context():
        try:
            db.create_all()
            yield app
        finally:
            db.session.remove()
            db.drop_all()


@fixture
def client(app_testing):
    return app_testing.test_client()


@fixture
def route_organisation():
    org = Organisation(image="image1.png", link="https://org1.com")
    db.session.add(org)
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise Exception(f"Ошибка при добавлении организации: {e}")
    return db.session.get(Organisation, org.id)


@fixture
def route_contact():
    data = {
        "name": "Leo Livshitz",
        "email": "Leolivshitz@gmail.com",
        "phone": "1234567890",
        "message": "Hello, World!",
    }
    # Проверяем наличие обязательных полей
    required_fields = ["name", "email", "phone", "message"]
    if not all(field in data for field in required_fields):
        raise ValueError("Отсутствуют обязательные поля для создания контакта")

    contact = Contact(**data)
    db.session.add(contact)
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise Exception(f"Ошибка при добавлении контакта: {e}")
    return db.session.get(Contact, contact.id)


@fixture
def route_event():
    event = Event(
        title="Event1",
        description="Description1",
        date=date(2023, 10, 1),
        time=time(10, 0),
        location="Location1",
    )
    db.session.add(event)
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise Exception(f"Ошибка при добавлении события: {e}")
    return db.session.get(Event, event.id)


@fixture
def route_news():
    news = News(
        title="News1",
        description="Description1",
        publication_date=datetime(2023, 10, 1),
        content="Content1",
    )
    db.session.add(news)
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise Exception(f"Ошибка при добавлении новости: {e}")
    return db.session.get(News, news.id)


@fixture
def route_project():
    project = Project(
        title="Project1",
        description="Description1",
        publication_date=datetime(2023, 10, 1),
        content="Content1",
    )
    db.session.add(project)
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise Exception(f"Ошибка при добавлении проекта: {e}")
    return db.session.get(Project, project.id)


@fixture
def route_publication():
    publication = Publications(
        title="Publication1",
        annotation="Annotation1",
        publication_date=datetime(2023, 10, 1),
    )
    db.session.add(publication)
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise Exception(f"Ошибка при добавлении публикации: {e}")
    return db.session.get(Publications, publication.id)


@fixture
def route_author():
    author = Author(first_name="Leo", last_name="Livshitz")
    db.session.add(author)
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise Exception(f"Ошибка при добавлении автора: {e}")
    return db.session.get(Author, author.id)


@fixture
def route_magazine():
    magazine = Magazine(name="Magazine1")
    db.session.add(magazine)
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise Exception(f"Ошибка при добавлении журнала: {e}")
    return db.session.get(Magazine, magazine.id)