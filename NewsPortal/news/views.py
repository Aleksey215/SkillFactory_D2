"""
В данном файле прописывается логика приложения.
Суть представления(views) в джанго - это запрос ин-ии из модели в файле models и
передача ее в шаблон(templates)

После создания представлений, нужно указать адреса, по которым будут доступны представления.
Для настройки адресов используется файл "urls.py" но не тот, который лежит в проекте, а тот
что нужно создать в приложении и указать на него ссылкой из основного файла.

Django поддерживает несколько разных видов представлений:
1) Class-based views — представления, организованные в виде классов.
2) Generic class-based views — часто используемые представления, которые Django предлагает в виде решения «из коробки».
   Они реализуют в первую очередь функционал CRUD (Create Read Update Delete).
3) Function-based views — представления в виде функций.

"""
from django.shortcuts import render, reverse, redirect
# импорт дженериков для представлений.
# дженерики - это элементы, которые позволяют визуализировать ин-ию из БД в браузере, при помощи HTML
from django.template.loader import render_to_string
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail, EmailMultiAlternatives
from django.contrib.auth.decorators import login_required

# Импорт пользовательских элементов:
# модели - передают ин-ию из БД
from .models import Post, Category, CategorySubscribers
# фильтры - прописываются в файле filters.py
# используются для отбора объектов по каким то критериям
from .filters import PostFilter
# формы - прописываются в файле forms.py
# используются для создания форм в браузере по модели
from .forms import PostForm


# generic-представление для отображения шаблона,
# унаследовав кастомный класс-представление от TemplateView и указав имя шаблона,
# так же унаследовали это представление от миксина проверки аутентификации.
# class IndexView(LoginRequiredMixin, TemplateView):
#     template_name = 'news/index.html'
#
#     def get_context_data(self, **kwargs):
#         # получили весь контекст из класса-родителя
#         context = super().get_context_data(**kwargs)
#         # добавили новую контекстную переменную is_not_authors
#         context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
#         return context
    # Чтобы ответить на вопрос, есть ли пользователь в группе, мы заходим в переменную запроса self.request
#     Из этой переменной мы можем вытащить текущего пользователя. В поле groups хранятся все группы,
#     в которых он состоит. Далее мы применяем фильтр к этим группам и ищем ту самую, имя которой premium.
#     После чего проверяем, есть ли какие-то значения в отфильтрованном списке.
#     Метод exists() вернет True, если группа premium в списке групп пользователя найдена, иначе — False.
#     А нам нужно получить наоборот — True, если пользователь не находится в этой группе,
#     поэтому добавляем отрицание not, и возвращаем контекст обратно.


class PostList(ListView):
    model = Post
    template_name = 'news/posts.html'
    context_object_name = 'posts'
    # queryset = Post.objects.order_by('-id')
    ordering = ['-id']  # задаем последовательность отображения по id
    paginate_by = 10  # задаем кол-во отображаемых объектов на странице


# Представление, созданное для поиска объектов по фильтрам
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
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset()) # вписываем наш фильтр в контекст
        return context


# представление для отображения деталей объекта (публикации)
class PostDetailView(DetailView):
    template_name = 'news/post_detail.html'
    # получение информации об объекте из БД
    queryset = Post.objects.all()


# представление для создания объекта.
class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'news/post_add.html'
    # указываем класс формы, созданный в файле forms.py
    form_class = PostForm
    permission_required = ('news.add_post',)  # создание разрешения на создание

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST)
        post_category_pk = request.POST['post_category']
        print(post_category_pk)
        sub_text = request.POST.get('text')
        sub_title = request.POST.get('title')
        post_category = Category.objects.get(pk=post_category_pk)
        print(post_category)
        subscribers = post_category.subscribers.all()
        print(subscribers)
        # получаем адрес хоста и порта (в нашем случае 127.0.0.1:8000), чтоб в дальнейшем указать его в ссылке
        # в письме, чтоб пользователь мог с письма переходить на наш сайт, на конкретную новость
        host = request.META.get('HTTP_HOST')

        if form.is_valid():
            news = form.save(commit=False)
            news.save()
            print('Статья:', news)

        for subscriber in subscribers:
            print('Адреса рассылки:', subscriber.email)

            # (6)
            # html_content = render_to_string(
            #     'news/mail_sender.html', {'user': subscriber, 'text': sub_text[:50], 'post': news, 'host': host})
            html_content = render_to_string(
                'news/mail.html', {'user': subscriber, 'text': sub_text[:50], 'post': news, 'host': host}
            )

            # (7)
            msg = EmailMultiAlternatives(
                # Заголовок письма, тема письма
                subject=f'Здравствуй, {subscriber.username}. Новая статья в вашем разделе!',
                # Наполнение письма
                body=f'{sub_text[:50]}',
                # От кого письмо (должно совпадать с реальным адресом почты)
                from_email='kalosha21541@yandex.ru',
                # Кому отправлять, конкретные адреса рассылки, берем из переменной, либо можно явно прописать
                to=[subscriber.email],
            )

            msg.attach_alternative(html_content, "text/html")
            # print(html_content)
            msg.send()
            print(post_category)
        return redirect('/posts/')


# представление для редактирования объекта
class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'news/post_add.html'
    # форм класс нужен, чтобы получать доступ к форме через метод POST
    form_class = PostForm
    permission_required = ('news.change_post',)  # создание разрешения на редактирование

# !!!! редактирование и создание поста осуществляется в одном и том же шаблоне news/post_add.html.
# Для этого достаточно просто прописать класс формы в атрибутах класса (form_class = PostForm), не меняя при этом шаблон.

    # метод get_object мы используем вместо queryset,
    # чтобы получить информацию об объекте из БД, который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


# представление для удаления объекта
class PostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = 'news/post_delete.html'
    permission_required = ('news.delete_post',)  # создания разрешения на удаление
    queryset = Post.objects.all()  # получение ин-ии об объекте из БД
    success_url = '/posts/'  # путь, по которому мы перейдем после удаления поста


# создаем представление
class CategoryList(ListView):
    # указываем модель из которой берем объекты
    model = Category
    # указываем имя шаблона, в котором написан html для отображения объектов модели
    template_name = 'news/category_list.html'
    # имя переменной, под которым будет передаваться объект в шаблон
    context_object_name = 'categories'


class CategoryDetail(DetailView):
    template_name = 'news/category_subscription.html'
    model = Category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('pk')
        category_subscribers = Category.objects.filter(pk=category_id).values("subscribers__username")
        context['is_not_subscribe'] = not category_subscribers.filter(subscribers__username=self.request.user).exists()
        context['is_subscribe'] = category_subscribers.filter(subscribers__username=self.request.user).exists()
        return context


@login_required
def add_subscribe(request, **kwargs):
    pk = request.GET.get('pk', )
    print('Пользователь', request.user, 'добавлен в подписчики категории:', Category.objects.get(pk=pk))
    Category.objects.get(pk=pk).subscribers.add(request.user)
    return redirect('/posts/categories')


@login_required
def del_subscribe(request, **kwargs):
    pk = request.GET.get('pk', )
    print('Пользователь', request.user, 'удален из подписчиков категории:', Category.objects.get(pk=pk))
    Category.objects.get(pk=pk).subscribers.remove(request.user)
    return redirect('/posts/categories')



