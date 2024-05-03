import os.path
from django.conf import settings
from django.urls import reverse

PATH_TO_SOCIAL_NETWORKS = 'portfolio/images/social-networks'


class SocialNetwork:
    def __init__(self, name_without_extension, path_relative_static_folder):
        self.name = name_without_extension
        self.path = path_relative_static_folder


path = os.path.join(settings.BASE_DIR, 'portfolio/static', PATH_TO_SOCIAL_NETWORKS)

SOCIAL_NETWORKS = (('Medium', 'Medium.svg'), ('Tumblr', 'Tumblr.svg'), ('ВКонтакте', 'ВКонтакте.svg'),
                   ('Мой Мир', 'Mailru_mir.svg'),
                   ('GitHub', 'GitHub.svg'), ('Boosty', 'Boosty.svg'), ('Instagram', 'Instagram.svg'),
                   ('Одноклассники', 'Одноклассники.svg'), ('Telegram', 'Telegram.svg'), ('Facebook', 'Facebook.svg'),
                   ('Pinterest', 'Pinterest.svg'), ('Twitch', 'Twitch.svg'), ('YouTube', 'YouTube.svg'),
                   ('Reddit', 'Reddit.svg'),
                   ('Dribbble', 'Dribbble.svg'), ('Linkedin', 'Linkedin.svg'), ('Patreon', 'Patreon.svg'),
                   ('Discord', 'Discord.svg'),
                   ('Slack', 'Slack.svg'), ('TikTok', 'TikTok.svg'), ('Behance', 'Behance.svg'))

SOCIAL_NETWORKS = (SocialNetwork(name, os.path.join(PATH_TO_SOCIAL_NETWORKS, file)) for (name, file) in
                   SOCIAL_NETWORKS)


def get_path_to_user_avatar(instance, filename):
    return f'images/users/user_{instance.user.id}/{filename}'


class GetProfileMixin:
    context_object_name = 'user_profile'
    slug_url_kwarg = 'nickname'
    slug_field = 'nickname'


class ProfileSuccessUrlMixin:
    custom_success_url = ''

    def get_success_url(self):
        return reverse(self.custom_success_url, kwargs={'nickname': self.request.user.profile.nickname})


class ContextUpdateMixin:
    PageTitle = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['PageTitle'] = self.PageTitle
        return context
