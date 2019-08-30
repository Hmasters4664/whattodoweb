from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from django.utils import timezone


class Group(models.Model):
    name = models.CharField(max_length=200)
    administrator = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now())

    class Meta:
        abstract = True
        ordering = ['-created_date']


class GroupMember(models.Model):
    group = models.ForeignKey(Group, null=True, blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        abstract = True


