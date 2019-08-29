from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .widgets import XDSoftDateTimePickerInput
from django.forms import DateTimeInput


class SignUpForm(UserCreationForm):
    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
    name = forms.CharField(label='Your name')

    class Meta:
        model = User
        fields = ('username', 'birth_date', 'name', 'password1', 'password2', )


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'country', 'city', 'province', 'birth_date']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


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
