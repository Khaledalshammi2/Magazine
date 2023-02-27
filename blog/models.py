from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


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