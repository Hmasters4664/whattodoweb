from django import template
register = template.Library()


@register.filter(name='check_relationship_exists')
def check_relationship_exists(profile, user):
    return profile.relationships.filter(pk=user.profile.pk).exists()

