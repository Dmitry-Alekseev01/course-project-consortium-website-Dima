# conftest.py
from pytest import fixture
from datetime import date, time
import sys
from pathlib import Path

root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

from app.models import Author, News, Event, Project, Publications, Organisation, Magazine



@fixture
def sample_author_with_middle_name():
    return Author(
        id=1,
        last_name="Иванов",
        first_name="Иван",
        middle_name="Иванович"
    )

@fixture
def sample_author_without_middle_name():
    return Author(
        id=2,
        last_name="Петров",
        first_name="Петр",
        middle_name=None
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
        materials="kitchen.jpg"
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
        description="Описание события 1"
    )

@fixture
def sample_project(sample_author_with_middle_name):
    project = Project(
        id=1,
        title="Проект 1",
        publication_date=date(2023, 9, 1),
        description="Описание проекта 1",
        content="Контент проекта 1",
        materials="loqiemean-как-у-людеи.mp3"
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
        link="https://t.me/vyshkochka"
    )