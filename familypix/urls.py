from django.conf import settings
from django.conf.urls import patterns, url, include
from django.contrib import admin

from familypix import views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'familypix.views.index', name='index'),
    url(r'^admin/', include(admin.site.urls)),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^album', views.album, name='album'),
    (r'^ckeditor/', include('ckeditor.urls')),
    )