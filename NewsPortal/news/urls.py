from django.urls import path
from .views import PostList, PostsSearch

urlpatterns = [
    path('', PostList.as_view()),
    # path('<int:pk>', PostDetail.as_view()),
    path('search/', PostsSearch.as_view()),
]
