from django.contrib import admin
from .models import Post, Category, Author, User

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Author)

