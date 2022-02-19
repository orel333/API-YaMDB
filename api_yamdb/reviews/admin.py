from django.contrib import admin

from users.models import CustomUser
from .models import Comment, Review, Category, Genre, Title

admin.site.register(CustomUser)
admin.site.register(Comment)
admin.site.register(Review)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Title)

