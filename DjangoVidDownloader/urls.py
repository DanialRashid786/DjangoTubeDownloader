from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView
from django.views.generic import RedirectView

urlpatterns = [
    
    path('', download_video),
    path('<string>', RedirectView.as_view(url='/'))    # Exceptions handling
]


