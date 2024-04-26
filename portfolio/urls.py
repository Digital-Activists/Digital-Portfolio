from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('register/', register, name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('enter-email/', EnterEmailToResetPassword.as_view(), name='enter_email'),
    path('set-new-password/<uidb64>/<token>/', UserResetPasswordConfirm.as_view(), name='reset_password'),
    path('eidt-settings-account', EditAccountInformationView.as_view(), name='edit_settings_account'),
    path('edit-settings-profile', EditProfileInformationView.as_view(), name='edit_settings_profile'),
    # path('edit-settings-security', .as_view(), name='edit_settings_security'),
]
