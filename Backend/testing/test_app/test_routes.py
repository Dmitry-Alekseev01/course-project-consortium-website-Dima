from datetime import datetime, date, time
from sqlite3 import IntegrityError
from unittest.mock import MagicMock, patch
from unittest.mock import patch, MagicMock
from flask_mail import Message
from app.routes import get_and_sort_results, send_email
from app import mail
import pytest
from app.models import (
    Organisation,
    Contact,
    Event,
    News,
    Project,
    Publications,
    Author,
    Magazine,
    db
)

class TestOrganisationRoutes:
    def test_get_organisations(self, client, route_organisation):
        # Выполняем запрос
        response = client.get('/api/organisations')
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 1
        assert data[0]['link'] == 'https://org1.com'

    def test_get_organisation_by_id(self, client, route_organisation):
        # Выполняем запрос
        response = client.get(f'/api/organisations/{route_organisation.id}')
        assert response.status_code == 200
        data = response.get_json()
        assert data['link'] == 'https://org1.com'

    def test_get_organisation_by_id_not_found(self, client):
        # Выполняем запрос с несуществующим ID
        response = client.get('/api/organisations/9999')
        assert response.status_code == 404
        data = response.get_json()
        assert data['error'] == 'Организация не найдена'


# class TestContactRoutes:
#     def test_create_contact(self, client):
#         # Данные для создания контакта
#         data = {
#             'name': 'Leo Livshitz',
#             'email': 'Leolivshitz@gmail.com',
#             'phone': '1234567890',
#             'message': 'Hello, World!'
#         }
#         # Выполняем запрос
#         response = client.post('/api/contact', json=data)
#         assert response.status_code == 201
#         data = response.get_json()
#         assert data['message'] == 'Сообщение отправлено успешно!'

# class TestContactRoutes:
#     def test_create_contact(self, client, app_testing, mock_contact_data):
#         with app_testing.app_context():
#             with mail.record_messages() as outbox:
#                 # Выполняем запрос с моковыми данными
#                 response = client.post('/api/contact', json=mock_contact_data)
#                 assert response.status_code == 201
#                 data = response.get_json()
#                 assert data['message'] == 'Сообщение отправлено успешно!'

#                 # Проверяем, что сообщение было отправлено
#                 assert len(outbox) == 1
#                 sent_message = outbox[0]
#                 assert sent_message.subject == f"Новое сообщение от {mock_contact_data['name']}"
#                 assert sent_message.sender == mock_contact_data['email']
#                 assert sent_message.recipients == ['maxweinsberg25@gmail.com']
#                 assert f"Имя: {mock_contact_data['name']}" in sent_message.body
#                 assert f"Email: {mock_contact_data['email']}" in sent_message.body
#                 assert f"Телефон: {mock_contact_data['phone']}" in sent_message.body
#                 assert f"Сообщение: {mock_contact_data['message']}" in sent_message.body

#     def test_create_contact_without_email(self, client, app_testing, mock_contact_data):
#         with app_testing.app_context():
#             with mail.record_messages() as outbox:
#                 # Удаляем обязательное поле email
#                 invalid_data = mock_contact_data.copy()
#                 invalid_data["email"] = "invalid_email"

#                 # Выполняем запрос
#                 response = client.post('/api/contact', json=invalid_data)
#                 assert response.status_code == 400  # Ожидаем ошибку из-за невалидного email
#                 assert len(outbox) == 0  # Проверяем, что сообщение не было отправлено

#     def test_create_incorrect(self, client_mail, mock_contact_data):
#         #with app_testing_mail.app_context():
        
#         response = client_mail.post('/api/contact', json=mock_contact_data)
#         assert response.status_code == 200
                

class TestContactRoutes:
    def test_create_contact_success(self, client, app_testing, mock_contact_data):
        with app_testing.app_context(), mail.record_messages() as outbox:
            response = client.post('/api/contact', json=mock_contact_data)
            assert response.status_code == 201
            data = response.get_json()
            assert data['message'] == 'Сообщение отправлено успешно!'
            
            # Проверка сохранения в БД
            contact = Contact.query.first()
            assert contact.email == mock_contact_data['email']
            assert contact.message == mock_contact_data['message']
            
            # Проверка отправки email
            assert len(outbox) == 1
            sent_msg = outbox[0]
            assert mock_contact_data['email'] in sent_msg.body
            assert 'не указано' in sent_msg.body  # Для пустого company

    def test_create_contact_duplicate(self, client, app_testing, mock_contact_data):
        with app_testing.app_context():
            # Первое успешное создание
            client.post('/api/contact', json=mock_contact_data)
            
            # Попытка создать дубликат
            response = client.post('/api/contact', json=mock_contact_data)
            assert response.status_code == 409
            assert 'уже отправлено' in response.get_json()['error']

    def test_create_contact_missing_fields(self, client, app_testing):
        test_cases = [
            ({'email': 'test@test.com'}, 'Missing required fields'),
            ({'name': 'Test'}, 'Missing required fields'),
            ({}, 'Missing required fields')
        ]
        
        for data, error_msg in test_cases:
            response = client.post('/api/contact', json=data)
            assert response.status_code == 400
            assert error_msg in response.get_json()['error']

    def test_create_contact_invalid_email(self, client, app_testing, mock_contact_data):
        invalid_data = mock_contact_data.copy()
        invalid_data['email'] = 'invalid-email'
        
        response = client.post('/api/contact', json=invalid_data)
        assert response.status_code == 400
        assert 'Invalid email' in response.get_json()['error']

    def test_create_contact_email_sending_failure(self, client_mail, mock_contact_data):
        with patch('app.routes.send_email') as mock_send:
            mock_send.return_value = False
            
            response = client_mail.post('/api/contact', json=mock_contact_data)
            assert response.status_code == 500
            data = response.get_json()
            assert 'сохранено, но не отправлено' in data['error']
            
            # Проверка сохранения в БД
            contact = Contact.query.first()
            assert contact is not None

    def test_create_contact_database_integrity_error(self, client, app_testing, mock_contact_data):
        with app_testing.app_context():
            # Мокируем ошибку целостности БД
            with patch('app.routes.db.session.commit') as mock_commit:
                mock_commit.side_effect = IntegrityError("Integrity Error", "params", "orig")
                
                response = client.post('/api/contact', json=mock_contact_data)
                assert response.status_code == 500
                data = response.get_json()
                assert 'Database error' in data['error']

    def test_create_contact_email_exception(self, client_mail, mock_contact_data):
        with patch('app.routes.send_email') as mock_send:
            mock_send.side_effect = Exception("SMTP Error")
            
            response = client_mail.post('/api/contact', json=mock_contact_data)
            assert response.status_code == 500
            data = response.get_json()
            assert 'сохранено, но не отправлено' in data['error']
            
            contact = Contact.query.first()
            assert contact is not None


class TestEmailSending:
    @patch('app.routes.mail')
    def test_send_email_success(self, mock_mail):
        mock_mail.send = MagicMock(return_value=None)
        
        result = send_email(
            subject="Test Subject",
            sender="test@example.com",
            recipients=["recipient@example.com"],
            body="Test Body"
        )
        
        assert result is True
        mock_mail.send.assert_called_once()
        msg = mock_mail.send.call_args[0][0]
        assert isinstance(msg, Message)
        assert msg.subject == "Test Subject"
        assert msg.sender == "test@example.com"
        assert msg.recipients == ["recipient@example.com"]
        assert msg.body == "Test Body"

    @patch('app.routes.mail')
    @pytest.mark.parametrize("exception, error_message", [
        (Exception("SMTP error"), "SMTP error"),
        (ConnectionError("Connection failed"), "Connection failed"),
        (TimeoutError("Server timeout"), "Server timeout"),
    ])
    def test_send_email_failure(self, mock_mail, exception, error_message):
        mock_mail.send = MagicMock(side_effect=exception)
        
        result = send_email(
            subject="Test Subject",
            sender="test@example.com",
            recipients=["recipient@example.com"],
            body="Test Body"
        )
        
        assert result is False
        mock_mail.send.assert_called_once()

    @patch('app.routes.mail')
    @patch('app.routes.logging.error')
    def test_send_email_logging(self, mock_logging, mock_mail):
        test_exception = Exception("Test error message")
        mock_mail.send = MagicMock(side_effect=test_exception)
        
        send_email(
            subject="Test",
            sender="test@example.com",
            recipients=["to@example.com"],
            body="Body"
        )
        
        expected_log_message = "Ошибка при отправке email: Test error message"
        mock_logging.assert_called_once_with(expected_log_message)

    @patch('app.routes.mail')
    @patch('app.routes.Message')
    def test_message_creation_failure(self, mock_message, mock_mail):

        mock_message.side_effect = ValueError("Invalid message parameters")

        result = send_email(
            subject="Invalid Subject",
            sender="invalid_sender",
            recipients=[],
            body=""
        )
        
        assert result is False
        mock_message.assert_called_once_with(
            "Invalid Subject",
            sender="invalid_sender",
            recipients=[]
        )
        mock_mail.send.assert_not_called()



class TestEventRoutes:
    def test_get_events(self, client, route_event):
        # Выполняем запрос
        response = client.get('/api/events')
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 1
        assert data[0]['title'] == 'Event1'

    def test_get_event_by_id(self, client, route_event):
        # Выполняем запрос
        response = client.get(f'/api/events/{route_event.id}')
        assert response.status_code == 200
        data = response.get_json()
        assert data['title'] == 'Event1'

    def test_get_event_by_id_not_found(self, client):
        # Выполняем запрос с несуществующим ID
        response = client.get('/api/events/9999')
        assert response.status_code == 404
        data = response.get_json()
        assert data['error'] == 'Событие не найдено'


class TestNewsRoutes:
    def test_get_news(self, client, route_news):
        # Выполняем запрос
        response = client.get('/api/news')
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 1
        assert data[0]['title'] == 'News1'

    def test_get_news_by_id(self, client, route_news):
        # Выполняем запрос
        response = client.get(f'/api/news/{route_news.id}')
        assert response.status_code == 200
        data = response.get_json()
        assert data['title'] == 'News1'

    def test_get_news_by_id_not_found(self, client):
        # Выполняем запрос с несуществующим ID
        response = client.get('/api/news/9999')
        assert response.status_code == 404
        data = response.get_json()
        assert data['error'] == 'Новость не найдена'


class TestProjectRoutes:
    def test_get_projects(self, client, route_project):
        # Выполняем запрос
        response = client.get('/api/projects')
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 1
        assert data[0]['title'] == 'Project1'

    def test_get_project_by_id(self, client, route_project):
        # Выполняем запрос
        response = client.get(f'/api/projects/{route_project.id}')
        assert response.status_code == 200
        data = response.get_json()
        assert data['title'] == 'Project1'

    def test_get_project_by_id_not_found(self, client):
        # Выполняем запрос с несуществующим ID
        response = client.get('/api/projects/999')
        assert response.status_code == 404
        data = response.get_json()
        assert data['error'] == 'Проект не найден'


class TestPublicationRoutes:
    def test_get_publications(self, client, route_publication):
        # Выполняем запрос
        response = client.get('/api/publications')
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 1
        assert data[0]['title'] == 'Publication1'

    def test_get_publication_by_id(self, client, route_publication):
        # Выполняем запрос
        response = client.get(f'/api/publications/{route_publication.id}')
        assert response.status_code == 200
        data = response.get_json()
        assert data['title'] == 'Publication1'

    def test_get_publication_by_id_not_found(self, client):
        # Выполняем запрос с несуществующим ID
        response = client.get('/api/publications/9999')
        assert response.status_code == 404
        data = response.get_json()
        assert data['error'] == 'Публикация не найдена'


class TestAuthorRoutes:
    def test_get_authors(self, client, route_author):
        # Выполняем запрос
        response = client.get('/api/authors')
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 1
        assert data[0]['first_name'] == 'Leo'

    def test_get_author_by_id(self, client, route_author):
        # Выполняем запрос
        response = client.get(f'/api/authors/{route_author.id}')
        assert response.status_code == 200
        data = response.get_json()
        assert data['first_name'] == 'Leo'
        assert data['last_name'] == 'Livshitz'

    def test_get_author_by_id_not_found(self, client):
        # Выполняем запрос с несуществующим ID
        response = client.get('/api/authors/999')
        assert response.status_code == 404
        data = response.get_json()
        assert data['error'] == 'автор не найден'


class TestMagazineRoutes:
    def test_get_magazines(self, client, route_magazine):
        # Выполняем запрос
        response = client.get('/api/magazines')
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 1
        assert data[0]['name'] == 'Magazine1'

    def test_get_magazine_by_id(self, client, route_magazine):
        # Выполняем запрос
        response = client.get(f'/api/magazines/{route_magazine.id}')
        assert response.status_code == 200
        data = response.get_json()
        assert data['name'] == 'Magazine1'

    def test_get_magazine_by_id_not_found(self, client):
        # Выполняем запрос с несуществующим ID
        response = client.get('/api/magazines/999')
        assert response.status_code == 404
        data = response.get_json()
        assert data['error'] == 'магазин не найден'
    

class TestSearchRoutes:
    def test_search_all_types(self, client, sample_news, sample_publication, sample_event, sample_project, sample_organisation):
        # Добавляем тестовые данные в БД
        db.session.add_all([sample_news, sample_publication, sample_event, sample_project, sample_organisation])
        db.session.commit()

        response = client.get('/api/search?q=1')
        assert response.status_code == 200
        data = response.json

        # Проверяем наличие всех категорий
        assert len(data['news']) == 1
        assert len(data['publications']) == 1
        assert len(data['events']) == 1
        assert len(data['projects']) == 1
        assert len(data['organisations']) == 1

    def test_search_with_authors_filter(self, client, sample_news, sample_publication, sample_project, sample_author_with_middle_name):
        # Настраиваем авторов
        author_id = sample_author_with_middle_name.id
        db.session.add_all([sample_news, sample_publication, sample_project])
        db.session.commit()

        response = client.get(f'/api/search?q=1&authors[]={author_id}')
        assert response.status_code == 200
        data = response.get_json()

        # Проверяем фильтрацию по автору
        assert len(data['news']) == 1
        assert len(data['publications']) == 1
        assert len(data['projects']) == 1

    def test_search_with_magazines_filter(self, client, sample_news, sample_publication, sample_magazine):
        magazine_id = sample_magazine.id
        db.session.add_all([sample_news, sample_publication])
        db.session.commit()

        response = client.get(f'/api/search?q=1&magazines[]={magazine_id}')
        assert response.status_code == 200
        data = response.get_json()

        assert len(data['news']) == 1
        assert len(data['publications']) == 1

    def test_search_with_date_filter(self, client, sample_news, sample_publication, sample_event, sample_project):
        db.session.add_all([sample_news, sample_publication, sample_event, sample_project])
        db.session.commit()

        response = client.get('/api/search?q=1&date_from=2023-01-01&date_to=2023-12-31')
        assert response.status_code == 200
        data = response.get_json()

        assert len(data['news']) == 1
        assert len(data['publications']) == 1
        assert len(data['events']) == 1
        assert len(data['projects']) == 1

class TestSearchFunctions:
    def test_search_empty_category(self, client):
        response = client.get('/api/search?q=fakequery')

        assert response.status_code == 200

        data = response.get_json()

        assert data["news"] == []
        assert data["publications"] == []
        assert data["projects"] == []
        assert data["events"] == []
        assert data["organisations"] == []
        
    def test_search_empty_query(self, client):
        response = client.get('/api/search?q=')
        assert response.status_code == 400
        data = response.get_json()
        assert data['error'] == "Пустой запрос"
    def test_sort_by_date(self, client):
        news1 = News(
            title="News 1",
            publication_date=datetime(2023, 10, 2),  # Используем datetime
            description="Description 1",
            content="Content 1"
        )
        news2 = News(
            title="News 2",
            publication_date=datetime(2023, 10, 1),  # Используем datetime
            description="Description 2",
            content="Content 2"
        )
        db.session.add_all([news1, news2])
        db.session.commit()

        results = get_and_sort_results(News, [News.title.ilike("%News%")], sort_key='publication_date', reverse=False)
        # Преобразуем datetime к date для сравнения
        assert [n.publication_date.date() for n in results] == [date(2023, 10, 1), date(2023, 10, 2)]


# class TestSearchRoutes:
#     def test_get_and_sort_results_without_sort(self, mock_news_for_search, mock_filters_for_search):
#         with patch('app.models.db.session.scalars') as mock_scalars:
#             mock_scalars.return_value.all.return_value = [mock_news_for_search]

#             # Вызываем функцию без сортировки
#             results = get_and_sort_results(News, mock_filters_for_search)

#             assert len(results) == 1
#             assert results[0].title == "Test News"

#     def test_get_and_sort_results_with_sort(self, mock_news_for_search, mock_filters_for_search):
#         with patch('app.models.db.session.scalars') as mock_scalars:
#             mock_scalars.return_value.all.return_value = [mock_news_for_search]

#             # Вызываем функцию с сортировкой по title
#             results = get_and_sort_results(News, mock_filters_for_search, sort_key='title', reverse=False)

#             assert len(results) == 1
#             assert results[0].title == "Test News"

#     def test_get_and_sort_results_with_reverse_sort(self, mock_news_for_search, mock_filters_for_search):
#         with patch('app.models.db.session.scalars') as mock_scalars:
#             mock_scalars.return_value.all.return_value = [mock_news_for_search]

#             # Вызываем функцию с сортировкой по title в обратном порядке
#             results = get_and_sort_results(News, mock_filters_for_search, sort_key='title', reverse=True)

#             assert len(results) == 1
#             assert results[0].title == "Test News"

#     def test_get_and_sort_results_with_date_sort(self, mock_news_for_search, mock_filters_for_search):
#         with patch('app.models.db.session.scalars') as mock_scalars:
#             mock_scalars.return_value.all.return_value = [mock_news_for_search]

#             # Вызываем функцию с сортировкой по дате
#             results = get_and_sort_results(News, mock_filters_for_search, sort_key='publication_date', reverse=False)

#             # Проверяем, что результаты возвращены корректно
#             assert len(results) == 1
#             assert results[0].publication_date == "2023-10-01"

#     def test_search_all_types(self, client, mock_db_session, mock_news, mock_publications, mock_project, mock_event, mock_organisation, mock_author, mock_magazine):
#         # mock_scalars = MagicMock()
#         # mock_scalars.all.side_effect = [
#         #     [mock_news],
#         #     [mock_publications],
#         #     [mock_project],
#         #     [mock_event],
#         #     [mock_organisation],
#         #     [mock_author],
#         #     [mock_magazine]
#         # ]
#         # mock_db_session.scalars.return_value = mock_scalars

#         # Выполняем запрос на поиск
#         response = client.get('/api/search?q=Test')
#         assert response.status_code == 200
#         data = response.get_json()

#         # Проверяем результаты поиска
#         # assert len(data['news']) == 1
#         # assert len(data['publications']) == 1
#         # assert len(data['projects']) == 1
#         # assert len(data['events']) == 1
#         # assert len(data['organisations']) == 1
#         # assert len(data['authors']) == 1
#         # assert len(data['magazines']) == 1

#     def test_search_empty_query(self, client):
#         response = client.get('/api/search?q=')
#         assert response.status_code == 400

#     def test_search_empty_q(self, client):
#         response = client.get('/api/search?')
#         assert response.status_code == 400


#     def test_search_with_authors_filter(self, client, mock_db_session, mock_news, mock_publications, mock_project, mock_event):
#         # mock_scalars = MagicMock()
#         # mock_scalars.all.side_effect = [
#         #     [mock_news],
#         #     [mock_publications],
#         #     [mock_project],
#         #     [mock_event],
#         #     [],  # Организации
#         #     [],  # Авторы
#         #     []   # Журналы
#         # ]
#         # mock_db_session.scalars.return_value = mock_scalars

#         response = client.get('/api/search?q=Test&authors[]=1&authors[]=2')
#         assert response.status_code == 200
#         data = response.get_json()

#         # assert len(data['news']) == 1
#         # assert len(data['publications']) == 1
#         # assert len(data['projects']) == 1
#         # assert len(data['events']) == 1
#         # assert len(data['organisations']) == 0
#         # assert len(data['authors']) == 0
#         # assert len(data['magazines']) == 0

#     def test_search_with_magazines_filter(self, client, mock_db_session, mock_news, mock_publications):
#         # mock_scalars = MagicMock()
#         # mock_scalars.all.side_effect = [
#         #     [mock_news],
#         #     [mock_publications],
#         #     [],  # Проекты
#         #     [],  # Организации
#         #     [],  # Авторы
#         #     [],   # Журналы
#         #     []
#         # ]
#         # mock_db_session.scalars.return_value = mock_scalars

#         response = client.get('/api/search?q=Test&magazines[]=1&magazines[]=2')
#         assert response.status_code == 200
#         data = response.get_json()

#         # assert len(data['news']) == 1
#         # assert len(data['publications']) == 1
#         # assert len(data['projects']) == 0
#         # assert len(data['organisations']) == 0
#         # assert len(data['authors']) == 0
#         # assert len(data['magazines']) == 0

#     def test_search_with_date_filter(self, client, mock_db_session, mock_news, mock_publications, mock_event, mock_project):
#         # mock_scalars = MagicMock()
#         # mock_scalars.all.side_effect = [
#         #     [mock_news],
#         #     [mock_publications],
#         #     [mock_project],
#         #     [mock_event],
#         #     [],
#         #     [],
#         #     []
#         # ]
#         # mock_db_session.scalars.return_value = mock_scalars

#         response = client.get('/api/search?q=Test&date_from=2023-01-01&date_to=2023-12-31')
#         assert response.status_code == 200
#         data = response.get_json()

#         # assert len(data['news']) == 1
#         # assert len(data['publications']) == 1
#         # assert len(data['projects']) == 1
#         # assert len(data['events']) == 1
#         # assert len(data['organisations']) == 0
#         # assert len(data['authors']) == 0
#         # assert len(data['magazines']) == 0

#     def test_search_with_combined_filters(self, client, mock_db_session, mock_news, mock_publications):

#         # mock_scalars = MagicMock()
#         # mock_scalars.all.side_effect = [
#         #     [mock_news],  # Новости
#         #     [mock_publications],  # Публикации
#         #     [],  # Проекты
#         #     [],  # Организации
#         #     [],  # Авторы
#         #     [],  # Журналы
#         #     []   # Что-то там еще
#         # ]
#         # mock_db_session.scalars.return_value = mock_scalars

#         response = client.get('/api/search?q=Test&authors[]=1&magazines[]=1&date_from=2023-01-01&date_to=2023-12-31')
#         assert response.status_code == 200
#         data = response.get_json()

#         # assert len(data['news']) == 1
#         # assert len(data['publications']) == 1
#         # assert len(data['projects']) == 0
#         # assert len(data['events']) == 0
#         # assert len(data['organisations']) == 0
#         # assert len(data['authors']) == 0
#         # assert len(data['magazines']) == 0

#     def test_search_with_no_results(self, client, mock_db_session):
#         # Пустые результаты
#         mock_scalars = MagicMock()
#         mock_scalars.all.side_effect = [
#             [],
#             [],
#             [],
#             [],
#             [],
#             [],
#             []
#         ]
#         mock_db_session.scalars.return_value = mock_scalars

#         response = client.get('/api/search?q=Test&authors[]=999&magazines[]=999&date_from=2025-01-01&date_to=2025-12-31')
#         assert response.status_code == 200
#         data = response.get_json()

#         assert len(data['news']) == 0
#         assert len(data['publications']) == 0
#         assert len(data['projects']) == 0
#         assert len(data['events']) == 0
#         assert len(data['organisations']) == 0
#         assert len(data['authors']) == 0
#         assert len(data['magazines']) == 0

class TestUploadsFile:
    def test_uploaded_wrong_file(self, client):
        response = client.get("/api/uploads/goal")
        assert response.status_code == 404
    def test_uploaded_correct_file(self, client, uploaded_organisation):
        response = client.get(f"/api/uploads/{uploaded_organisation.image}")
        assert response.status_code == 200
        