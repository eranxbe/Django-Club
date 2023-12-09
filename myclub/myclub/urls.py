from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('events.urls')),
    path('members/', include('django.contrib.auth.urls')),
    path('members/', include('members.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Config Admin Titles

admin.site.site_header = "My Club Administration Page"
admin.site.site_title = "My Club"
admin.site.index_title = "My Club Administration"
