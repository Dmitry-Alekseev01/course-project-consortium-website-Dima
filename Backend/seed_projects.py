# import os
# from datetime import datetime
# from app.models import db, Project, Author, project_authors

# def seed_projects(app):
#     with app.app_context():
#         # Очистка таблиц Project и project_authors
#         db.session.query(project_authors).delete()  # Очищаем промежуточную таблицу
#         db.session.query(Project).delete()  # Очищаем таблицу Project
#         db.session.commit()

#         author1 = Author.query.filter_by(first_name="Иван", last_name="Иванов").first()
#         author2 = Author.query.filter_by(first_name="Петр", last_name="Петров").first()
#         author3 = Author.query.filter_by(first_name="Сергей", last_name="Сидоров").first()

#         if not author1 or not author2 or not author3:
#             print("Ошибка: Авторы не найдены. Запустите скрипт seed_authors.py.")
#             return

#         # Путь к папке uploads
#         UPLOADS_DIR = os.path.join(os.path.dirname(__file__), 'uploads')
#         os.makedirs(UPLOADS_DIR, exist_ok=True)

#         test_files = {
#             "kitchen.jpg": "kitchen.jpg",
#             "loqiemean-как-у-людеи.mp3": "loqiemean-как-у-людеи.mp3",
#             "loqiemean-потом.mp3": "loqiemean-потом.mp3",
#         }

#         for filename in test_files.values():
#             file_path = os.path.join(UPLOADS_DIR, filename)
#             if not os.path.exists(file_path):
#                 print(f"Файл {filename} не найден в папке uploads. Пропускаем.")
#             else:
#                 print(f"Файл {filename} найден в папке uploads.")

#         project1 = Project(
#             title="Проект с изображением",
#             publication_date=datetime.strptime("21/11/06 16:30", "%d/%m/%y %H:%M"),
#             description="Описание проекта с изображением",
#             content="Основной текст проекта с изображением",
#             materials="kitchen.jpg"  # Имя файла
#         )
#         project1.authors.append(author1)
#         project1.authors.append(author2)

#         project2 = Project(
#             title="Проект с аудио 1",
#             publication_date=datetime.strptime("21/11/06 16:30", "%d/%m/%y %H:%M"),
#             description="Описание проекта с аудио 1",
#             content="Основной текст проекта с аудио 1",
#             materials="loqiemean-как-у-людеи.mp3"  # Имя файла
#         )
#         project2.authors.append(author3)

#         project3 = Project(
#             title="Проект с аудио 2",
#             publication_date=datetime.strptime("21/11/06 16:30", "%d/%m/%y %H:%M"),
#             description="Описание проекта с аудио 2",
#             content="Основной текст проекта с аудио 2",
#             materials="loqiemean-потом.mp3"  # Имя файла
#         )
#         project3.authors.append(author1)

#         db.session.add(project1)
#         db.session.add(project2)
#         db.session.add(project3)
#         db.session.commit()
#         print("Тестовые проекты успешно добавлены в базу данных!")

# # if __name__ == "__main__":
# #     seed_projects()