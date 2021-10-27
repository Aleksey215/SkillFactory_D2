from django.db import models


class Author(models.Model):
    user = models.OneToOneField('User')
    rating = models.IntegerField(default=0)


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    article = 'AR'
    news = 'NE'

    kind = [
        (article, 'Статья'),
        (news, 'Новость')
    ]

    author = models.ForeignKey(Author)
    mode = models.CharField(max_length=2, choices=kind, default=article)
    time_of_creation = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    heading = models.CharField()
    text = models.TextField()
    rating = models.IntegerField(default=0)


class PostCategory(models.Model):
    post = models.ForeignKey(Post)
    category = models.ForeignKey(Category)


class Comment(models.Model):
    post = models.ForeignKey(Post)
    user = models.ForeignKey('User')
    text = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
