from django.urls import path

from .views import *

urlpatterns = [
    path('', portfolio, name='home'),
    path('register/', register, name='register'),
]
