from django.urls import path
from . import views

app_name = 'blogs'

urlpatterns = [
    path('', views.Magazines.as_view(), name="magazines"),
    path('magazine/<int:pk>/', views.Magazine.as_view(), name="magazine_details"),
    path('blog/<int:pk>/', views.BlogView.as_view(), name="blog_details"),
    path('author/<int:pk>/', views.AuthorView.as_view(), name="author_details"),
]
