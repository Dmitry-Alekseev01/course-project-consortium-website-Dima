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
    


# class TestMyModelView:
#     def test_on_model_change_translation(self, news_view, sample_news):

#         news_view.on_model_change(None, sample_news, is_created=True)

#         assert sample_news.title_en == "Новость 1_en"
#         assert sample_news.description_en == "Описание новости 1_en"

#     def test_on_model_change_event(self, event_view, sample_event):

#         event_view.on_model_change(None, sample_event, is_created=True)

#         assert sample_event.title_en == "Событие 1_en"
#         assert sample_event.description_en == "Описание события 1_en"