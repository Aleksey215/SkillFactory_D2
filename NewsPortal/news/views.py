from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post, PostCategory


class PostList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'

