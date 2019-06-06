from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

from rest_framework.urlpatterns import format_suffix_patterns

# browsers make a request for /favicon.ico whenever
# they send a GET request to any page for rendering
# a favicon in the browser tab hence the RedirectView
favicon_view = RedirectView.as_view(url='/static/imgs/favicon.ico', permanent=True)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('favicon.ico', favicon_view),
    path('api/', include('backend.api')),
    path('rest-framework-auth/', include('rest_framework.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)
