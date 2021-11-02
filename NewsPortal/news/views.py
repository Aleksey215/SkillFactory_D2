from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post, Category
from .filters import PostFilter


class PostList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    # queryset = Post.objects.order_by('-id')
    ordering = ['-id']
    paginate_by = 10


class PostsSearch(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'posts_search'
    ordering = ['-time_of_creation']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context

# class PostDetail(DetailView):
#     model = Post
#     template_name = 'post.html'
#     context_object_name = 'post'
#



