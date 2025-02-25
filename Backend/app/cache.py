# from flask_caching import Cache

# # Инициализация кэша
# cache = Cache()

# def get_cached_translation(text, translator, dest_language='en'):
#     """
#     Возвращает перевод текста из кэша, если он есть.
#     Если перевода нет в кэше, выполняет перевод и сохраняет его в кэш.
#     """
#     cache_key = f"translation_{text}_{dest_language}"
#     translated_text = cache.get(cache_key)

#     if translated_text is None:
#         translated_text = translator.translate(text)
#         cache.set(cache_key, translated_text)
#         print(f"Translation cached: {text} -> {translated_text}")
#     else:
#         print(f"Translation retrieved from cache: {text} -> {translated_text}")

#     return translated_text

# from flask_caching import Cache

# cache = Cache()

# def get_cached_translation(text, translator, dest_language='en'):
#     cache_key = f"translation_ru_en_{text}"
#     try:
#         translated_text = cache.get(cache_key)
#         if translated_text is None:
#             translated_text = translator.translate(text)
#             cache.set(cache_key, translated_text)
        
#         return translated_text or text  # Защита от None
#     except Exception as e:
#         print(f"Cache error: {e}")
#         return text

from flask_caching import Cache

cache = Cache()

def get_cached_translation(text, translator, dest_language='en'):
    cache_key = f"translation_{text}_{dest_language}"
    translated_text = cache.get(cache_key)

    if translated_text is None:
        translated_text = translator.translate(text)
        cache.set(cache_key, translated_text)
    
    return translated_text if translated_text else text