from django import template
register = template.Library()


@register.filter(name='check_relationship_exists')
def check_relationship_exists(profile, user):
    user_id = int(user.id)  # get the user id
    return profile.relationships.filter(pk=user.profile.pk).exists()