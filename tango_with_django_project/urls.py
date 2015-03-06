from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin

from rango.views import MyRegistrationView

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^rango/', include('rango.urls', namespace='rango')),
    url(r'^accounts/register/$', MyRegistrationView.as_view(), name='registration_register'),
    (r'^accounts/', include('registration.backends.simple.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static', 
        (r'^media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), 
    )


