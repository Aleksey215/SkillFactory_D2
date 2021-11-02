from django_filters import FilterSet
from .models import Post


class PostFilter(FilterSet):

    class Meta:
        model = Post
        fields = {
            'time_of_creation': ['gte'],
            'title': ['icontains'],
            'author': ['exact'],
        }
        # fields = ('time_of_creation', 'title', 'author', 'view')