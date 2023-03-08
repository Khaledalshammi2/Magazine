from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib import admin
from django.utils.translation import gettext_lazy as _, get_language
from django.utils import timezone
import datetime
from django.contrib.auth.models import Permission
from django.utils.translation import ngettext


# used with Model fields, relationships, verbose_name, help_text, Model methods description


class Author(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Name"))
    email = models.EmailField(verbose_name=_("Email"))
    profile_image = models.ImageField(upload_to='profile_images/', verbose_name=_("Profile Image"))
    bio = models.TextField(verbose_name=_("Bio"))
    bio_ar = models.TextField(verbose_name=_("Bio in arabic"), null=True, default="")

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse('blogs:author_details', args={self.pk})

    class Meta:
        verbose_name = _('author')
        verbose_name_plural = _('authors')

    def get_bio(self):
        language = get_language()
        if language == "ar":
            return self.bio_ar
        return self.bio


# class MagazineQuerySet(models.QuerySet):
#     def magazines(self):
#         return self.all().order_by("-publish_date")

# class MagazineManager(models.Manager):
#     def get_queryset(self):
#         return MagazineQuerySet(self.model, using=self._db)#
#     def magazines(self):
#         return self.get_queryset().magazines()


class MagazineManager(models.Manager):
    def magazines(self):
        # return super().get_queryset().all().order_by("-publish_date")
        return self.all().order_by("-publish_date")


class Magazine(models.Model):
    title = models.CharField(max_length=150, verbose_name=_("Title"))
    title_ar = models.CharField(max_length=150, null=True, default="", verbose_name=_("Title in arabic"))
    publish_date = models.DateTimeField(auto_now_add=True, verbose_name=_("Publish date"))
    description = models.TextField(verbose_name=_("Description"))
    description_ar = models.TextField(null=True, default="", verbose_name=_("Description in arabic"))

    # magazines = MagazineManager()
    # objects = MagazineQuerySet.as_manager() instead of MagazineManager class
    objects = MagazineManager()

    def __str__(self) -> str:
        language = get_language()
        if language == "ar":
            return self.title_ar
        return self.title

    def get_absolute_url(self):
        return reverse('blogs:magazine_details', args={self.pk})

    class Meta:
        verbose_name = _('magazine')
        verbose_name_plural = _('magazines')

    def get_title(self):
        language = get_language()
        if language == "ar":
            return self.title_ar
        return self.title

    def get_description(self):
        language = get_language()
        if language == "ar":
            return self.description_ar
        return self.description


class BlogManager(models.Manager):
    def published_magazines(self, magazine):
        blogs = Blog.objects.filter(magazine_id=magazine, status="p")
        return blogs.order_by("-publish_date")

    def author_blogs(self, author):
        blogs = Blog.objects.filter(author=author, status='p')
        return blogs


class Blog(models.Model):
    STATUS_CHOICES = [
        ('d', _('Draft')),
        ('p', _('Published')),
        ('w', _('Withdrawn')),
    ]
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name=_("Author"))
    title = models.CharField(max_length=150, verbose_name=_("Title"))
    title_ar = models.CharField(max_length=150, null=True, default="", verbose_name=_("Title in arabic"))
    content = models.TextField(verbose_name=_("Content"))
    content_ar = models.TextField(null=True, default="", verbose_name=_("Content in arabic"))
    magazine = models.ForeignKey(Magazine, on_delete=models.CASCADE, verbose_name=_("Magazine"))
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name=_("Status"))
    cover_image = models.ImageField(upload_to='blog_covers/', verbose_name=_("Image"))
    publish_date = models.DateTimeField(auto_now_add=True, verbose_name=_("Publish date"))

    objects = BlogManager()

    def __str__(self):
        language = get_language()
        if language == "ar":
            return self.title_ar
        return self.title

    def get_absolute_url(self):
        return reverse('blogs:blog_details', args={self.pk})

    class Meta:
        verbose_name = _('blog')
        verbose_name_plural = _('blogs')

    def get_title(self):
        language = get_language()
        if language == "ar":
            return self.title_ar
        return self.title

    def get_content(self):
        language = get_language()
        if language == "ar":
            return self.content_ar
        return self.content

    def get_status(self):
        return self.status


class PersonManager(models.Manager):
    # Person.objects.manager_only_method()
    def manager_only_method(self):
        return self.all()


class PersonQuerySet(models.QuerySet):
    # Person.objects.manager_and_queryset_method()
    def manager_and_queryset_method(self):
        return self.all()


MyManager = PersonManager.from_queryset(PersonQuerySet)


class Person(models.Model):
    name = models.CharField(max_length=100, help_text=_('Enter your fullname'), verbose_name=_("Name"))
    name_ar = models.CharField(max_length=100, null=True, default="", verbose_name=_("Arabic Name"))
    age = models.IntegerField(verbose_name=_("Age"))
    age_ar = models.IntegerField(verbose_name=_("Arabic age"))

    objects = MyManager()

    class Meta:
        verbose_name = _('person')
        verbose_name_plural = _('persons')

    @admin.display(description=_('above 18'))
    def above_20(self):
        return self.age > 18

    def __str__(self):
        language = get_language()
        if language == "ar":
            return self.name_ar
        return self.name

    def person_details(self):
        language = get_language()
        if language == "ar":
            return "%s, %d سنة" % (self.name_ar, self.age_ar)
        return ngettext(
            "%s, %d year old",
            "%s, %d years old",
            self.age
        ) % (self.name, self.age)

    def get_name(self):
        language = get_language()
        if language == "ar":
            return self.name_ar
        return self.name

    def get_age(self):
        language = get_language()
        if language == "ar":
            return self.age_ar
        return self.age


class CarQuerySet(models.QuerySet):
    # Available on both Manager and QuerySet.
    # Car.objects.public_method()
    def public_method(self):
        return self.all()

    # Available only on QuerySet.
    # Car.objects.all()._private_method()
    def _private_method(self):
        return self.all()

    # Available only on QuerySet.
    # Car.objects.all().opted_out_public_method()
    def opted_out_public_method(self):
        return self.all()

    opted_out_public_method.queryset_only = True

    # Available on both Manager and QuerySet.
    # Car.objects._opted_in_private_method()
    def _opted_in_private_method(self):
        return self.all()

    _opted_in_private_method.queryset_only = False


class Car(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name=_('Person'))
    # date = models.DateTimeField(localize=True)
    publish_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Publish_date'))
    storage = models.IntegerField(verbose_name=_('Storage'))
    storage_ar = models.IntegerField(verbose_name=_('Storage in arabic'), null=True, blank=True)
    profit = models.DecimalField(max_digits=4, decimal_places=2, verbose_name=_('Profit'))
    profit_ar = models.DecimalField(max_digits=4, decimal_places=2, verbose_name=_('Profit in arabic'),
                                    null=True, blank=True)

    objects = CarQuerySet.as_manager()

    class Meta:
        verbose_name = _('car')
        verbose_name_plural = _('cars')

    def __str__(self):
        language = get_language()
        if language == "ar":
            return "%s الربح: %s" % (self.person.name_ar, str(self.profit_ar))
        return "%s profit: %s" % (self.person.name, str(self.profit))

    def get_profit(self):
        language = get_language()
        if language == "ar":
            return self.profit_ar
        return self.profit
