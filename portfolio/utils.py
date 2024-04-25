import pathlib

SOCIAL_NETWORKS = ['facebook', 'twitter', 'instagram', 'linkedin', 'youtube']


def get_path_to_user_avatar(instance, filename):
    return f'images/users/user_{instance.user.id}/{filename}'

