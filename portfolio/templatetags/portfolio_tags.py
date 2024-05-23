from django import template

register = template.Library()


@register.simple_tag
def is_liked(post, user):
    return post.is_liked_post(user)


@register.simple_tag
def dict_key_lookup(the_dict, key):
    return the_dict.get(key)
