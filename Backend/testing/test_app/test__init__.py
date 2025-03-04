import pytest
import base64
from flask import url_for
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

class TestMyAdminIndexView:
    
    @pytest.fixture(autouse=True)
    def setup(self, client):
        self.client = client
        self.admin_url = '/admin/'
        self.valid_headers = self._auth_headers('admin', 'password')
        self.invalid_headers = self._auth_headers('wrong', 'wrong')

    def _auth_headers(self, username, password):
        credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
        return {'Authorization': f'Basic {credentials}'}

    def test_admin_access_without_auth(self):
        response = self.client.get(self.admin_url)
        assert response.status_code == 401
        assert 'WWW-Authenticate' in response.headers

    def test_admin_access_with_valid_auth(self):
        response = self.client.get(self.admin_url, headers=self.valid_headers)
        assert response.status_code == 200
        assert 'Admin Panel' in response.get_data(as_text=True)

    def test_admin_access_with_invalid_auth(self):
        response = self.client.get(self.admin_url, headers=self.invalid_headers)
        assert response.status_code == 401


class TestMyModelView:
    
    @pytest.fixture(autouse=True)
    def setup(self, client):
        self.client = client
        self.valid_headers = self._auth_headers('admin', 'password')
        self.invalid_headers = self._auth_headers('wrong', 'wrong')
        self.endpoints = [
            '/admin/unique_magazine_admin/',
            '/admin/unique_author_admin/',
            '/admin/unique_contact_admin/',
            '/admin/unique_event_admin/',
            '/admin/unique_news_admin/',
            '/admin/unique_publications_admin/',
            '/admin/unique_project_admin/',
            '/admin/unique_organisation_admin/'
        ]

    def _auth_headers(self, username, password):
        credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
        return {'Authorization': f'Basic {credentials}'}

    @pytest.mark.parametrize("endpoint", [
        '/admin/unique_magazine_admin/',
        '/admin/unique_author_admin/',
        '/admin/unique_contact_admin/',
        '/admin/unique_event_admin/',
        '/admin/unique_news_admin/',
        '/admin/unique_publications_admin/',
        '/admin/unique_project_admin/',
        '/admin/unique_organisation_admin/'
    ])
    def test_model_view_access(self, endpoint):

        response = self.client.get(endpoint)
        assert response.status_code == 401

        response = self.client.get(endpoint, headers=self.valid_headers)
        assert response.status_code == 200


        response = self.client.get(endpoint, headers=self.invalid_headers)
        assert response.status_code == 401

    def test_all_model_views_in_sequence(self):
        for endpoint in self.endpoints:
            response = self.client.get(endpoint)
            assert response.status_code == 401
            
            response = self.client.get(endpoint, headers=self.valid_headers)
            assert response.status_code == 200
            
            response = self.client.get(endpoint, headers=self.invalid_headers)
            assert response.status_code == 401
    
    # def test_admin_create_event(admin_client):
    #     """Тест создания события через админку"""
    #     data = {
    #         'title': 'Новое событие',
    #         'description': 'Описание события',
    #         'publication_date': '2023-01-01',
    #         'location': 'Москва'
    #     }
    
    #     response = admin_client.post(
    #         '/admin/unique_event_admin/new/',
    #         data=data,
    #         follow_redirects=True
    #     )
    
    #     assert response.status_code == 200
    #     event = Event.query.first()
    #     assert event.title_en == "Новое событие_en"
    #     assert event.description_en == "Описание события_en"

    # def test_admin_update_news(admin_client, route_news):
    #     """Тест обновления новости через админку"""
    #     updated_data = {
    #         'title': 'Обновлённый заголовок',
    #         'description': 'Новое описание',
    #         'publication_date': '2023-01-01',
    #         'content': 'Новый контент'
    #     }
        
    #     response = admin_client.post(
    #         f'/admin/unique_news_admin/edit/?id={route_news.id}',
    #         data=updated_data,
    #         follow_redirects=True
    #     )
        
    #     updated_news = News.query.get(route_news.id)
    #     assert updated_news.title_en == "Обновлённый заголовок_en"
    #     assert updated_news.description_en == "Новое описание_en"
