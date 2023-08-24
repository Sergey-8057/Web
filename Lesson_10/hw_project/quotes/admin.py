from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Author, Tag, Quote


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Quote)
