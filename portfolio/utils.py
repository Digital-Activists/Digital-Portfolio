import os.path
import pathlib
from django.conf import settings

PATH_TO_SOCIAL_NETWORKS = 'portfolio/images/social-networks'


class SocialNetwork:
    def __init__(self, name_without_extension, path_relative_static_folder):
        self.name = name_without_extension
        self.path = path_relative_static_folder


path = os.path.join(settings.BASE_DIR, 'portfolio/static', PATH_TO_SOCIAL_NETWORKS)
file_filter = '*.svg'

SOCIAL_NETWORKS = [SocialNetwork(file.stem, os.path.join(PATH_TO_SOCIAL_NETWORKS, file.name)) for file in
                   pathlib.Path(path).glob(file_filter)]


def get_path_to_user_avatar(instance, filename):
    return f'images/users/user_{instance.user.id}/{filename}'


class PageTitleMixin:
    PageTitle = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'title': self.PageTitle})
        return context
