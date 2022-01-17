"""
В данном файле регистрируются модели, чтобы их можно было видеть в админке
"""
from django.contrib import admin
# Импортируем модели, которые нужны нам в админке
from .models import Post, Category, Author, Comment, CategorySubscribers

# регистрируем наши модели
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Comment)
admin.site.register(CategorySubscribers)

