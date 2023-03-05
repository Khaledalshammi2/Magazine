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
from django.core.mail import BadHeaderError, send_mail, EmailMessage, EmailMultiAlternatives
from django.core import mail
from django.views.generic.edit import CreateView
from django.http import HttpResponse, HttpResponseRedirect
import os

class Magazines(ListView):
    template_name = "blog/homepage.html"
    # queryset = Magazine.magazines.all()
    queryset = Magazine.objects.magazines()
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
        # blogs = Blog.objects.filter(magazine_id=self.kwargs['pk'], status="p").order_by("-publish_date")
        blogs = Blog.objects.published_magazines(magazine=self.kwargs['pk'])
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
        blogs = Blog.objects.author_blogs(author=author)
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

send_mail(
    'sport',
    "it's sport message.",
    'kkhhaa2002yl@gmail.com',
    ['khalod.zeko@gmail.com'],
    fail_silently=False,
)

# I used locmem to testing environments not send a real email
# it will store in memory
# mail.send_mail(
#     'sport',
#     "it's sport message.",
#     'kkhhaa2002yl@gmail.com',
#     ['khalod.zeko@gmail.com'],
#     fail_silently=False,
# )
# emails = mail.outbox
# # emails have list of e email messages

# dummy like locmem, doesn't send a real message + doesn't store it in memory
# mail.send_mail(
#     'Subject here',
#     'Here is the message.',
#     'from@example.com',
#     ['to@example.com'],
#     fail_silently=False,
# )


# message1 = ('Family', 'Family is whole life', 'kkhhaa2002yl@gmail.com',
#             ['khalod.zeko@gmail.com', 'khalod.zeko22@gmail.com'])
# message2 = ('Sport', 'Sport is useful', 'kkhhaa2002yl@gmail.com', ['khalod.alshami@gmail.com'])
# send_mass_mail((message1, message2), fail_silently=False)

class MyEmailView(View):
    template_name = 'send_email.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')
        to_email = request.POST.get('to_email', '')
        if subject and message and to_email:
            try:
                send_mail(subject, message, 'kkhhaa2002yl@gmail.com', [to_email])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return HttpResponseRedirect('/en/')
        else:
            return HttpResponse('Make sure all fields are entered and valid.')

# it has more options like reply_to, attach_file, attach
# email = EmailMessage(
#     'Good morning',
#     "I'm khaled",
#     'kkhhaa2002yl@gmail.com',
#     ['khalod.zeko@gmail.com', 'khalod.zeko22@gmail.com'],
#     ['khalod.alshami@gmail.com'],
#     reply_to=['khalod.zeko@gmail.com'],
#     headers={'Message-ID': 'kh775'},
# )
# email.attach_file('blog/static/images/khaled.jpeg')
# image_path = "blog/static/images/khaled.jpeg"
# with open(image_path, 'rb') as img:
#     image_data = img.read()
#     image_name = os.path.basename(image_path)
#     email.attach(image_name, image_data, 'image/jpeg')
# with open('blog/static/pdf/khaledPDF.pdf', 'rb') as pdf:
#     email.attach('khaledPDF.pdf', pdf.read(), 'application/pdf')
# email.send()



# To send a text and HTML combination message
# html = '<p>An <strong>important</strong> message from khaled</p>'
# msg = EmailMultiAlternatives("Khaled", 'an Important message from khaled',
# "kkhhaa2002yl@gmail.com", ['khalod.zeko@gmail.com'])
# # msg.attach_alternative(html, "text/html")
# msg.send()



# email1 = EmailMessage(
#     'Good morning',
#     "I'm khaled",
#     'kkhhaa2002yl@gmail.com',
#     ['khalod.zeko@gmail.com', 'khalod.zeko22@gmail.com'],
#     headers={'Message-ID': 'kh775'},
# )
# email2 = EmailMessage(
#     'Good morning',
#     "I'm khaled",
#     'kkhhaa2002yl@gmail.com',
#     ['khalod.zeko@gmail.com', 'khalod.zeko22@gmail.com'],
#     headers={'Message-ID': 'kh775'},
# )
# email3 = EmailMessage(
#     'Good morning',
#     "I'm khaled",
#     'kkhhaa2002yl@gmail.com',
#     ['khalod.zeko@gmail.com', 'khalod.zeko22@gmail.com'],
#     headers={'Message-ID': 'kh775'},
# )
#
# # by this way, we will send multiple EmailMessage
# emails = [email1, email2, email3]
# connection = mail.get_connection()
# messages = emails
# connection.send_messages(messages)
