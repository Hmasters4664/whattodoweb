from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from .validators import validate_characters, check_negative_number, check_zero_number
from django.utils import timezone

RELATIONSHIP_FOLLOWING = 1
RELATIONSHIP_BLOCKED = 2
RELATIONSHIP_STATUSES = (
    (RELATIONSHIP_FOLLOWING, 'Friends'),
    (RELATIONSHIP_BLOCKED, 'Blocked'),
)


class Event(models.Model):
    name = models.CharField(max_length=100, validators=[validate_characters],)
    description = models.TextField(validators=[validate_characters],)
    url = models.CharField(_('Ticket Purchase URL'), max_length=50, blank=True)
    imageUrl = models.CharField(max_length=50,)
    picture = models.ImageField(upload_to='images/', blank=True, null=True)
    dateCreated = models.DateField(auto_now_add=True)
    lastModified = models.DateField(auto_now_add=True)
    startDate = models.DateField(_('Start Date and Time'))
    endDate = models.DateField(_('End Date and Time'))
    TicketPrice1 = models.DecimalField(max_digits=19, decimal_places=2, default=200.00,
                                       validators=[check_negative_number],)
    TicketPrice2 = models.DecimalField(max_digits=19, decimal_places=2, default=200.00,
                                       validators=[check_negative_number], )
    TicketPrice3 = models.DecimalField(max_digits=19, decimal_places=2, default=200.00,
                                       validators=[check_negative_number], )
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.CASCADE)
    venue = models.OneToOneField('Venue', on_delete=models.CASCADE)


class Venue(models.Model):
    name = models.CharField(max_length=100, validators=[validate_characters],)
    addressline1 = models.CharField(max_length=100, validators=[validate_characters],)
    addressline2 = models.CharField(max_length=100, validators=[validate_characters],)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    country = models.CharField(max_length=50, validators=[validate_characters],)
    province = models.CharField(_('provice/state'), max_length=50, validators=[validate_characters],)
    city = models.CharField(max_length=100, validators=[validate_characters],)




class Organiser(models.Model):
    name = models.CharField(max_length=100, validators=[validate_characters], )
    phone = models.CharField(max_length=12, validators=[validate_characters], )
    facebookurl = models.CharField(max_length=50,)
    twitterhandle = models.CharField(max_length=50,)


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('slug', 'parent',)
        verbose_name_plural = "categories"

    def __str__(self):
        full_path = [self.name]

        k = self.parent


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    name = models.TextField(max_length=50, blank=True)
    country = models.CharField(max_length=30, blank=True)
    city = models.CharField(max_length=30, blank=True)
    province = models.CharField(_('provice/state'),max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    relationships = models.ManyToManyField('self', through='Relationship',
                                           symmetrical=False,)

    def __unicode__(self):
        return self.name


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


def add_relationship(self, person, status, symm=True):
    relationship, created = Relationship.objects.get_or_create(
        from_person=self,
        to_person=person,
        status=status)
    if symm:
        # avoid recursion by passing `symm=False`
        person.add_relationship(self, status, False)
    return relationship


def remove_relationship(self, person, status, symm=True):
    Relationship.objects.filter(
        from_person=self,
        to_person=person,
        status=status).delete()
    if symm:
        # avoid recursion by passing `symm=False`
        person.remove_relationship(self, status, False)


def get_relationships(self, status):
    return self.relationships.filter(
        to_people__status=status,
        to_people__from_person=self)


class Relationship(models.Model):
    from_person = models.ForeignKey(Profile, related_name='from_people', on_delete=models.CASCADE)
    to_person = models.ForeignKey(Profile, related_name='to_people', on_delete=models.CASCADE)
    status = models.IntegerField(choices=RELATIONSHIP_STATUSES)












