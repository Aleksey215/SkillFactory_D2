"""
В данном файле прописывается логика приложения.
Суть представления(views) в джанго - это запрос ин-ии из модели в файле models и
передача ее в шаблон(templates)

После создания представлений, нужно указать адреса, по которым будут доступны представления.
Для настройки адресов используется файл "urls.py" но не тот, который лежит в проекте, а тот
что нужно создать в приложении и указать на него ссылкой из основного файла.
"""
from django.shortcuts import render
# импорт дженериков для представлений.
# дженерики - это элементы, которые позволяют визуализировать ин-ию из БД в браузере, при помощи HTML
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail

# Импорт пользовательских элементов:
# модели - передают ин-ию из БД
from .models import Post, Category
# фильтров
from .filters import PostFilter
# форм
from .forms import PostForm


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'news/index.html'

    def get_context_data(self, **kwargs):
        # получили весь контекст из класса-родителя
        context = super().get_context_data(**kwargs)
        # добавили новую контекстную переменную is_no t_premium
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context
    # Чтобы ответить на вопрос, есть ли пользователь в группе, мы заходим в переменную запроса self.request
#     Из этой переменной мы можем вытащить текущего пользователя. В поле groups хранятся все группы,
#     в которых он состоит. Далее мы применяем фильтр к этим группам и ищем ту самую, имя которой premium.
#     После чего проверяем, есть ли какие-то значения в отфильтрованном списке.
#     Метод exists() вернет True, если группа premium в списке групп пользователя найдена, иначе — False.
#     А нам нужно получить наоборот — True, если пользователь не находится в этой группе,
#     поэтому добавляем отрицание not, и возвращаем контекст обратно.


# создаем представление
class CategoryList(ListView):
    # указываем модель из которой берем объекты
    model = Category
    # указываем имя шаблона, в котором написан html для отображения объектов модели
    template_name = 'news/category_list.html'
    # имя переменной, под которым будет передаваться объект в шаблон
    context_object_name = 'categories'


class PostList(ListView):
    model = Post
    template_name = 'news/posts.html'
    context_object_name = 'posts'
    # queryset = Post.objects.order_by('-id')
    ordering = ['-id']  # задаем последовательность отображения по id
    paginate_by = 10  # задаем кол-во отображаемых объектов


class PostsSearch(ListView):
    model = Post
    template_name = 'news/search.html'
    context_object_name = 'posts_search'
    ordering = ['-time_of_creation']

    # метод get_context_data нужен нам для того, чтобы мы могли передать переменные в шаблон.
    # В возвращаемом словаре context будут храниться все переменные.
    # Ключи этого словаря и есть переменные, к которым мы сможем потом обратиться через шаблон
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


# представление для отображения деталей объекта (публикации)
class PostDetailView(DetailView):
    template_name = 'news/post_detail.html'
    queryset = Post.objects.all()


# представление для создания объекта.
class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'news/post_add.html'
    form_class = PostForm
    permission_required = ('news.add_post',)


# представление для редактирования объекта
class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'news/post_add.html'
    form_class = PostForm
    permission_required = ('news.change_post',)

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


# представление для удаления объекта
class PostDeleteView(DeleteView):
    template_name = 'news/post_delete.html'
    queryset = Post.objects.all()
    success_url = '/posts/'


