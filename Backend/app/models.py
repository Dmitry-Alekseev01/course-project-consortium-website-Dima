from . import utils
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, time, date
from .translator import translate_to_english

db = SQLAlchemy()
# class TranslateMixin:
    
#     translations = ()
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
        
#         for translation_from, translation_to in self.translations:
#             attribute_from = getattr(self, translation_from)
#             attribute_to = getattr(self, translation_to)
#             if attribute_from and not attribute_to:
#                 translated_value = translate_to_english(attribute_from) or attribute_from
#                 setattr(self, translation_to, translated_value)


class TranslateMixin:
    translations = ()
    
    @classmethod
    def __declare_last__(cls):
        """Регистрация обработчиков событий после объявления модели"""
        from sqlalchemy import event

        def translate_fields(mapper, connection, target):
            for from_field, to_field in target.translations:
                source_value = getattr(target, from_field)
                target_value = getattr(target, to_field)
                
                if source_value and not target_value:
                    translated = translate_to_english(source_value)
                    #print(translated)
                    setattr(target, to_field, translated or source_value)

        # Обработчики для вставки и обновления
        event.listen(cls, 'before_insert', translate_fields)
        event.listen(cls, 'before_update', translate_fields)
        
        


# Таблица для журналов
class Magazine(TranslateMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)  # Уникальное название журнала
    name_en = db.Column(db.String(100), nullable=True, unique=True)
    news = db.relationship('News', backref='magazine', cascade="all, delete")
    publications = db.relationship('Publications', backref='magazine', cascade="all, delete")
    translations = (
        ('name', 'name_en'),
    )

# Таблица для авторов
class Author(TranslateMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)  # Имя
    first_name_en = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=False)   # Фамилия
    last_name_en = db.Column(db.String(50), nullable=True)
    middle_name = db.Column(db.String(50), nullable=True)  # Отчество (может быть NULL)
    middle_name_en = db.Column(db.String(50), nullable=True)
    translations = (
        ('first_name', 'first_name_en'),
        ('last_name', 'last_name_en'),
        ('middle_name', 'middle_name_en')
    )

# Таблица связи для новостей и авторов
news_authors = db.Table('news_authors',
    db.Column('news_id', db.Integer, db.ForeignKey('news.id', ondelete="CASCADE"), primary_key=True),
    db.Column('author_id', db.Integer, db.ForeignKey('author.id', ondelete="CASCADE"), primary_key=True)
)

# Таблица связи для публикаций и авторов
publication_authors = db.Table('publication_authors',
    db.Column('publication_id', db.Integer, db.ForeignKey('publications.id', ondelete="CASCADE"), primary_key=True),
    db.Column('author_id', db.Integer, db.ForeignKey('author.id', ondelete="CASCADE"), primary_key=True)
)

# Промежуточная таблица для проектов и авторов
project_authors = db.Table('project_authors',
    db.Column('project_id', db.Integer, db.ForeignKey('project.id', ondelete="CASCADE"), primary_key=True),
    db.Column('author_id', db.Integer, db.ForeignKey('author.id', ondelete="CASCADE"), primary_key=True)
)

# Модель для контактов
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    company = db.Column(db.String(100))
    message = db.Column(db.Text, nullable=False)

# Модель для событий
class Event(TranslateMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    title_en = db.Column(db.String(100), nullable=True)
    # date = db.Column(db.String(50), nullable=False)
    # time = db.Column(db.DateTime, nullable=False)
    publication_date = db.Column(db.DateTime, nullable=False)
    #date = db.Column(db.Date, nullable=False)
    #time = db.Column(db.Time, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    description_en = db.Column(db.Text, nullable=True)
    translations = (
        ('title', 'title_en'),
        ('description', 'description_en')
    )

    # @property
    # def title_display(self):
    #     language = utils.get_current_language()
    #     return self.title_en if language == 'en' else self.title

    # @property
    # def description_display(self):
    #     language = utils.get_current_language()
    #     return self.description_en if language == 'en' else self.description

# Модель для новостей
class News(TranslateMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    title_en = db.Column(db.String(100), nullable=True)
    #publication_date = db.Column(db.String(50), nullable=False)
    publication_date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=False)
    description_en = db.Column(db.Text, nullable=True)
    magazine_id = db.Column(db.Integer, db.ForeignKey('magazine.id', ondelete="CASCADE"), nullable=True)
    content = db.Column(db.Text, nullable=False)
    content_en = db.Column(db.Text, nullable=True)
    materials = db.Column(db.String(300))  # Путь к файлу
    authors = db.relationship('Author', secondary=news_authors, lazy='subquery',
                              backref=db.backref('news', lazy=True), cascade="all, delete")
    translations = (
        ('title', 'title_en'),
        ('description', 'description_en'),
        ('content', 'content_en')
    )
    
    # @property
    # def title_display(self):
    #     language = utils.get_current_language()
    #     return self.title_en if language == 'en' else self.title

    # @property
    # def description_display(self):
    #     language = utils.get_current_language()
    #     return self.description_en if language == 'en' else self.description
    
    # def __init__(self, **kwargs):
    #     super(News, self).__init__(**kwargs)
        
    #     if self.title and not self.title_en:
    #         self.title_en = translate_to_english(self.title) or self.title
        
    #     if self.description and not self.description_en:
    #         self.description_en = translate_to_english(self.description) or self.description
    
    
    # def __init__(self, **kwargs):
    #     super(News, self).__init__(**kwargs)
    #     if self.title and not self.title_en:
    #         try:
    #             self.title_en = translate_to_english(self.title)
    #             if self.title_en is None:
    #                 raise ValueError("Translation failed for title")
    #         except Exception as e:
    #             print(f"Error translating title: {e}")
    #             self.title_en = self.title  # Fallback

    #     if self.description and not self.description_en:
    #         try:
    #             self.description_en = translate_to_english(self.description)
    #             if self.description_en is None:
    #                 raise ValueError("Translation failed for description")
    #         except Exception as e:
    #             print(f"Error translating description: {e}")
    #             self.description_en = self.description  # Fallback

    # def get_translated_field(self, field: str, language: str = 'ru') -> str:
    #     """
    #     Возвращает значение поля на указанном языке.
    #     Если перевод отсутствует, возвращает значение на русском.

    #     :param field: Название поля (например, 'title' или 'description').
    #     :param language: Язык ('ru' или 'en').
    #     :return: Значение поля на нужном языке.
    #     """
    #     if language == 'en':
    #         translated_field = getattr(self, f"{field}_en")
    #         return translated_field if translated_field else getattr(self, field)
    #     return getattr(self, field)

# Модель для публикаций
class Publications(TranslateMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    title_en = db.Column(db.String(100), nullable=True)
    publication_date = db.Column(db.DateTime, nullable=False)
    magazine_id = db.Column(db.Integer, db.ForeignKey('magazine.id', ondelete="CASCADE"), nullable=True)
    annotation = db.Column(db.Text, nullable=False)
    annotation_en = db.Column(db.Text, nullable=True)
    authors = db.relationship('Author', secondary=publication_authors, lazy='subquery',
                              backref=db.backref('publications', lazy=True), cascade="all, delete")
    translations = (
        ('title', 'title_en'),
        ('annotation', 'annotation_en')
    )

    # @property
    # def title_display(self):
    #     language = utils.get_current_language()
    #     return self.title_en if language == 'en' else self.title

    # @property
    # def annotation_display(self):
    #     language = utils.get_current_language()
    #     return self.annotation_en if language == 'en' else self.annotation   
     
    # def __init__(self, **kwargs):
    #     super(Publications, self).__init__(**kwargs)
        
    #     if self.title and not self.title_en:
    #         self.title_en = translate_to_english(self.title) or self.title
        
    #     if self.annotation and not self.annotation_en:
    #         self.annotation_en = translate_to_english(self.annotation) or self.annotation

# Модель для проектов
class Project(TranslateMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    title_en = db.Column(db.String(100), nullable=True)
    #publication_date = db.Column(db.String(50), nullable=False)
    publication_date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=False)
    description_en = db.Column(db.Text, nullable=True)
    content = db.Column(db.Text, nullable=False)
    content_en = db.Column(db.Text, nullable=True)
    materials = db.Column(db.String(300))  # Путь к файлу
    authors = db.relationship('Author', secondary=project_authors, lazy='subquery',
                              backref=db.backref('projects', lazy=True), cascade="all, delete")
    translations = (
        ('title', 'title_en'),
        ('description', 'description_en'),
        ('content', 'content_en')
    )

    # @property
    # def title_display(self):
    #     language = utils.get_current_language()
    #     return self.title_en if language == 'en' else self.title

    # @property
    # def description_display(self):
    #     language = utils.get_current_language()
    #     return self.description_en if language == 'en' else self.description
    
    # def __init__(self, **kwargs):
    #     super(Project, self).__init__(**kwargs)
        
    #     if self.title and not self.title_en:
    #         self.title_en = translate_to_english(self.title) or self.title
        
    #     if self.description and not self.description_en:
    #         self.description_en = translate_to_english(self.description) or self.description

# Модель для организаций
class Organisation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(200), nullable=False)
    link = db.Column(db.String(200), nullable=False)

