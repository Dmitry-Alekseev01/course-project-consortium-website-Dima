import datetime
from unittest.mock import patch
# Backend/testing/test_app/test_serializers.py
from app.serializers import (
    serialize_author,
    serialize_news,
    serialize_events,
    serialize_projects,
    serialize_publications,
    serialize_organisations
)

class TestAuthorSerializer:
    def test_serialize_author_with_middle_name(self, sample_author_with_middle_name):
        result = serialize_author(sample_author_with_middle_name)
        assert result == "Иванов И.И."
        
    def test_serialize_author_without_middle_name(self, sample_author_without_middle_name):
        result = serialize_author(sample_author_without_middle_name)
        assert result == "Петров П." 


class TestNewsSerializer:
    @patch("app.utils.get_current_language", return_value="ru")
    def test_serialize_news_with_magazine(self, mock_get_current_language, sample_news):
        result = serialize_news(sample_news)
        
        assert result["authors"] == ["Иванов И.И.", "Петров П."]
        assert result["materials"] == "/uploads/kitchen.jpg"
        
    @patch("app.utils.get_current_language", return_value="ru")
    def test_serialize_news_without_magazine(self, mock_get_current_language, sample_news):
        sample_news.magazine = None
        result = serialize_news(sample_news)
        assert result["magazine"] is None


class TestEventSerializer:
    @patch("app.utils.get_current_language", return_value="ru")
    def test_serialize_event_time_format(self, mock_get_current_language, sample_event):
        result = serialize_events(sample_event)
        assert result["publication_date"] == datetime.date(2023, 10, 1)


class TestProjectSerializer:
    @patch("app.utils.get_current_language", return_value="ru")
    def test_serialize_project_materials(self, mock_get_current_language, sample_project):
        result = serialize_projects(sample_project)
        assert result["materials"] == "/uploads/loqiemean-как-у-людеи.mp3"

class TestPublicationSerializer:
    @patch("app.utils.get_current_language", return_value="ru")
    def test_serialize_publication_authors(self, mock_get_current_language, sample_publication):
        result = serialize_publications(sample_publication)
        assert set(result["authors"]) == {"Иванов И.И.", "Петров П."}

class TestOrganisationSerializer:
    def test_serialize_organisation(self, sample_organisation):
        result = serialize_organisations(sample_organisation)
        
        assert result["id"] == 1
        assert result["image"] == "kitchen.jpg"
        assert result["link"] == "https://t.me/vyshkochka1"

