from datetime import datetime, date, time
from unittest.mock import MagicMock, patch
from app.routes import get_and_sort_results
from app import mail
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

class TestContactRoutes:
    def test_create_contact(self, client, app_testing, mock_contact_data):
        with app_testing.app_context():
            with mail.record_messages() as outbox:
                # Выполняем запрос с моковыми данными
                response = client.post('/api/contact', json=mock_contact_data)
                assert response.status_code == 201
                data = response.get_json()
                assert data['message'] == 'Сообщение отправлено успешно!'

                # Проверяем, что сообщение было отправлено
                assert len(outbox) == 1
                sent_message = outbox[0]
                assert sent_message.subject == f"Новое сообщение от {mock_contact_data['name']}"
                assert sent_message.sender == mock_contact_data['email']
                assert sent_message.recipients == ['maxweinsberg25@gmail.com']
                assert f"Имя: {mock_contact_data['name']}" in sent_message.body
                assert f"Email: {mock_contact_data['email']}" in sent_message.body
                assert f"Телефон: {mock_contact_data['phone']}" in sent_message.body
                assert f"Сообщение: {mock_contact_data['message']}" in sent_message.body

    def test_create_contact_without_email(self, client, app_testing, mock_contact_data):
        with app_testing.app_context():
            with mail.record_messages() as outbox:
                # Удаляем обязательное поле email
                invalid_data = mock_contact_data.copy()
                invalid_data["email"] = "invalid_email"

                # Выполняем запрос
                response = client.post('/api/contact', json=invalid_data)
                assert response.status_code == 400  # Ожидаем ошибку из-за невалидного email
                assert len(outbox) == 0  # Проверяем, что сообщение не было отправлено

    def test_create_incorrect(self, client_mail, mock_contact_data):
        #with app_testing_mail.app_context():
        
        response = client_mail.post('/api/contact', json=mock_contact_data)
        assert response.status_code == 200
                

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


class TestMagazineRoutes:
    def test_get_magazines(self, client, route_magazine):
        # Выполняем запрос
        response = client.get('/api/magazines')
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 1
        assert data[0]['name'] == 'Magazine1'


class TestSearchRoutes:
    def test_get_and_sort_results_without_sort(self, mock_news_for_search, mock_filters_for_search):
        with patch('app.models.db.session.scalars') as mock_scalars:
            mock_scalars.return_value.all.return_value = [mock_news_for_search]

            # Вызываем функцию без сортировки
            results = get_and_sort_results(News, mock_filters_for_search)

            assert len(results) == 1
            assert results[0].title == "Test News"

    def test_get_and_sort_results_with_sort(self, mock_news_for_search, mock_filters_for_search):
        with patch('app.models.db.session.scalars') as mock_scalars:
            mock_scalars.return_value.all.return_value = [mock_news_for_search]

            # Вызываем функцию с сортировкой по title
            results = get_and_sort_results(News, mock_filters_for_search, sort_key='title', reverse=False)

            assert len(results) == 1
            assert results[0].title == "Test News"

    def test_get_and_sort_results_with_reverse_sort(self, mock_news_for_search, mock_filters_for_search):
        with patch('app.models.db.session.scalars') as mock_scalars:
            mock_scalars.return_value.all.return_value = [mock_news_for_search]

            # Вызываем функцию с сортировкой по title в обратном порядке
            results = get_and_sort_results(News, mock_filters_for_search, sort_key='title', reverse=True)

            assert len(results) == 1
            assert results[0].title == "Test News"

    def test_get_and_sort_results_with_date_sort(self, mock_news_for_search, mock_filters_for_search):
        with patch('app.models.db.session.scalars') as mock_scalars:
            mock_scalars.return_value.all.return_value = [mock_news_for_search]

            # Вызываем функцию с сортировкой по дате
            results = get_and_sort_results(News, mock_filters_for_search, sort_key='publication_date', reverse=False)

            # Проверяем, что результаты возвращены корректно
            assert len(results) == 1
            assert results[0].publication_date == "2023-10-01"

    def test_search_all_types(self, client, mock_db_session, mock_news, mock_publications, mock_project, mock_event, mock_organisation, mock_author, mock_magazine):
        mock_scalars = MagicMock()
        mock_scalars.all.side_effect = [
            [mock_news],
            [mock_publications],
            [mock_project],
            [mock_event],
            [mock_organisation],
            [mock_author],
            [mock_magazine]
        ]
        mock_db_session.scalars.return_value = mock_scalars

        # Выполняем запрос на поиск
        response = client.get('/api/search?q=Test')
        assert response.status_code == 200
        data = response.get_json()

        # Проверяем результаты поиска
        assert len(data['news']) == 1
        assert len(data['publications']) == 1
        assert len(data['projects']) == 1
        assert len(data['events']) == 1
        assert len(data['organisations']) == 1
        assert len(data['authors']) == 1
        assert len(data['magazines']) == 1

    def test_search_empty_query(self, client):
        response = client.get('/api/search?q=')
        assert response.status_code == 400

    def test_search_empty_q(self, client):
        response = client.get('/api/search?')
        assert response.status_code == 400


    def test_search_with_authors_filter(self, client, mock_db_session, mock_news, mock_publications, mock_project, mock_event):
        mock_scalars = MagicMock()
        mock_scalars.all.side_effect = [
            [mock_news],
            [mock_publications],
            [mock_project],
            [mock_event],
            [],  # Организации
            [],  # Авторы
            []   # Журналы
        ]
        mock_db_session.scalars.return_value = mock_scalars

        response = client.get('/api/search?q=Test&authors[]=1&authors[]=2')
        assert response.status_code == 200
        data = response.get_json()

        assert len(data['news']) == 1
        assert len(data['publications']) == 1
        assert len(data['projects']) == 1
        assert len(data['events']) == 1
        assert len(data['organisations']) == 0
        assert len(data['authors']) == 0
        assert len(data['magazines']) == 0

    def test_search_with_magazines_filter(self, client, mock_db_session, mock_news, mock_publications):
        mock_scalars = MagicMock()
        mock_scalars.all.side_effect = [
            [mock_news],
            [mock_publications],
            [],  # Проекты
            [],  # Организации
            [],  # Авторы
            [],   # Журналы
            []
        ]
        mock_db_session.scalars.return_value = mock_scalars

        response = client.get('/api/search?q=Test&magazines[]=1&magazines[]=2')
        assert response.status_code == 200
        data = response.get_json()

        assert len(data['news']) == 1
        assert len(data['publications']) == 1
        assert len(data['projects']) == 0
        assert len(data['organisations']) == 0
        assert len(data['authors']) == 0
        assert len(data['magazines']) == 0

    def test_search_with_date_filter(self, client, mock_db_session, mock_news, mock_publications, mock_event, mock_project):
        mock_scalars = MagicMock()
        mock_scalars.all.side_effect = [
            [mock_news],
            [mock_publications],
            [mock_project],
            [mock_event],
            [],
            [],
            []
        ]
        mock_db_session.scalars.return_value = mock_scalars

        response = client.get('/api/search?q=Test&date_from=2023-01-01&date_to=2023-12-31')
        assert response.status_code == 200
        data = response.get_json()

        assert len(data['news']) == 1
        assert len(data['publications']) == 1
        assert len(data['projects']) == 1
        assert len(data['events']) == 1
        assert len(data['organisations']) == 0
        assert len(data['authors']) == 0
        assert len(data['magazines']) == 0

    def test_search_with_combined_filters(self, client, mock_db_session, mock_news, mock_publications):
        mock_scalars = MagicMock()
        mock_scalars.all.side_effect = [
            [mock_news],  # Новости
            [mock_publications],  # Публикации
            [],  # Проекты
            [],  # Организации
            [],  # Авторы
            [],  # Журналы
            []   # Что-то там еще
        ]
        mock_db_session.scalars.return_value = mock_scalars

        response = client.get('/api/search?q=Test&authors[]=1&magazines[]=1&date_from=2023-01-01&date_to=2023-12-31')
        assert response.status_code == 200
        data = response.get_json()

        assert len(data['news']) == 1
        assert len(data['publications']) == 1
        assert len(data['projects']) == 0
        assert len(data['events']) == 0
        assert len(data['organisations']) == 0
        assert len(data['authors']) == 0
        assert len(data['magazines']) == 0

    def test_search_with_no_results(self, client, mock_db_session):
        # Пустые результаты
        mock_scalars = MagicMock()
        mock_scalars.all.side_effect = [
            [],
            [],
            [],
            [],
            [],
            [],
            []
        ]
        mock_db_session.scalars.return_value = mock_scalars

        response = client.get('/api/search?q=Test&authors[]=999&magazines[]=999&date_from=2025-01-01&date_to=2025-12-31')
        assert response.status_code == 200
        data = response.get_json()

        assert len(data['news']) == 0
        assert len(data['publications']) == 0
        assert len(data['projects']) == 0
        assert len(data['events']) == 0
        assert len(data['organisations']) == 0
        assert len(data['authors']) == 0
        assert len(data['magazines']) == 0

class TestUploadsFile:
    def test_uploaded_wrong_file(self, client):
        response = client.get("/uploads/goal")
        assert response.status_code == 404
    def test_uploaded_correct_file(self, client, uploaded_organisation):
        response = client.get(f"/uploads/{uploaded_organisation.image}")
        assert response.status_code == 200
        