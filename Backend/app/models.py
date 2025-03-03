# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime
# from .translator import translate_to_english

# db = SQLAlchemy()

# class TranslatableModel:
#     translatable_fields = []
    
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self._apply_translations()
        
#     def _apply_translations(self):
#         """Автоматический перевод для всех указанных полей"""
#         for field in self.translatable_fields:
#             original = getattr(self, field)
#             en_field = f"{field}_en"
            
#             if not getattr(self, en_field):
#                 try:
#                     translated = translate_to_english(original)
#                     setattr(self, en_field, translated)
#                 except Exception as e:
#                     print(f"Translation error for {self.__class__.__name__}.{field}: {e}")
#                     setattr(self, en_field, original)  # Fallback

# # Базовые модели без перевода
# class Magazine(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False, unique=True)
#     news = db.relationship('News', backref='magazine', cascade="all, delete")
#     publications = db.relationship('Publications', backref='magazine', cascade="all, delete")

# class Author(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     first_name = db.Column(db.String(50), nullable=False)
#     last_name = db.Column(db.String(50), nullable=False)
#     middle_name = db.Column(db.String(50), nullable=True)

# # Таблицы связи
# news_authors = db.Table('news_authors',
#     db.Column('news_id', db.Integer, db.ForeignKey('news.id', ondelete="CASCADE"), primary_key=True),
#     db.Column('author_id', db.Integer, db.ForeignKey('author.id', ondelete="CASCADE"), primary_key=True)
# )

# publication_authors = db.Table('publication_authors',
#     db.Column('publication_id', db.Integer, db.ForeignKey('publications.id', ondelete="CASCADE"), primary_key=True),
#     db.Column('author_id', db.Integer, db.ForeignKey('author.id', ondelete="CASCADE"), primary_key=True)
# )

# project_authors = db.Table('project_authors',
#     db.Column('project_id', db.Integer, db.ForeignKey('project.id', ondelete="CASCADE"), primary_key=True),
#     db.Column('author_id', db.Integer, db.ForeignKey('author.id', ondelete="CASCADE"), primary_key=True)
# )

# # Модели с переводом
# class News(db.Model, TranslatableModel):
#     translatable_fields = ['title', 'description']
    
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     title_en = db.Column(db.String(100), nullable=False)
#     publication_date = db.Column(db.DateTime, nullable=False)
#     description = db.Column(db.Text, nullable=False)
#     description_en = db.Column(db.Text, nullable=False)
#     magazine_id = db.Column(db.Integer, db.ForeignKey('magazine.id', ondelete="CASCADE"), nullable=True)
#     content = db.Column(db.Text, nullable=False)
#     materials = db.Column(db.String(300))
#     authors = db.relationship('Author', secondary=news_authors, lazy='subquery',
#                             backref=db.backref('news', lazy=True), cascade="all, delete")

# class Publications(db.Model, TranslatableModel):
#     translatable_fields = ['title', 'annotation']
    
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     title_en = db.Column(db.String(100), nullable=False)
#     publication_date = db.Column(db.DateTime, nullable=False)
#     magazine_id = db.Column(db.Integer, db.ForeignKey('magazine.id', ondelete="CASCADE"), nullable=True)
#     annotation = db.Column(db.Text, nullable=False)
#     annotation_en = db.Column(db.Text, nullable=False)
#     authors = db.relationship('Author', secondary=publication_authors, lazy='subquery',
#                             backref=db.backref('publications', lazy=True), cascade="all, delete")

# class Project(db.Model, TranslatableModel):
#     translatable_fields = ['title', 'description']
    
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     title_en = db.Column(db.String(100), nullable=False)
#     publication_date = db.Column(db.DateTime, nullable=False)
#     description = db.Column(db.Text, nullable=False)
#     description_en = db.Column(db.Text, nullable=False)
#     content = db.Column(db.Text, nullable=False)
#     materials = db.Column(db.String(300))
#     authors = db.relationship('Author', secondary=project_authors, lazy='subquery',
#                             backref=db.backref('projects', lazy=True), cascade="all, delete")

# class Event(db.Model, TranslatableModel):
#     translatable_fields = ['title', 'description']
    
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     title_en = db.Column(db.String(100), nullable=False)
#     publication_date = db.Column(db.DateTime, nullable=False)
#     location = db.Column(db.String(100), nullable=False)
#     description = db.Column(db.Text, nullable=False)
#     description_en = db.Column(db.Text, nullable=False)

# # Модели без перевода
# class Contact(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     email = db.Column(db.String(100), nullable=False)
#     phone = db.Column(db.String(20), nullable=False)
#     company = db.Column(db.String(100))
#     message = db.Column(db.Text, nullable=False)

# class Organisation(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     image = db.Column(db.String(200), nullable=False)
#     link = db.Column(db.String(200), nullable=False)

# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime
# from .translator import translate_to_english

# db = SQLAlchemy()

# class TranslatableModel:
#     """
#     Базовый класс для моделей с поддержкой перевода
#     """
#     # Переопределить в дочерних классах список полей для перевода
#     translatable_fields = []

#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.apply_translations()

#     def apply_translations(self):
#         """Автоматически переводит указанные поля при создании объекта"""
#         for field in self.translatable_fields:
#             original = getattr(self, field, None)
#             translated_field = f"{field}_en"
            
#             if original and not getattr(self, translated_field, None):
#                 try:
#                     translated = translate_to_english(original)
#                     setattr(self, translated_field, translated)
#                 except Exception as e:
#                     print(f"Error translating {field} for {self.__class__.__name__}: {e}")
#                     setattr(self, translated_field, original)  # Fallback

#     def get_translated(self, field: str, lang: str = 'ru') -> str:
#         """Универсальный метод для получения перевода"""
#         if lang == 'en':
#             translated = getattr(self, f"{field}_en", None)
#             return translated if translated else getattr(self, field, '')
#         return getattr(self, field, '')

# # Базовые модели
# class Magazine(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False, unique=True)
#     news = db.relationship('News', backref='magazine', cascade="all, delete")
#     publications = db.relationship('Publications', backref='magazine', cascade="all, delete")

# class Author(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     first_name = db.Column(db.String(50), nullable=False)
#     last_name = db.Column(db.String(50), nullable=False)
#     middle_name = db.Column(db.String(50), nullable=True)

# # Таблицы связи
# news_authors = db.Table('news_authors',
#     db.Column('news_id', db.Integer, db.ForeignKey('news.id', ondelete="CASCADE"), primary_key=True),
#     db.Column('author_id', db.Integer, db.ForeignKey('author.id', ondelete="CASCADE"), primary_key=True)
# )

# publication_authors = db.Table('publication_authors',
#     db.Column('publication_id', db.Integer, db.ForeignKey('publications.id', ondelete="CASCADE"), primary_key=True),
#     db.Column('author_id', db.Integer, db.ForeignKey('author.id', ondelete="CASCADE"), primary_key=True)
# )

# project_authors = db.Table('project_authors',
#     db.Column('project_id', db.Integer, db.ForeignKey('project.id', ondelete="CASCADE"), primary_key=True),
#     db.Column('author_id', db.Integer, db.ForeignKey('author.id', ondelete="CASCADE"), primary_key=True)
# )

# # Модели с переводом
# class News(db.Model, TranslatableModel):
#     translatable_fields = ['title', 'description']
    
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     title_en = db.Column(db.String(100), nullable=False)
#     publication_date = db.Column(db.DateTime, nullable=False)
#     description = db.Column(db.Text, nullable=False)
#     description_en = db.Column(db.Text, nullable=False)
#     magazine_id = db.Column(db.Integer, db.ForeignKey('magazine.id', ondelete="CASCADE"), nullable=True)
#     content = db.Column(db.Text, nullable=False)
#     materials = db.Column(db.String(300))
#     authors = db.relationship('Author', secondary=news_authors, lazy='subquery',
#                             backref=db.backref('news', lazy=True), cascade="all, delete")

# class Publications(db.Model, TranslatableModel):
#     translatable_fields = ['title', 'annotation']
    
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     title_en = db.Column(db.String(100), nullable=False)
#     publication_date = db.Column(db.DateTime, nullable=False)
#     magazine_id = db.Column(db.Integer, db.ForeignKey('magazine.id', ondelete="CASCADE"), nullable=True)
#     annotation = db.Column(db.Text, nullable=False)
#     annotation_en = db.Column(db.Text, nullable=False)
#     authors = db.relationship('Author', secondary=publication_authors, lazy='subquery',
#                             backref=db.backref('publications', lazy=True), cascade="all, delete")

# class Project(db.Model, TranslatableModel):
#     translatable_fields = ['title', 'description']
    
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     title_en = db.Column(db.String(100), nullable=False)
#     publication_date = db.Column(db.DateTime, nullable=False)
#     description = db.Column(db.Text, nullable=False)
#     description_en = db.Column(db.Text, nullable=False)
#     content = db.Column(db.Text, nullable=False)
#     materials = db.Column(db.String(300))
#     authors = db.relationship('Author', secondary=project_authors, lazy='subquery',
#                             backref=db.backref('projects', lazy=True), cascade="all, delete")

# class Event(db.Model, TranslatableModel):
#     translatable_fields = ['title', 'description']
    
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     title_en = db.Column(db.String(100), nullable=False)  # <- Здесь
#     description_en = db.Column(db.Text(), nullable=False) # <- И здесь
#     location = db.Column(db.String(100), nullable=False)
#     description = db.Column(db.Text, nullable=False)
#     description_en = db.Column(db.Text, nullable=False)

# class Contact(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     email = db.Column(db.String(100), nullable=False)
#     phone = db.Column(db.String(20), nullable=False)
#     company = db.Column(db.String(100))
#     message = db.Column(db.Text, nullable=False)

# class Organisation(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     image = db.Column(db.String(200), nullable=False)
#     link = db.Column(db.String(200), nullable=False)



from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, time, date
from .translator import translate_to_english

db = SQLAlchemy()
class TranslateMixin:
    # translations = (
    #     ('title', 'title_en'),
    #     ('description', 'description_en')
    # )
    translations = ()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        for translation_from, translation_to in self.translations:
            attribute_from = getattr(self, translation_from)
            attribute_to = getattr(self, translation_to)
            if attribute_from and not attribute_to:
                translated_value = translate_to_english(attribute_from) or attribute_from
                setattr(self, translation_to, translated_value)
        
        


# Таблица для журналов
class Magazine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)  # Уникальное название журнала
    news = db.relationship('News', backref='magazine', cascade="all, delete")
    publications = db.relationship('Publications', backref='magazine', cascade="all, delete")

# Таблица для авторов
class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)  # Имя
    last_name = db.Column(db.String(50), nullable=False)   # Фамилия
    middle_name = db.Column(db.String(50), nullable=True)  # Отчество (может быть NULL)

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
    title_en = db.Column(db.String(100), nullable=False)
    # date = db.Column(db.String(50), nullable=False)
    # time = db.Column(db.DateTime, nullable=False)
    publication_date = db.Column(db.DateTime, nullable=False)
    #date = db.Column(db.Date, nullable=False)
    #time = db.Column(db.Time, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    description_en = db.Column(db.Text, nullable=False)
    translations = (
        ('title', 'title_en'),
        ('description', 'description_en')
    )


# Модель для новостей
class News(TranslateMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    title_en = db.Column(db.String(100), nullable=False)
    #publication_date = db.Column(db.String(50), nullable=False)
    publication_date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=False)
    description_en = db.Column(db.Text, nullable=False)
    magazine_id = db.Column(db.Integer, db.ForeignKey('magazine.id', ondelete="CASCADE"), nullable=True)
    content = db.Column(db.Text, nullable=False)
    materials = db.Column(db.String(300))  # Путь к файлу
    authors = db.relationship('Author', secondary=news_authors, lazy='subquery',
                              backref=db.backref('news', lazy=True), cascade="all, delete")
    translations = (
        ('title', 'title_en'),
        ('description', 'description_en')
    )
    

    
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
    title_en = db.Column(db.String(100), nullable=False)
    publication_date = db.Column(db.DateTime, nullable=False)
    magazine_id = db.Column(db.Integer, db.ForeignKey('magazine.id', ondelete="CASCADE"), nullable=True)
    annotation = db.Column(db.Text, nullable=False)
    annotation_en = db.Column(db.Text, nullable=False)
    authors = db.relationship('Author', secondary=publication_authors, lazy='subquery',
                              backref=db.backref('publications', lazy=True), cascade="all, delete")
    translations = (
        ('title', 'title_en'),
        ('annotation', 'annotation_en')
    )

    
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
    title_en = db.Column(db.String(100), nullable=False)
    #publication_date = db.Column(db.String(50), nullable=False)
    publication_date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=False)
    description_en = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    materials = db.Column(db.String(300))  # Путь к файлу
    authors = db.relationship('Author', secondary=project_authors, lazy='subquery',
                              backref=db.backref('projects', lazy=True), cascade="all, delete")
    translations = (
        ('title', 'title_en'),
        ('description', 'description_en')
    )
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

