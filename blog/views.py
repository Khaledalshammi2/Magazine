from django.shortcuts import render
from .models import *
from django.views.generic import ListView, DetailView
from django.views.generic.detail import SingleObjectMixin


class Magazines(ListView):
    template_name = "homepage.html"
    queryset = Magazine.objects.all().order_by("-publish_date")
    context_object_name = "magazines"

class Magazine(DetailView):
    model = Magazine
    template_name = "magazine_details.html"
    context_object_name = "magazine"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blogs = Blog.objects.filter(magazine_id=self.kwargs['pk'], status="p").order_by("-publish_date")
        context["blogs"] = blogs
        return context



class BlogView(DetailView):
    model = Blog
    template_name = "blog_details.html"
    context_object_name = "blog"


class AuthorView(DetailView):
    template_name = "author.html"
    context_object_name = "author"
    model = Author

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = self.get_object()
        blogs = Blog.objects.filter(author=author, status='p')
        context["blogs"] = blogs
        return context
