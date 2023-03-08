from django.urls import path
from . import views
from django.utils.translation import gettext_lazy as _

app_name = 'blogs'

urlpatterns = [
    path('', views.MagazinesView.as_view(), name="magazines"),
    path('magazine/<int:pk>/', views.MagazineView.as_view(), name="magazine_details"),
    path('blog/<int:pk>/', views.BlogView.as_view(), name="blog_details"),
    path('author/<int:pk>/', views.AuthorView.as_view(), name="author_details"),
    path('create/author/', views.AuthorCreateView.as_view(), name="create_author"),
    path('author/<int:pk>/delete', views.DeleteAuthorView.as_view(), name="delete_author"),
    # path('test/', views.translation_view1),
    # path('page/<int:page>/', views.TranslationView2.as_view()),
    # path(_('test2/'), views.translation_view3),
    # path('difference/', views.gettext_and_gettext_lazy),
    # path('Localize/', views.LocalizationView.as_view()),
    # path('profit/', views.ProfitView.as_view()),
    # path('timezone/', views.set_timezone, name="set_timezone"),
    # path('middleware/', views.MyTestView.as_view()),
    # path('handle/', views.handel_middleware),
    # path('send/', views.MyEmailView.as_view(), name="send_email"),
    # path('name/', views.NameView.as_view(), name="name"),
    path('contact/', views.ContactView.as_view(), name="contact_us"),
    path('manage/', views.manage_articles),
]
