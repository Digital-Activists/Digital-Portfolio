import pathlib

SOCIAL_NETWORKS = ['facebook', 'twitter', 'instagram', 'linkedin', 'youtube']
MONTHS = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь',
          'Декабрь']
MONTHS = ((i, month) for (i, month) in enumerate(MONTHS))


def get_path_to_user_avatar(instance, filename):
    return f'images/users/user_{instance.user.id}/{filename}'


class PageTitleMixin():
    PageTitle = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'title': self.PageTitle})
        return context