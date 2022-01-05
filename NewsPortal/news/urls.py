"""
Данный файл описывает продолжение адреса для конкретного приложения.
То есть главный файл urls.py ссылается на файл news.urls и приписывает в начале адреса: posts/ (например)
после чего начинают действовать адреса, указанные в этом файле в переменной "urlpatterns"
Главный файл забирает все адреса из этого файла, чтобы выстроить полный путь
"""

from django.urls import path
# Импортируем представления, написанные в файле "views.py"
from .views import PostList, PostsSearch, PostDetailView, \
    PostCreateView, PostUpdateView, PostDeleteView, \
    IndexView, CategoryList

# создаем список всех url-адресов данного приложения
# мысленно добавляем к каждому адресу: posts/ из главного файла
urlpatterns = [
    # по пустому адресу мы получаем список публикаций как представление
    path('', PostList.as_view(), name='posts'),  # т. к. сам по себе это класс,
    # то нам надо представить этот класс в виде view. Для этого вызываем метод as_view

    path('search/', PostsSearch.as_view(), name='search'),

    # адрес к конкретному объекту по его id или pk
    # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),

    path('add/', PostCreateView.as_view(), name='post_add'),
    path('add/<int:pk>', PostUpdateView.as_view(), name='post_update'),
    path('delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),
    path('profile/', IndexView.as_view()),
    path('categories/', CategoryList.as_view(), name='categories')
]
