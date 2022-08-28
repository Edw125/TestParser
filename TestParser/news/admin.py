from django.contrib import admin

from TestParser.settings import VALUE_DISPLAY
from news.models import Tag, News


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_filter = ('name',)
    search_fields = ('name',)
    empty_value_display = VALUE_DISPLAY


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'resource', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('created_at',)
    empty_value_display = VALUE_DISPLAY
