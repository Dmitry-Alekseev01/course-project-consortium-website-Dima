from datetime import datetime, date, time
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