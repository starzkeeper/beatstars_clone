from django.contrib import admin
from .models import Songs, Author


# Register your models here.
@admin.register(Songs)
class SongsAdmin(admin.ModelAdmin):
    fields = ['name', 'author', ('file', 'cover'), 'text', ('temp', 'ton', 'hashtags'), 'slug', 'price']
    prepopulated_fields = {'slug': ('name', )}


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    fields = ['name']
