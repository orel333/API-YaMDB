import re

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import (
    AdminPasswordChangeForm,
    UserChangeForm,
    UserCreationForm,
)

from api_yamdb.settings import EMPTY_VALUE
from api.methods import encode, give_jwt_for
from users.models import CustomUser, PreUser

from api.serializers import logger

class AdminAreaSite(admin.AdminSite):
    site_header = 'Admin Area'

my_admin_site = AdminAreaSite()
#my_admin_site.register(CustomUser, AdminPermissions)

class CustomUserCreationForm(UserCreationForm):
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user_role = user.role
        email = user.email
        username = user.username
        if user_role == 'admin':
            user.is_staff = True
        user.save()
        dict = {
            'email': email,
            'username': username
        }
        confirmation_code = encode(dict)
        if user.is_superuser == True:
            token = give_jwt_for(user, is_superuser=True)
            first_line = f'Создан суперпользователь {username}.\n'
        else:
            first_line = f'Создан пользователь {username}.\n'
            token = give_jwt_for(user)


        print(f'{first_line}Его роль: {user_role}.\n'
              f'Его токен: {token}\n'
              f'Его confirmation_code для обновления токена:\n'
              f'{confirmation_code}')
        logger.debug(f'user is active: {user.is_active}')
        logger.debug(f'user is staff: {user.is_staff}')
        return user

class AdminPermissions(admin.ModelAdmin):
    logger.debug('Admin permissions are exploited')
    
    def has_delete_permission(self, request, obj=None):
        logger.debug('Admin delete permissions are exploited')
        return request.user.is_staff
    def has_add_permission(self, request):
        logger.debug('Admin add permissions are exploited')
        return request.user.is_staff
    def has_change_permission(self, request, obj=None):
        logger.debug('Admin change permissions are exploited')
        return request.user.is_staff
    def has_view_permission(self, request, obj=None):
        logger.debug('Admin view permissions are exploited')
        return request.user.is_staff
            

@admin.register(CustomUser)
class UserAdminConfig(UserAdmin):
    #actions_selection_counter = False
    default_site = 'api_yamdb.users.admin.AdminAreaSite'
    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
        'bio',
        'role',
        #'is_superuser'
    )
    search_fields = ('username', 'email')
    list_filter = ('is_superuser', 'is_staff')
    fieldsets = (
        ('Key fields', {
            'fields': ('username', 'email', 'password', 'role')
        }),
        ('Personal info', {
            'fields': (
                'first_name', 'last_name', 'bio'
            ), 'classes': ('collapse',) 
        }),
        ('Permissions', {
            'fields': ('is_staff',),
        }),
    )
    # formfield_overrides = {
        # CustomUser.bio: {'widget': Textarea(attrs={'rows':10, 'cols':40})},
    # }
    add_fieldsets = (
        (None, {
            'classes': ('extrapretty',),
            'fields': ('username', 'email', 'password1', 'password2', 'role'),
        }),
    )
    add_form = CustomUserCreationForm

    def has_module_permission(self, request):
        return True

@admin.register(PreUser)
class PreUser(admin.ModelAdmin):
    list_display = (
        'username',
        'email'
    )


