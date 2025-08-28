
from django.contrib import admin
from django.urls import path, include, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import home

urlpatterns = [
    path('notify/', include('notify.urls')),

    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('auth/', include('accounts.urls')),
    path('outpasses/', include('outpasses.urls')),
    path('gate/', include('gate.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
