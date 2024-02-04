from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from django.urls import re_path
from django.views.static import serve
from django.conf.urls import handler500

urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),


    path('admin/', admin.site.urls),
    path('',include('DjangoVidDownloader.urls')),
    
    
    
]

handler404='DjangoVidDownloader.views.handling_404'
handler500 = 'DjangoVidDownloader.views.custom_500'

