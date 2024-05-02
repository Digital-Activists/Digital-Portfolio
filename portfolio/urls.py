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
    path('edit-settings-profile', EditProfileView.as_view(), name='edit_settings_profile'),
    path('submit-social-network-form', submit_social_network, name='submit_social_network_form'),
    path('edit-settings-security', change_user_email_and_password, name='edit_settings_security'),
    path('post-kakogoto-usera', CreatePostView.as_view(), name='create_post'),
    path('profile/<slug:nickname>/', UserProfileView.as_view(), name='view_user_profile'),
    # TODO: Комментарии ниже
]
