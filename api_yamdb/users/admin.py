from django.contrib import admin

from api_yamdb.settings import EMPTY_VALUE
from users.models import CustomUser, PreUser


@admin.register(CustomUser)
class CustomUser(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
        'bio',
        'role',
    )
    empty_value_display = EMPTY_VALUE


@admin.register(PreUser)
class PreUser(admin.ModelAdmin):
    list_display = (
        'username',
        'email'
    )