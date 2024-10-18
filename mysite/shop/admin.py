from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin


class CarPhotos(admin.TabularInline):
    model = CarPhotos
    extra = 1


@admin.register(Car)
class CarAdmin(TranslationAdmin):
    inlines = [CarPhotos]

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(Marka)
admin.site.register(Model)
admin.site.register(Rating)
admin.site.register(Favorite)

