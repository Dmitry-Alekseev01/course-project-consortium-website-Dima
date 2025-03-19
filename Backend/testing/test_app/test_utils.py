from app.utils import get_current_language
from flask import session

def test_get_current_language_default(app_testing):
    with app_testing.test_request_context():
        assert get_current_language() == 'ru'