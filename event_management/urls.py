from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls
from core.views import home, contact


urlpatterns = [
    path("", home, name="home"),
    path("contact-us/", contact, name="contact-us"),
    path("", include("events.urls")),
    path("users/", include("user.urls")),
    path("admin/", admin.site.urls),
] + debug_toolbar_urls()

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
