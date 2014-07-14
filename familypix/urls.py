from django.conf import settings
from django.conf.urls import patterns, url, include
from django.contrib import admin

from familypix import views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'familypix.views.index', name='index'),
    url(r'^addCircle/', 'familypix.views.addCircle', name='addCircle'),
    url(r'^addPhoto/', 'familypix.views.addPhoto', name='addPhoto'),
    url(r'^addAlbum/', 'familypix.views.addAlbum', name='addAlbum'),
    url(r'^upload/', 'familypix.views.photoUpload', name='photoUpload'),
    url(r'^albumUpload/', 'familypix.views.albumUpload', name='albumUpload'),
    url(r'^addAll/', 'familypix.views.addAll', name='addAll'),
    url(r'^file-upload', 'familypix.views.filePost', name='filePost'),
    url(r'^batchFileUpload/(?P<index>\w+)/', 'familypix.views.batchFilePost', name='batchFilePost'),
    url(r'^admin/', include(admin.site.urls)),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^user/(?P<userpage>\w+)/', views.album, name='album'),
    (r'^ckeditor/', include('ckeditor.urls')),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    )
