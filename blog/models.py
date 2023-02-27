from django.db import models
from django.contrib.auth.models import User


class Magazine(models.Model):
    name = models.CharField(max_length=100)
    publisher = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    publication_date = models.DateField(auto_now_add=True)
    description = models.TextField()

    def __str__(self) -> str:
        return self.name




class Blog(models.Model):
    STATUS_CHOICES = [
        ('d', 'Draft'),
        ('p', 'Published'),
        ('w', 'Withdrawn'),
    ]
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    content = models.TextField()
    magazine = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)

    def __str__(self) -> str:
        return self.title
