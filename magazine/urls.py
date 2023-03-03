from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import JavaScriptCatalog
from django.views.decorators.cache import cache_page
from django import get_version

urlpatterns = [
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('blog.urls', namespace='blogs')),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
