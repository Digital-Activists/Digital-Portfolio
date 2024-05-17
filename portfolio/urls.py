from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('register/', register, name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('enter-email/', EnterEmailToResetPassword.as_view(), name='enter_email'),
    path('set-new-password/<uidb64>/<token>/', UserResetPasswordConfirm.as_view(), name='reset_password'),

    path('profile:<slug:nickname>/eidt-settings-account', EditAccountInformationView.as_view(), name='edit_settings_account'),
    path('profile:<slug:nickname>/edit-settings-profile', EditProfileView.as_view(), name='edit_settings_profile'),
    path('profile:<slug:nickname>/edit-settings-security', EditSecuritySettingsView.as_view(), name='edit_settings_security'),
    path('profile:<slug:nickname>/edit-settings-tags', EditProfileTagsView.as_view(), name='edit_settings_tags'),

    path('profile:<slug:nickname>/create-post', CreatePostView.as_view(), name='create_post'),
    path('profile:<slug:nickname>/', UserProfileView.as_view(), name='view_user_profile'),
    path('profile:edit-post:<slug:post_slug>', EditPostView.as_view(), name='edit_post'),
    path('profile:edit-post-tags:<slug:post_slug>', EditPostTagsView.as_view(), name='edit_post_tags'),

    path('delete-post:<int:post_id>', delete_post, name='delete_post'),
    path('like-post:<int:post_id>', like_post, name='like_post'),
    path('dislike-post:<int:post_id>', dislike_post, name='dislike_post'),
]
