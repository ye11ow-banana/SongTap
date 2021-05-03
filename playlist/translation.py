from modeltranslation.translator import register, TranslationOptions
from .models import Genre


@register(Genre)
class GenreTranslationOptions(TranslationOptions):
    fields = ('value',)
