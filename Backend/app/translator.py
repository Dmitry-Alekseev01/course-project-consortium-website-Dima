# from translate import Translator
# from .cache import get_cached_translation

# def translate_to_english(text, translator=None):
#     """
#     Переводит текст на английский язык с помощью библиотеки translate.
#     Использует кэширование для ускорения повторных запросов.
#     Возвращает None в случае ошибки.

#     :param text: Текст для перевода.
#     :param translator: Экземпляр Translator (опционально).
#     :return: Переведенный текст или None.
#     """
#     if translator is None:
#         translator = Translator(from_lang="ru", to_lang="en")

#     try:
#         return get_cached_translation(text, translator, dest_language='en')
#     except Exception as e:
#         print(f"Translation error: {e}")
#         return text #None





# from translate import Translator
# from .cache import get_cached_translation

# def translate_to_english(text, translator=None):
#     """Перевод с русского на английский с кэшированием"""
#     if not text or not isinstance(text, str):
#         return text
    
#     try:
#         if translator is None:
#             translator = Translator(from_lang="ru", to_lang="en")
            
#         return get_cached_translation(text, translator, 'en') or text
#     except Exception as e:
#         print(f"Translation error: {e}")
#         return text


from translate import Translator
# from .cache import get_cached_translation

def translate_to_english(text, translator=Translator(from_lang="ru", to_lang="en")):
    """Перевод с русского на английский с кэшированием"""
    if not text or not isinstance(text, str):
        return text

    try:
        # if translator is None:
        #     translator = Translator(from_lang="ru", to_lang="en")

        # Проверка кэша
        # cached = get_cached_translation(text, translator, 'en')
        # if cached is not None:
        #     return cached
        
        # Если кэша нет — переводим и кэшируем
        translated_text = translator.translate(text)
        return translated_text
    except Exception as e:
        print(f"Translation error: {e}")
        return text