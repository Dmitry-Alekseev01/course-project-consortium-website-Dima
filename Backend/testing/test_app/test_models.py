def test_magazine_str(sample_magazine):
    assert str(sample_magazine) == "Журнал 1"


def test_contact_str(sample_contact):
    assert str(sample_contact) == "1 Leo Livshitz"

def test_event_str(sample_event):
    assert str(sample_event) == "1 Событие 1"

def test_news_str(sample_news):
    assert str(sample_news) == "1 Новость 1"

def test_project_str(sample_project):
    assert str(sample_project) == "1 Проект 1"

def test_publication_str(sample_publication):
    assert str(sample_publication) == "1 Публикация 1"
