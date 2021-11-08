from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

from .models import BaseRegisterForm


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/posts/profile'


@login_required
def upgrade_me(request):
    # мы получили объект текущего пользователя из переменной запроса
    user = request.user
    # Вытащили premium-группу из модели Group
    author_group = Group.objects.get(name='authors')
    # проверяем, находится ли пользователь в этой группе
    if not request.user.groups.filter(name='authors').exists():
        # если он все-таки еще не в ней — смело добавляем.
        author_group.user_set.add(user)
    return redirect('/posts/profile/')
