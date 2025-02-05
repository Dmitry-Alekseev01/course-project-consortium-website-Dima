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
    def test_serialize_news_with_magazine(self, sample_news):
        result = serialize_news(sample_news)
        
        assert result["authors"] == ["Иванов И.И.", "Петров П."]
        assert result["materials"] == "/uploads/kitchen.jpg"

    def test_serialize_news_without_magazine(self, sample_news):
        sample_news.magazine = None
        result = serialize_news(sample_news)
        assert result["magazine"] is None

class TestEventSerializer:
    def test_serialize_event_time_format(self, sample_event):
        result = serialize_events(sample_event)
        assert result["time"] == "14:00"

class TestProjectSerializer:
    def test_serialize_project_materials(self, sample_project):
        result = serialize_projects(sample_project)
        assert result["materials"] == "/uploads/loqiemean-как-у-людеи.mp3"

class TestPublicationSerializer:
    def test_serialize_publication_authors(self, sample_publication):
        result = serialize_publications(sample_publication)
        assert set(result["authors"]) == {"Иванов И.И.", "Петров П."}
class TestOrganisationSerializer:
    def test_serialize_organisation(self, sample_organisation):
        result = serialize_organisations(sample_organisation)
        
        assert result["id"] == 1
        assert result["image"] == "kitchen.jpg"
        assert result["link"] == "https://t.me/vyshkochka"