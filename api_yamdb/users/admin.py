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


# class CustomUserCreationForm(UserCreationForm):
    # def save(self, commit=True):
        # user = super().save(commit=False)
        # user.set_password(self.cleaned_data["password1"])
        # user_role = user.role
        # email = user.email
        # username = user.username
        # if user_role == 'admin':
            # user.is_staff = True
        # user.save()
        # dict = {
            # 'email': email,
            # 'username': username
        # }
        # confirmation_code = encode(dict)
        # if user.is_superuser == True:
            # token = give_jwt_for(user, is_superuser=True)
            # first_line = f'Создан суперпользователь {username}.\n'
        # else:
            # first_line = f'Создан пользователь {username}.\n'
            # token = give_jwt_for(user)
# 
# 
        # print(f'{first_line}Его роль: {user_role}.\n'
              # f'Его токен: {token}\n'
              # f'Его confirmation_code для обновления токена:\n'
              # f'{confirmation_code}')
        # logger.debug(f'user is active: {user.is_active}')
        # logger.debug(f'user is staff: {user.is_staff}')
        # return user

class AdminPermissions(admin.ModelAdmin):
    logger.debug('Admin permissions are exploited')
            

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
   # add_form = CustomUserCreationForm

    def has_module_permission(self, request):
        return True

    def has_delete_permission(self, request, obj=None):
        if obj != None:
            return request.user.is_staff and not obj.is_staff
        return request.user.is_staff
    def has_add_permission(self, request):
        return request.user.is_staff
    def has_change_permission(self, request, obj=None):
        logger.debug(obj)
        if obj != None:
            return request.user.is_staff and not obj.is_staff
        return request.user.is_staff
    def has_view_permission(self, request, obj=None):
        return request.user.is_staff

    def save_model(self, request, obj, form, change):
        logger.debug(change)
        #logger.debug(f'role: {obj.role}')
        #logger.debug(f'form: {form}')
        #logger.debug(f'obj: {obj}')
        #logger.debug(f'rd: {request.data}')
        #logger.debug(request.method)
        if isinstance(obj, CustomUser):
            logger.debug('The object was recognized as CustomUser instance')
            super().save_model(request, obj, form, change)
            user_role = obj.role
            email = obj.email
            username = obj.username
            if user_role == 'admin':
                obj.is_staff = True
            # на случай изменения объекта
            else:
                obj.is_staff = False
            obj.save()
            dict = {
                'email': email,
                'username': username
            }
            confirmation_code = encode(dict)
            if change:
                if obj.is_superuser == True:
                    token = give_jwt_for(obj, is_superuser=True)
                    pre_first_line = (f'\tВНИМАНИЕ! Объект был изменен на '
                                      f'"суперпользователь {username}".')
                else:
                    pre_first_line = (f'\tВНИМАНИЕ! Объект был изменен на '
                                      f'"пользователь {username}".')
                    token = give_jwt_for(obj)
                first_line = (f'{pre_first_line}\n\tДля него были '
                              'созданы новые коды доступа.')
            else:
                if obj.is_superuser == True:
                    token = give_jwt_for(obj, is_superuser=True)
                    first_line = f'Создан суперпользователь {username}.'
                else:
                    first_line = f'Создан пользователь {username}.'
                    token = give_jwt_for(obj)


            print(f'{first_line}\nЕго роль: {user_role}.\n'
                f'Его токен: {token}\n'
                f'Его confirmation_code для обновления токена:\n'
                f'{confirmation_code}')
            logger.debug(f'user is active: {obj.is_active}')
            logger.debug(f'user is staff: {obj.is_staff}')
        else:
            super().save_model(request, obj, form, change)

@admin.register(PreUser)
class PreUser(admin.ModelAdmin):
    list_display = (
        'username',
        'email'
    )
