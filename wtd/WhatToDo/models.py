import sys

from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from .validators import validate_characters, check_negative_number, check_zero_number
from django.utils import timezone
from autoslug import AutoSlugField
from django.shortcuts import get_list_or_404, get_object_or_404
from django.utils import timezone
from django.db import models
from django.conf import settings
import uuid
from django.template.defaultfilters import slugify
from sorl.thumbnail import ImageField, get_thumbnail
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from io import StringIO, BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import os

RELATIONSHIP_FOLLOWING = 0
RELATIONSHIP_REQUESTED = 1
RELATIONSHIP_BLOCKED = 2
RELATIONSHIP_STATUSES = (
    (RELATIONSHIP_FOLLOWING, 'Friends'),
    (RELATIONSHIP_REQUESTED, 'Request'),
    (RELATIONSHIP_BLOCKED, 'Blocked'),
)

PUBLIC = 1
PRIVATE = 0
EVENT_TYPE = (
    (PUBLIC, 'Public'),
    (PRIVATE, 'Private'),

)

GENERAL = 1
FRIEND = 0
NOTIFICATION_TYPE = (
    (GENERAL, 'General'),
    (FRIEND, 'Friend'),
)


class Event(models.Model):
    name = models.CharField(max_length=100, validators=[validate_characters], )
    description = models.TextField(validators=[validate_characters], )
    url = models.CharField(_('Ticket Purchase URL'), max_length=50, blank=True)
    picture = models.ImageField(upload_to='events', blank=True, null=True, default='default_events.jpg')
    dateCreated = models.DateTimeField(auto_now_add=True)
    lastModified = models.DateTimeField(auto_now_add=True)
    startDate = models.DateTimeField(_('Start Date and Time'))
    endDate = models.DateTimeField(_('End Date and Time'), )
    TicketPrice1 = models.DecimalField(_('Lowest Ticket Price'), max_digits=19, decimal_places=2, default=000.00,
                                       validators=[check_negative_number], )
    TicketPrice2 = models.DecimalField(_('Middle Ticket Price'), max_digits=19, decimal_places=2, default=000.00,
                                       validators=[check_negative_number], )
    TicketPrice3 = models.DecimalField(_('Highest Ticket Price'), max_digits=19, decimal_places=2, default=000.00,
                                       validators=[check_negative_number], )
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.CASCADE)
    interest = models.ManyToManyField('Profile', blank=True, related_name='post_interest')

    venue = models.ForeignKey('Venue', on_delete=models.CASCADE, blank=True, null=True)
    slug = models.SlugField(blank=True, unique=True)

    class Meta:
        ordering = ['-id']

    def save(self, **kwargs):
        if not self.name:
            self.name = "Unkown"

        slug_str = "%s %s %s" % (self.name, uuid.uuid4(), self.category)
        self.slug = slugify(slug_str)

        super(Event, self).save(**kwargs)


class Venue(models.Model):
    name = models.CharField(max_length=100, validators=[validate_characters], )
    addressline1 = models.CharField(max_length=100, validators=[validate_characters], )
    addressline2 = models.CharField(max_length=100, validators=[validate_characters], )
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    country = models.CharField(max_length=50, validators=[validate_characters], )
    province = models.CharField(_('provice/state'), max_length=50, validators=[validate_characters], )
    city = models.CharField(max_length=100, validators=[validate_characters], )

    class Meta:
        ordering = ['-id']


class Organiser(models.Model):
    name = models.CharField(max_length=100, validators=[validate_characters], )
    phone = models.CharField(max_length=12, validators=[validate_characters], )
    facebookurl = models.CharField(max_length=50, )
    twitterhandle = models.CharField(max_length=50, )

    class Meta:
        ordering = ['-id']


class Category(models.Model):
    name = models.CharField(max_length=50, validators=[validate_characters], )
    slug = AutoSlugField(populate_from='name')
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('slug', 'parent',)
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True, validators=[validate_characters], )
    name = models.TextField(max_length=50, blank=False, validators=[validate_characters], )
    country = models.CharField(max_length=30, blank=True, validators=[validate_characters], )
    profile_picture = models.ImageField(upload_to='profile', blank=True, null=True, default='profile/avatar.jpg')
    profile_small = models.ImageField(upload_to='profile', blank=True, null=True, )
    profile_medium = models.ImageField(upload_to='profile', blank=True, null=True, )
    city = models.CharField(max_length=30, blank=True, validators=[validate_characters], )
    province = models.CharField(_('provice/state'), max_length=30, blank=True, validators=[validate_characters], )
    birth_date = models.DateField(null=True, blank=True, )
    relationships = models.ManyToManyField('self', through='Relationship',
                                           symmetrical=False, related_name='related_to')
    slug = models.SlugField(blank=True, unique=True)

    class Meta:
        ordering = ['-id']

    def save(self, **kwargs):
        if not self.name:
            self.name = "Unkown"

        slug_str = "%s %s" % (self.name, uuid.uuid4())
        self.slug = slugify(slug_str)
        if self.profile_picture and not self.profile_small:
            image = Image.open(self.profile_picture)
            image.thumbnail((54, 54), Image.ANTIALIAS)
            output = BytesIO()
            image.save(output, format='JPEG', quality=85)
            output.seek(0)
            name = "%s %s" % (self.name, uuid.uuid4())
            name += "-54.jpg"
            self.profile_small = InMemoryUploadedFile(output, 'ImageField', name,
                                                      'image/jpeg',
                                                      sys.getsizeof(output), None)
            image = Image.open(self.profile_picture)
            image.thumbnail((160, 155), Image.ANTIALIAS)
            output = BytesIO()
            image.save(output, format='JPEG', quality=85)
            output.seek(0)
            name = "%s %s" % (self.name, uuid.uuid4())
            name += "-160.jpg"
            self.profile_medium = InMemoryUploadedFile(output, 'ImageField', name,
                                                      'image/jpeg',
                                                      sys.getsizeof(output), None)
        super(Profile, self).save(**kwargs)

    def __unicode__(self):
        return self.name

    def add_relationship(self, person, status, uuids=uuid.uuid4(), symm=True):

        relationship, created = Relationship.objects.get_or_create(
            from_person=self,
            to_person=person,
            status=status,
            uuid=uuids)
        if symm:
            # avoid recursion by passing `symm=False`
            person.add_relationship(self, status, uuids, False)
        return relationship

    def friend_relationship(self, person, symm=True):
        try:
            relationship = Relationship.objects.get(from_person=self, to_person=person)
        except Relationship.DoesNotExist:
            relationship = None

        if relationship:
            relationship.status = 0
            relationship.save()
        if symm:
            # avoid recursion by passing `symm=False`
            person.friend_relationship(self, False)
        return relationship

    def block_relationship(self, person, status, symm=True):
        try:
            relationship = Relationship.objects.get(from_person=self, to_person=person)
        except Relationship.DoesNotExist:
            relationship = None

        if relationship:
            relationship.status = 2
        if symm:
            # avoid recursion by passing `symm=False`
            person.block_relationship(self, status, False)
        return relationship

    def get_relationships(self, status):
        return self.relationships.filter(
            to_people__status=status,
            to_people__from_person=self)

    def count_relationships(self, status):
        return self.relationships.filter(
            to_people__status=status,
            to_people__from_person=self).count()

    def remove_relationship(self, person, status, symm=True):
        Relationship.objects.filter(
            from_person=self,
            to_person=person,
            status=status).delete()
        if symm:
            # avoid recursion by passing `symm=False`
            person.remove_relationship(self, status, False)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    # instance.profile.full_clean()
    instance.profile.save()


class Relationship(models.Model):
    from_person = models.ForeignKey(Profile, related_name='from_people', on_delete=models.CASCADE)
    to_person = models.ForeignKey(Profile, related_name='to_people', on_delete=models.CASCADE)
    status = models.IntegerField(choices=RELATIONSHIP_STATUSES, default=1)
    uuid = models.UUIDField(editable=False)

    class Meta:
        ordering = ['-id']


class Like(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']


class EventCommentQuerySet(models.query.QuerySet):

    def get_comments(self, event):
        return self.filter(event=event)

    def count_comments(self, event_id):
        return self.filter(pk=event_id).count()


class Messages(models.Model):
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sender')
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recipient')
    text = models.CharField(max_length=150)
    opened = models.BooleanField(_('opened'), default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']


class Notifications(models.Model):
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='actioner')
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='receiver')
    notification_type = models.IntegerField(choices=NOTIFICATION_TYPE, default=1)
    action = models.CharField(max_length=150)
    read = models.BooleanField(_('read'), default=False)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created']


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author')
    content = models.CharField(max_length=300)
    picture = models.ImageField(upload_to='posts', blank=True, null=True)
    dateCreated = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField('Profile', blank=True, related_name='user_likes')
    public = models.BooleanField(_('Is Public'), default=False)


class Schedule(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='creator')
    title = models.CharField(max_length=200, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    notes = models.TextField(u'Textual Notes', help_text=u'Textual Notes', blank=True, null=True)

    class Meta:
        verbose_name = u'Scheduling'
        verbose_name_plural = u'Scheduling'

    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError('Ending times must be after starting times')


class Comment(models.Model):
    post = models.ForeignKey('WhatToDo.Event', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    authname = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='authorname')
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=True)

    def approve(self):
        self.approved_comment = True
        self.save()

    def disapprove(self):
        self.approved_comment = False
        self.save()

    def __str__(self):
        return self.text
