from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib import admin
from django.utils.translation import gettext_lazy as _


# used with Model fields, relationships, verbose_name, help_text, Model methods description


class Author(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    profile_image = models.ImageField(upload_to='profile_images/')
    bio = models.TextField()

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('blogs:author_details', args={self.pk})


class Magazine(models.Model):
    title = models.CharField(max_length=150)
    publish_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse('blogs:magazine_details', args={self.pk})


class Blog(models.Model):
    STATUS_CHOICES = [
        ('d', 'Draft'),
        ('p', 'Published'),
        ('w', 'Withdrawn'),
    ]
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    content = models.TextField()
    magazine = models.ForeignKey(Magazine, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    cover_image = models.ImageField(upload_to='blog_covers/')
    publish_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse('blogs:blog_details', args={self.pk})


class Person(models.Model):
    name = models.CharField(max_length=100, help_text=_('Enter your fullname'))
    age = models.IntegerField()

    class Meta:
        verbose_name = _('person')
        verbose_name_plural = _('persons')

    @admin.display(description=_('above 18'))
    def above_20(self):
        return self.age > 18


class Car(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name=_('car'), )
