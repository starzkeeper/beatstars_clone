from .models import Songs, User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


# Register your models here.
@admin.register(Songs)
class SongsAdmin(admin.ModelAdmin):
    fields = ['name', 'author', ('file', 'cover'), 'text', ('temp', 'ton', 'hashtags'), 'slug', 'price']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(User, UserAdmin)
