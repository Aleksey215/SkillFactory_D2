"""
В данном файле создаются и описываются сущности баз данных(БД).
Описываются их поля(атрибуты) и методы.
Для этого используются приемы ООП, а именно - Классы.
Также здесь описываются все связи между сущностями:
один ко многим (One to Many)
многие ко многим (Many to Many)
один к одному (One to one)
"""

from django.core.validators import MinValueValidator
# Импорт модели "Пользователь", чтобы через наследование создать класс "Автор"
from django.contrib.auth.models import User
# Импорт функции для суммирования поля "рейтинг"
from django.db.models import Sum
# Для использования ORM(см. определение), нужно импортировать "models"
from django.db import models


# для создания сущностей в БД через ООП, нужно наследоваться от "models.Model"
# Создание сущности "Автор" в БД
class Author(models.Model):
    # данный атрибут связан с сущностью "User" через связь "Один к Одному"
    author_user = models.OneToOneField(User, on_delete=models.CASCADE)
    # целочисленный атрибут, имеющий значение ноль по умолчанию
    author_rating = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    # Метод обновления рейтинга пользователя
    def update_rating(self):
        # в данное поле записывается сумма всех значений поля "рейтинг" модели "Публикация"
        # но значение в формате queryset. То есть нужно преобразовать
        author_post_rating = self.post_set.aggregate(postRating=Sum('post_rating'))
        # Создаем промежуточную переменную
        p_rat = 0
        # записываем в нее извлеченные данные методом "get" из postRating
        p_rat += author_post_rating.get('postRating')

        author_comment_rating = self.author_user.comment_set.aggregate(commentRating=Sum('comment_rating'))
        c_rat = 0
        c_rat += author_comment_rating.get('commentRating')

        # суммирование переменных (по заданию)
        self.author_rating = p_rat * 3 + c_rat
        # сохраняем результат в БД
        self.save()

    def __str__(self):
        return f'{self.author_user}'


# создание сущности "Категория" в БД
class Category(models.Model):
    # имя категории - текстовое поле длинной не более 64 сим-ов и уникальное(unique)
    name = models.CharField(max_length=64, unique=True)
    # subscribers = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.name}'


# создание сущности "Публикация" в БД
class Post(models.Model):
    # публикация может быть двух видов:
    # AR - article(статья) или NW - news(новость)
    # создали две переменные для каждого вида
    # эти значения будут в базе данных
    article = 'AR'
    news = 'NW'

    # список картежей для выбора вида публикации
    kind = [
        (article, 'Статья'),
        (news, 'Новость')
    ]

    # поле "Автор" - через связь Один ко Многим связано с сущностью "Автор"
    # on_delete задает опцию удаления объекта текущей модели при удалении связанного объекта главной модели.
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    # поле "Вид публикации" - текстовое, длинной=2символа(как в переменных выше),
    # выбирается из списка "kind", по умолчанию - статья
    view = models.CharField(max_length=2, choices=kind, default=article)
    # поле "Время создания" - временное поле, которое хранит время и дату, при создании экземпляра
    time_of_creation = models.DateTimeField(auto_now_add=True)
    # поле "Категория публикации" - берется через связь Многие ко Многим из сущности "Категория"
    # через сущность "Публикация-Категория"
    post_category = models.ManyToManyField(Category, through='PostCategory')
    # поле "Заголовок" - текстовое с макс длинной=128 сим-ов
    title = models.CharField(max_length=128)
    # поле "Текст" - большое текстовое(содержание публикации)
    text = models.TextField()
    # поле "Рейтинг публикации" - целочисленное, по умолчанию=0
    post_rating = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return f'{self.title.title()}: {self.get_view_display()}'

    # Метод, который увеличивает рейтинг на один при вызове
    def like(self,):
        self.post_rating += 1
        self.save()

    # Метод, который уменьшает рейтинг на один при вызове
    def dislike(self,):
        self.post_rating -= 1
        self.save()

    # Метод, который выводит 125 символов текста, а в конце добавляет троеточие
    def preview(self):
        return f'{self.text[:125]} + {"..."}'

    def get_absolute_url(self):
        return f'/posts/{self.id}'


# создание сущности "Пост-Категория" в БД
# является промежуточной таблицей для связи Многие ко Многим
# между сущностью "Публикация" и "Категория"
class PostCategory(models.Model):
    # поле "Публикация" - берется через связь Один ко многим из сущности "Публикация"
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # поле "Категория" - берется через связь Один ко многим из сущности "Категория"
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Категория публикации'
        verbose_name_plural = 'Категории Публикаций'

    def __str__(self):
        return f'{self.post}, {self.category}'


# создание сущности "Комментарий" в БД
class Comment(models.Model):
    # поле "Публикация" - берется через связь Один ко Многим из сущности "Публикация"
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # поле "Пользователь" - берется через связь Один ко Многим из сущности "Пользователь"
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # поле "Текст" - большой текст(содержание комментария)
    text = models.TextField()
    # поле "Время" - сохраняет время и дату создания комментария
    time = models.DateTimeField(auto_now_add=True)
    # поле "Рейтинг_комментария" - целочисленное, отображает рейтинг
    comment_rating = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    # Метод, который увеличивает рейтинг на один при вызове
    def like(self):
        self.comment_rating += 1
        self.save()

    # Метод, который уменьшает рейтинг на один при вызове
    def dislike(self,):
        self.comment_rating -= 1
        self.save()
