from django.db import models
from .validators import validate_characters, check_negative_number, check_zero_number


class Events(models.Model):
    name = models.CharField(max_length=100, validators=[validate_characters],)
    description = models.TextField(validators=[validate_characters],)
    url = models.CharField(max_length=50,)
    imageUrl = models.CharField(max_length=50,)
    dateCreated = models.DateField()
    lastModified = models.DateField()
    startDate = models.DateField()
    endDate = models.DateField()
    ticketprice1 = models.DecimalField(max_digits=19, decimal_places=2,default=00.00,validators = [check_negative_number],)
    ticketprice2 = models.DecimalField(max_digits=19, decimal_places=2, default=00.00,
                                       validators=[check_negative_number], )
    ticketprice3 = models.DecimalField(max_digits=19, decimal_places=2, default=00.00,
                                       validators=[check_negative_number], )
    venue = models.ForeignKey('Venue', on_delete=models.CASCADE)


class Venues(models.Model):
    name = models.CharField(max_length=100, validators=[validate_characters],)
    addressline1 = models.CharField(max_length=100, validators=[validate_characters],)
    addressline2 = models.CharField(max_length=100, validators=[validate_characters],)
    latitude = models.DecimalField()
    longitude = models.DecimalField()
    country = models.CharField(max_length=50, validators=[validate_characters],)
    province = models.CharField(max_length=50, validators=[validate_characters],)
    city = models.CharField(max_length=100, validators=[validate_characters],)


class Organisers(models.Model):
    name = models.CharField(max_length=100, validators=[validate_characters], )
    phone = models.CharField(max_length=12, validators=[validate_characters], )
    facebookurl = models.CharField(max_length=50,)
    twitterhandle = models.CharField(max_length=50,)


class Categories(models.Model):
    name = models.CharField(max_length=100, validators=[validate_characters], )














