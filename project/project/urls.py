from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('demand/', include('main.urls')),
    path('geography/', include('main.urls')),
    path('skills/', include('main.urls')),
    path('vacancies/', include('main.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
