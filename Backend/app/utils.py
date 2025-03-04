from flask import session

def get_current_language():
    return session.get('language', 'ru')
