from flask_mail import Mail
from flask_migrate import Migrate
from flask_cors import CORS
import logging
from .models import db
#from .admin_views import register_admin_views 
from flask_basicauth import BasicAuth
from flask import Response, redirect, Flask
from flask_admin import AdminIndexView, Admin
from flask_admin.contrib.sqla import ModelView
from werkzeug.exceptions import HTTPException

# Инициализация расширений
mail = Mail()
migrate = Migrate()
#admin = Admin(name='Admin Panel', template_mode='bootstrap3')
#basic_auth = BasicAuth()



# class AuthException(HTTPException):
#     def init(self, message):
#         super().init(message, Response(
#             "You could not be authenticated. Please refresh the page.", 401,
#             {'WWW-Authenticate': 'Basic realm="Login Required"'} ))


# class MyModelView(ModelView):
#     def is_accessible(self):
#         print("is_accesible_model")
#         if not basic_auth.authenticate():
#             print("before_exception_model")
#             return redirect(basic_auth.challenge())
#             #raise AuthException('Not authenticated.')
#         else:
#             return True
#     def inaccessible_callback(self, name, **kwargs):
#         print("inaccesible_callback_model")
#         return redirect(basic_auth.challenge())
    
# class MyAdminIndexView(AdminIndexView):
#     def is_accessible(self):
#         print("is_accesible")
#         if not basic_auth.authenticate():
#             print("before exception")
#             return False #redirect(basic_auth.challenge())
#             #raise AuthException('Not authenticated.')
#         else:
#             return True
#     def inaccessible_callback(self, name, **kwargs):
#         print("inaccessible_callback")
#         return redirect(basic_auth.challenge())
    

# В цикл запихнуть
def register_admin_views(admin: Admin, db):
    admin.add_view(ModelView(models.Magazine, db.session, name='Журналы', category='Модели', endpoint='unique_magazine_admin'))
    admin.add_view(ModelView(models.Author, db.session, name='Авторы', category='Модели', endpoint='unique_author_admin'))
    admin.add_view(ModelView(models.Contact, db.session, name='Контакты', category='Модели', endpoint='unique_contact_admin'))
    admin.add_view(ModelView(models.Event, db.session, name='События', category='Модели', endpoint='unique_event_admin'))
    admin.add_view(ModelView(models.News, db.session, name='Новости', category='Модели', endpoint='unique_news_admin'))
    admin.add_view(ModelView(models.Publications, db.session, name='Публикации', category='Модели', endpoint='unique_publications_admin'))
    admin.add_view(ModelView(models.Project, db.session, name='Проекты', category='Модели', endpoint='unique_project_admin'))
    admin.add_view(ModelView(models.Organisation, db.session, name='Организации', category='Модели', endpoint='unique_organisation_admin'))

    

def create_app(config_path = 'app.config.Config', mail = mail):
    app = Flask(__name__)
    app.config.from_object(config_path)
    app.config['DEBUG'] = True


    #basic_auth.init_app(app)

    # Инициализация расширений
    db.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    #admin = Admin(name='Admin Panel', template_mode='bootstrap3', index_view = MyAdminIndexView())
    admin = Admin(name='Admin Panel', template_mode='bootstrap3')
    admin.init_app(app)

    # Регистрация представлений Flask-Admin
    register_admin_views(admin, db)  # Вызов функции

    # Регистрация Blueprint
    from .routes import main
    app.register_blueprint(main)

    CORS(app, origins=["http://localhost:3000", "http://127.0.0.1:3000"])

    with app.app_context():
        db.create_all()

    return app