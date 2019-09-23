from django.forms import ModelForm
from .models import *
from user.models import User
from django.conf import settings
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .widgets import XDSoftDateTimePickerInput
from django.forms import DateTimeInput
from .validators import validate_characters


class SignUpForm(UserCreationForm):
    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
    name = forms.CharField(label='Your name', validators=[validate_characters])

    class Meta:
        model = User
        fields = ('email', 'birth_date', 'name', 'password1', 'password2', )


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'country', 'city', 'province', 'birth_date']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)


class DateInput(forms.DateInput):
    input_type = 'date'


class EventForm(forms.ModelForm):
    start = forms.DateTimeField(
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control'},
            format='%Y-%m-%dT%H:%M')
    )
    end = forms.DateTimeField(
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control'},
            format='%Y-%m-%dT%H:%M')
    )

    venueName = forms.CharField(label='Venue Name', validators=[validate_characters])
    Adress1 = forms.CharField(label='Adress Line 1', validators=[validate_characters])
    Adress2 = forms.CharField(label='Adress Line 2', validators=[validate_characters])
    city = forms.CharField(validators=[validate_characters])
    province = forms.CharField(validators=[validate_characters])
    country = forms.CharField(validators=[validate_characters])
    class Meta:
        model = Event
        fields = ['name', 'description', 'url', 'picture',
                  'TicketPrice1', 'TicketPrice2', 'TicketPrice3', 'category']




class VenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = ['name', 'addressline1', 'addressline2',
                  'country', 'province', 'city']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'parent']
