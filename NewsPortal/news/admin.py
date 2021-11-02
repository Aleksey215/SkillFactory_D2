from django.contrib import admin
from .models import Post, Category, Author, PostCategory, User

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(PostCategory)
admin.site.register(Author)

