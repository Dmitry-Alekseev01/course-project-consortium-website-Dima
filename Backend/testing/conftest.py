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

from flask_mail import Mail
from unittest.mock import MagicMock, patch
from pytest import fixture
from datetime import datetime, date, time
import sys
from pathlib import Path
from sqlalchemy.exc import SQLAlchemyError
from flask_admin import Admin

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
from app import MyModelView, create_app


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
def news_view():
    """Создаем экземпляр MyModelView для модели News."""
    return MyModelView(News, db.session)

@fixture
def event_view():
    """Создаем экземпляр MyModelView для модели Event."""
    return MyModelView(Event, db.session)

@fixture
def sample_event():
    return Event(
        id=1,
        title="Событие 1",
        publication_date=date(2023, 10, 1),
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
        link="https://t.me/vyshkochka1",
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

# @fixture
# def admin_client(client):
#     """Клиент с авторизацией для тестирования админки"""
#     credentials = base64.b64encode(b"admin:password").decode()
#     client.environ_base['HTTP_AUTHORIZATION'] = f'Basic {credentials}'
#     return client


@fixture
def route_organisation():
    org = Organisation(image="image1.png", link="https://org1.com")
    db.session.add(org)
    db.session.commit()
    # try:
    #     db.session.commit()
    # except SQLAlchemyError as e:
    #     db.session.rollback()
    #     raise Exception(f"Ошибка при добавлении организации: {e}")
    return db.session.get(Organisation, org.id)


# @fixture
# def route_contact():
#     data = {
#         "name": "Leo Livshitz",
#         "email": "Leolivshitz@gmail.com",
#         "phone": "1234567890",
#         "message": "Hello, World!",
#     }
#     # Проверяем наличие обязательных полей
#     required_fields = ["name", "email", "phone", "message"]
#     if not all(field in data for field in required_fields):
#         raise ValueError("Отсутствуют обязательные поля для создания контакта")

#     contact = Contact(**data)
#     db.session.add(contact)
#     db.session.commit()
#     # try:
#     #     db.session.commit()
#     # except SQLAlchemyError as e:
#     #     db.session.rollback()
#     #     raise Exception(f"Ошибка при добавлении контакта: {e}")
#     return db.session.get(Contact, contact.id)


@fixture
def route_event():
    event = Event(
        title="Event1",
        description="Description1",
        publication_date=date(2023, 10, 1),
        location="Location1",
    )
    db.session.add(event)
    db.session.commit()
    # try:
    #     db.session.commit()
    # except SQLAlchemyError as e:
    #     db.session.rollback()
    #     raise Exception(f"Ошибка при добавлении события: {e}")
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
    db.session.commit()
    # try:
    #     db.session.commit()
    # except SQLAlchemyError as e:
    #     db.session.rollback()
    #     raise Exception(f"Ошибка при добавлении новости: {e}")
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
    db.session.commit()
    # try:
    #     db.session.commit()
    # except SQLAlchemyError as e:
    #     db.session.rollback()
    #     raise Exception(f"Ошибка при добавлении проекта: {e}")
    return db.session.get(Project, project.id)


@fixture
def route_publication():
    publication = Publications(
        title="Publication1",
        annotation="Annotation1",
        publication_date=datetime(2023, 10, 1),
    )
    db.session.add(publication)
    db.session.commit()
    # try:
    #     db.session.commit()
    # except SQLAlchemyError as e:
    #     db.session.rollback()
    #     raise Exception(f"Ошибка при добавлении публикации: {e}")
    return db.session.get(Publications, publication.id)


@fixture
def route_author():
    author = Author(first_name="Leo", last_name="Livshitz")
    db.session.add(author)
    db.session.commit()
    # try:
    #     db.session.commit()
    # except SQLAlchemyError as e:
    #     db.session.rollback()
    #     raise Exception(f"Ошибка при добавлении автора: {e}")
    return db.session.get(Author, author.id)


@fixture
def route_magazine():
    magazine = Magazine(name="Magazine1")
    db.session.add(magazine)
    db.session.commit()
    # try:
    #     db.session.commit()
    # except SQLAlchemyError as e:
    #     db.session.rollback()
    #     raise Exception(f"Ошибка при добавлении журнала: {e}")
    return db.session.get(Magazine, magazine.id)


@fixture
def mock_contact_data():
    """Моковые данные для создания контакта"""
    return {
        "name": "Test Contact",
        "email": "leonidlivshits05@gmail.com",
        "phone": "9876543210",
        "message": "This is a test message"
    }

#МОК ДЛЯ ПЕРЕВОДА
@fixture(autouse=True)
def auto_mock_translator(monkeypatch):
    def mock_translate(text, translator=None):
        return f"{text}_en"
    
    #monkeypatch.setattr("app.models.translate_to_english", mock_translate)
    monkeypatch.setattr("app.translator.translate_to_english", mock_translate)
    #yield

# @fixture
# def mock_mail(app_testing):
#     """Мок для отправки email."""
#     with app_testing.app_context():
#         mail = Mail(app_testing)
#         with patch.object(mail, 'send', return_value=True) as mock_send:
#             yield mock_send


# @fixture
# def mock_db_session():
#     """Мок для сессии базы данных."""
#     with patch('app.models.db.session') as mock_session:
#         mock_scalars = MagicMock()
#         mock_scalars.all.return_value = []
#         mock_session.scalars.return_value = mock_scalars
#         yield mock_session

# @fixture
# def mock_contact():
#     """Мок для модели Contact."""
#     contact = MagicMock(spec=Contact)
#     contact.id = 1
#     contact.name = "Test Contact"
#     contact.email = "test@example.com"
#     contact.phone = "1234567890"
#     contact.message = "Test message"
#     return contact

# @fixture
# def mock_news():
#     """Мок для модели News."""
#     news = MagicMock(spec=News)
#     news.id = 1
#     news.title = "Test News"
#     news.description = "Test Description"
#     news.content = "Test Content"
#     return news

# @fixture
# def mock_event():
#     """Мок для модели Event."""
#     event = MagicMock(spec=Event)
#     event.id = 1
#     event.title = "Test Event"
#     event.description = "Test Description"
#     event.location = "Test Location"
#     return event

# @fixture
# def mock_project():
#     """Мок для модели Project."""
#     project = MagicMock(spec=Project)
#     project.id = 1
#     project.title = "Test Project"
#     project.description = "Test Description"
#     project.content = "Test Content"
#     return project

# @fixture
# def mock_publications():
#     """Мок для модели Publications."""
#     publication = MagicMock(spec=Publications)
#     publication.id = 1
#     publication.title = "Test Publication"
#     publication.annotation = "Test Annotation"
#     return publication

# @fixture
# def mock_author():
#     """Мок для модели Author."""
#     author = MagicMock(spec=Author)
#     author.id = 1
#     author.first_name = "Test"
#     author.last_name = "Author"
#     author.middle_name = "Middle"
#     return author

# @fixture
# def mock_magazine():
#     """Мок для модели Magazine."""
#     magazine = MagicMock(spec=Magazine)
#     magazine.id = 1
#     magazine.name = "Test Magazine"
#     return magazine

# @fixture
# def mock_organisation():
#     """Мок для модели Organisation."""
#     organisation = MagicMock(spec=Organisation)
#     organisation.id = 1
#     organisation.link = "https://test.com"
#     return organisation

# @fixture
# def mock_admin():
#     return MagicMock(spec=Admin)

# @fixture
# def mock_db(mock_db_session):
#     db_mock = MagicMock()
#     db_mock.session = mock_db_session
#     return db_mock


@fixture
def uploaded_organisation(sample_organisation):
    org = sample_organisation
    db.session.add(org)
    db.session.commit()
    # try:
    #     db.session.commit()
    # except SQLAlchemyError as e:
    #     db.session.rollback()
    #     raise Exception(f"Ошибка при добавлении организации: {e}")
    return db.session.get(Organisation, org.id)

class MockMail:
    # def send(message, *args, **kwargs):
    #     raise Exception
    def init_app(app, *args, **kwargs):
        pass

@fixture
def app_testing_mail():
    app = create_app("app.config.TestConfig", MockMail())
    with app.app_context():
        try:
            db.create_all()
            yield app
        finally:
            db.session.remove()
            db.drop_all()


@fixture
def client_mail(app_testing_mail):
    return app_testing_mail.test_client()

# @fixture
# def mock_news_for_search():
#     news = News(id=1, title="Test News", publication_date="2023-10-01")
#     return news


# @fixture
# def mock_filters_for_search():
#     return [News.title.ilike("%Test%")]