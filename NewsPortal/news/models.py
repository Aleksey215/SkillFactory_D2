from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db import models


class Author(models.Model):
    author_user = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rating = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    def update_rating(self):
        author_post_rating = self.post_set.aggregate(postRating=Sum('post_rating'))
        p_rat = 0
        p_rat += author_post_rating.get('postRating')

        author_comment_rating = self.author_user.comment_set.aggregate(commentRating=Sum('comment_rating'))
        c_rat = 0
        c_rat += author_comment_rating.get('commentRating')

        self.author_rating = p_rat * 3 + c_rat
        self.save()

    def __str__(self):
        return f'{self.author_user}'


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.name.title()}'


class Post(models.Model):
    article = 'AR'
    news = 'NW'

    kind = [
        (article, 'Статья'),
        (news, 'Новость')
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    view = models.CharField(max_length=2, choices=kind, default=article)
    time_of_creation = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
    post_rating = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return f'{self.title.title()}: {self.view}'

    def like(self,):
        self.post_rating += 1
        self.save()

    def dislike(self,):
        self.post_rating -= 1
        self.save()

    def preview(self):
        return f'{self.text[:125]} + {"..."}'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Категория публикации'
        verbose_name_plural = 'Категории Публикаций'

    def __str__(self):
        return f'{self.post}, {self.category}'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self,):
        self.comment_rating -= 1
        self.save()
