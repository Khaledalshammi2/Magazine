from django.shortcuts import render
from .models import *
from django.views.generic import ListView, DetailView, TemplateView
from django.utils.translation import gettext as _, ngettext, gettext_lazy
from django.utils.text import format_lazy
from django.views import View
from django.http import HttpResponse
from django.utils.translation import pgettext
from django.utils.functional import lazy
from django.utils.safestring import mark_safe
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
import pytz
from .forms import ProfitForm


class Magazines(ListView):
    template_name = "blog/homepage.html"
    queryset = Magazine.objects.all().order_by("-publish_date")
    context_object_name = "magazines"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extra_data = self.request.extra_data
        context['extra_data'] = extra_data
        return context


class Magazine(DetailView):
    model = Magazine
    template_name = "blog/magazine_details.html"
    context_object_name = "magazine"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blogs = Blog.objects.filter(magazine_id=self.kwargs['pk'], status="p").order_by("-publish_date")
        context["blogs"] = blogs
        return context


class BlogView(DetailView):
    model = Blog
    template_name = "blog/blog_details.html"
    context_object_name = "blog"


class AuthorView(DetailView):
    template_name = "blog/author.html"
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


mark_safe_lazy = lazy(mark_safe, str)


def translation_view3(request):
    # name = gettext_lazy('Khaled')
    name = _('Khaled')
    age = _("20 years old")
    # result = format_lazy('{name}: {age} years old', name=name, age=age)
    result = "%(name)s %(age)s" % {"name": name, "age": age}
    test = mark_safe_lazy(_("<p>programmer</p>"))
    return render(request, "blog/translation_template1.html", {
        "result": result,
        "test": test})


# def gettext_and_gettext_lazy(request):
#     name = gettext_lazy('Khaled ')
#     age = _("20 years old")
#     return render(request, "blog/translation_template2.html", {
#         "name": name,
#         "age": age
#     })
#
#
# class LocalizationView(View):
#     def get(self, request):
#         car = Car.objects.get(pk=1)
#         return render(request, "blog/localization.html", {"car": car})
#
# class ProfitView(FormView):
#     form_class = ProfitForm
#     template_name = "blog/profit.html"
#     success_url = reverse_lazy('blogs:magazines')
#     def form_valid(self, form):
#         storage = form.cleaned_data['storage']
#         profit = form.cleaned_data['profit']
#         person = Person.objects.get(pk=1)
#         Car.objects.create(person=person, storage=storage, profit=profit)
#         return super().form_valid(form)
#
#
# def set_timezone(request):
#     if request.method == 'POST':
#         request.session['django_timezone'] = request.POST['timezone']
#         return redirect('/')
#     else:
#         return render(request, 'blog/time_zone_template.html', {'timezones': pytz.common_timezones})


# class MyTestView(TemplateView):
#     template_name = 'my_template.html'

# def handel_middleware(request):
#     return HttpResponse(fd)