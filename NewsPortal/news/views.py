from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Post, PostCategory, Category
from .filters import PostFilter
from .forms import PostForm


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


# дженерик для отображения деталей объекта
class PostDetailView(DetailView):
    template_name = 'news/post_detail.html'
    queryset = Post.objects.all()


# дженерик для создания объекта.
class PostCreateView(LoginRequiredMixin, CreateView):
    template_name = 'news/post_add.html'
    form_class = PostForm


# дженерик для редактирования объекта
class PostUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'news/post_add.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


# дженерик для удаления товара
class PostDeleteView(DeleteView):
    template_name = 'news/post_delete.html'
    queryset = Post.objects.all()
    success_url = '/posts/'


