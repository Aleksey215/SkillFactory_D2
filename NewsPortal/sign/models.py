from django.db import models
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


# Create your models here.
class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2", )


class BasicSignupForm(SignupForm):

    def save(self, request):
        # мы вызываем этот же метод класса-родителя,
        # чтобы необходимые проверки и сохранение в модель User были выполнены.
        user = super(BasicSignupForm, self).save(request)
        # получаем объект модели группы basic
        common_group = Group.objects.get(name='common')
        # через атрибут user_set, возвращающий список всех пользователей этой группы,
        # мы добавляем нового пользователя в эту группу
        common_group.user_set.add(user)
        # Обязательным требованием метода save()
        # является возвращение объекта модели User по итогу выполнения функции.
        return user