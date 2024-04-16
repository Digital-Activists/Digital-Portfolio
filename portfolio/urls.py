from django.urls import path

from .views import *

urlpatterns = [
    # path('/', , name=''),
    path('', index, name='home'),
    path('register/', register, name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('reset_password/', reset_password, name='reset_password'),
    path('email_recovery/', EmailRecovery.as_view(), name='email_recovery'),
    path('enter_code_from_email/', enter_code_from_email, name='enter_code_from_email'),
]
