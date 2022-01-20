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
    CategoryList, add_subscribe, del_subscribe, CategoryDetail

# создаем список всех url-адресов данного приложения
# мысленно добавляем к каждому адресу: posts/ из главного файла
# в переменной name указываем имя шаблона для визуализации
urlpatterns = [
    # по пустому адресу мы получаем список публикаций как представление
    path('', PostList.as_view(), name='posts'),  # т. к. сам по себе это класс,
    # то нам надо представить этот класс в виде view. Для этого вызываем метод as_view

    # адрес для поиска постов
    path('search/', PostsSearch.as_view(), name='search'),

    # адрес к конкретному объекту по его id или pk
    # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),

    # адрес для добавления поста
    path('add/', PostCreateView.as_view(), name='post_add'),

    # адрес для редактирования выбранного поста
    path('add/<int:pk>', PostUpdateView.as_view(), name='post_update'),

    # адрес для удаления выбранного поста
    path('delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),

    # адрес для просмотра категорий
    path('categories/', CategoryList.as_view(), name='categories'),
    path('categories/<int:pk>/add_subscribe/', add_subscribe, name='add_subscribe'),
    path('categories/<int:pk>/del_subscribe/', del_subscribe, name='del_subscribe'),
    path('categories/<int:pk>/', CategoryDetail.as_view(), name='category_subscription'),


]
