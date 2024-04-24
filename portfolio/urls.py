from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('register/', register, name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('enter_email/', EnterEmailToResetPassword.as_view(), name='enter_email'),
    path('set_new_password/<uidb64>/<token>/', SetNewPassword.as_view(), name='reset_password'),
    path('eidt_settings_account', EditAccountInformationView.as_view(), name='edit_settings_account'),
    path('edit_settings_profile', EditProfileInformationView.as_view(), name='edit_settings_profile'),
    # path('edit_settings_security', .as_view(), name='edit_settings_security'),
]
