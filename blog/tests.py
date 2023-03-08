from django.test import TestCase, RequestFactory, Client
from django.utils import translation

from .models import Person, Magazine
from django.urls import reverse, resolve
from .views import MagazinesView, MagazineView
from django.utils.translation import gettext_lazy as _


class PersonTestCase(TestCase):
    def setUp(self):
        Person.objects.create(name="khaled", name_ar="خالد", age=20, age_ar=20)
        Person.objects.create(name="mohamed", name_ar="محمد", age=1, age_ar=1)

    def test_persons(self):
        khaled = Person.objects.get(name='khaled')
        mohamed = Person.objects.get(name='mohamed')
        # nour = Person.objects.get(name='nour')
        #
        # self.assertEqual(khaled.person_details(), "khaled, 20 years old")
        # self.assertEqual(mohamed.person_details(), "mohamed, 1 year old")
        # self.assertEqual(nour.person_details(), "nour, 15 years old")


def create_magazine(title, title_ar, description, description_ar):
    return Magazine.objects.create(title=title, title_ar=title_ar, description=description,
                                   description_ar=description_ar)


class MagazineTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_magazine(self):
        factory = RequestFactory()
        request = factory.get(reverse('blogs:magazines'))
        response = MagazinesView.as_view()(request)
        view_func, args, kwargs = resolve(request.path_info)
        view_class = view_func.view_class

        # check if func of resolver_match equal Magazines CBV
        self.assertEqual(view_class, MagazinesView)
        self.assertIs(view_class, MagazinesView)
        # with self.assertRaises(ValueError, msg="Custom error message"):

    def test_magazine_context(self):
        create_magazine('khfhsd', 'سليليس', 'shgdsgdg', 'لصسالاساتف')
        create_magazine('khfhsd', 'سليليس', 'shgdsgdg', 'لصسالاساتف')
        create_magazine('khfhsd', 'سليليس', 'shgdsgdg', 'لصسالاساتف')
        create_magazine('khfhsd', 'سليليس', 'shgdsgdg', 'لصسالاساتف')
        create_magazine('khfhsd', 'سليليس', 'shgdsgdg', 'لصسالاساتف')
        response = self.client.get(reverse('blogs:magazines'))
        self.assertEqual(len(response.context['magazines']), 5)


class MyTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    # def test_session(self):
    #     client = Client()
    #     client.session['my_key'] = 'my_value'
    #     client.session.save()
    #     my_value = client.session.get('my_key')
    #     self.assertEqual(my_value, 'my_value')
    def test_arabic(self):
        with translation.override('ar'):
            self.assertEqual(_('name'), 'الاسم')
            response = self.client.get(reverse('blogs:magazines'))
            self.assertContains(response, "خالد")
            # self.assertEqual(response.content, "خالد")
