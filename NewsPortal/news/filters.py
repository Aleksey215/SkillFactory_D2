from django_filters import FilterSet, DateFilter
from .models import Post, Category


class PostFilter(FilterSet):
    time_of_creation = DateFilter

    class Meta:
        model = Post
        fields = {
            'post_category': ['exact'],
            'time_of_creation': ['gte'],
            'title': ['icontains'],
            'author': ['exact'],
        }
        # fields = ('time_of_creation', 'title', 'author', 'view')