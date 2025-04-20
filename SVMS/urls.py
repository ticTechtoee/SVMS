from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboardApp.urls')),
    path('company/', include('companyApp.urls')),
    path('vehicle/', include('vehicleApp.urls')),
    path('account/', include('accountApp.urls')),
    path('reminder/', include('reminderApp.urls')),
    path('prediction/', include('predictionApp.urls')),
]
# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)