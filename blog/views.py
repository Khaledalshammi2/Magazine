from django.shortcuts import render
from .models import *
from django.views.generic import ListView, DetailView
from django.utils.translation import gettext as _, ngettext, gettext_lazy
from django.utils.text import format_lazy
from django.views import View
from django.http import HttpResponse
from django.utils.translation import pgettext


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


def translation_view1(request):
    # may have several meaning, so we can define its meaning
    month = pgettext("month name", "May")
    # npgettext() with plural
    output = _("Hello world, We are in %(month)s") % {'month': month}
    return HttpResponse(output)

class TranslationView2(View):
    def get(self, request, page):
        pluralization = ngettext(
            "I'm in page %(page)d",
            "I'm in pages %(page)d",
            page,
        ) % {
                'page': page,
                }
        return HttpResponse(pluralization)


def translation_view3(request):
    # name = gettext_lazy('Khaled')
    name = _('Khaled')
    age = _(20)
    # result = format_lazy('{name}: {age} years old', name=name, age=age)
    result = "%(name)s %(age)d years old" % {"name": name, "age": age}
    return render(request, "translation_template1.html", {"result": result})
