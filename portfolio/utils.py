import re
import os.path
from django.conf import settings
from django.urls import reverse

PATH_TO_SOCIAL_NETWORKS = 'portfolio/images/social-networks'
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

SOCIAL_NETWORKS = {name: os.path.join(PATH_TO_SOCIAL_NETWORKS, file) for (name, file) in
                   SOCIAL_NETWORKS}
social_networks_patterns = {
    'Medium': r'https?://medium\.com/@[A-Za-z0-9_]+/?',
    'Tumblr': r'https?://[A-Za-z0-9_]+\.tumblr\.com/?',
    'ВКонтакте': r'https?://vk\.com/[A-Za-z0-9_]+/?',
    'Мой Мир': r'https?://my\.mail\.ru/[A-Za-z0-9_]+/?',
    'GitHub': r'https?://github\.com/[A-Za-z0-9_]+/?',
    'Boosty': r'https?://boosty\.to/[A-Za-z0-9_]+/?',
    'Instagram': r'https?://www\.instagram\.com/[A-Za-z0-9_]+/?',
    'Одноклассники': r'https?://ok\.ru/[A-Za-z0-9_]+/?',
    'Telegram': r'https?://t\.me/[A-Za-z0-9_]+/?',
    'Facebook': r'https?://www\.facebook\.com/[A-Za-z0-9_]+/?',
    'Pinterest': r'https?://www\.pinterest\.com/[A-Za-z0-9_]+/?',
    'Twitch': r'https?://www\.twitch\.tv/[A-Za-z0-9_]+/?',
    'YouTube': r'https?://www\.youtube\.com/user/[A-Za-z0-9_]+/?',
    'Reddit': r'https?://www\.reddit\.com/user/[A-Za-z0-9_]+/?',
    'Dribbble': r'https?://dribbble\.com/[A-Za-z0-9_]+/?',
    'Linkedin': r'https?://www\.linkedin\.com/in/[A-Za-z0-9_]+/?',
    'Patreon': r'https?://www\.patreon\.com/[A-Za-z0-9_]+/?',
    'Discord': r'https?://discord\.gg/[A-Za-z0-9_]+/?',
    'Slack': r'https?://[A-Za-z0-9_]+\.slack\.com/?',
    'TikTok': r'https?://www\.tiktok\.com/@[A-Za-z0-9_]+/?',
    'Behance': r'https?://www\.behance\.net/[A-Za-z0-9_]+/?',
}


def check_social_lick_type(social_network_type):
    return social_network_type in social_networks_patterns


def check_social_link(social_network, url):
    pattern = social_networks_patterns.get(social_network)
    result = re.match(pattern, url)
    return result is not None


def get_path_to_user_avatar(instance, filename):
    return f'images/users/user_{instance.user.id}/{filename}'


def get_path_to_post_files(instance, filename):
    return f'posts/user_{instance.post.author.id}/{instance.post.id}/{filename}'


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
