
from django.contrib import admin
from django.urls import path,include
from django.contrib.staticfiles.urls import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('hand.urls'))
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
