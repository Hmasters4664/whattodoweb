from django.contrib.auth.models import User
from django.shortcuts import render

from django.shortcuts import render_to_response, get_object_or_404
from django.utils.http import is_safe_url
import csv
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from .models import Event, Venue, Organiser, Category, Profile, Notifications, Messages, RELATIONSHIP_REQUESTED, \
    RELATIONSHIP_FOLLOWING, Relationship
from django.views.generic import CreateView
from django.views.generic.edit import FormView
from django.views.generic.base import View, TemplateView
from django.core import serializers
import json
from .forms import EventForm, ProfileForm, UserForm, VenueForm
from django.views.generic.list import ListView
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.db.models import Q
from django.contrib import messages
import xlwt
import xlrd
from tablib import Dataset
import magic
from django.core.files.storage import default_storage
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import SignUpForm, CategoryForm
from django.db.models import Q
import json
from datetime import datetime
from django.core.serializers import serialize
from django.forms.models import model_to_dict
from django.utils import timezone


class Main(LoginRequiredMixin, ListView):
    model = Event
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'main.html'
    context_object_name = 'events'
    Event.objects.all()


@login_required
def notification(request):
    notifications = Notifications.objects.filter(to_user=request.user, notification_type=1, read=False) \
        .values('action', 'created', 'from_user__profile__profile_picture')
    jayson = list(notifications)
    return JsonResponse(jayson, safe=False)


@login_required
def friend(request):
    friends = Notifications.objects.filter(to_user=request.user, notification_type=0, read=False) \
        .values('action', 'created', 'from_user__profile__profile_picture')
    jayson = list(friends)
    return JsonResponse(jayson, safe=False)


@login_required
def message(request):
    mess = Messages.objects.filter(to_user=request.user, opened=False) \
        .values('from_user__profile__name', 'created', 'text')
    jayson = list(mess)
    return JsonResponse(jayson, safe=False)


class Login(FormView):
    template_name = 'login.html'
    success_url = '/main/'
    form_class = AuthenticationForm
    redirect_field_name = REDIRECT_FIELD_NAME

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        # Sets a test cookie to make sure the user has cookies enabled
        request.session.set_test_cookie()

        return super(Login, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        auth_login(self.request, form.get_user())

        # If the test cookie worked, go ahead and
        # delete it since its no longer needed
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()

        return super(Login, self).form_valid(form)

    def get_success_url(self):
        redirect_to = self.request.GET.get(self.redirect_field_name)
        if not is_safe_url(url=redirect_to, allowed_hosts=self.request.get_host()):
            redirect_to = self.success_url
        return redirect_to


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.profile.name = form.cleaned_data.get('name')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


class AddCategory(LoginRequiredMixin, FormView):
    model = Category
    template_name = 'forms.html'
    success_url = '/main/'
    login_url = '/login/'
    form_class = CategoryForm
    redirect_field_name = 'redirect_to'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class AddEvent(LoginRequiredMixin, FormView):
    model = Event
    template_name = 'forms.html'
    success_url = '/main/'
    login_url = '/login/'
    form_class = EventForm
    redirect_field_name = 'redirect_to'

    def form_valid(self, form):
        event = form.save(commit=False)
        event.startDate = form.cleaned_data.get('start')
        event.endDate = form.cleaned_data.get('end')

        event.save()
        return super().form_valid(form)


@login_required
def logout(request):
    success_url = '/login/'
    redirect_field_name = REDIRECT_FIELD_NAME
    auth_logout(request)

    return redirect(success_url)


@login_required
def Search(request):
    object_list = Profile.objects.filter(name__startswith=request.GET.get('search')).values("name", "profile_picture",
                                                                                            "city", "country")
    jason = list(object_list)
    # print(jason)
    return JsonResponse(jason, safe=False)


class Results(LoginRequiredMixin, ListView):
    model = Profile
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'searchpage.html'

    # paginate_by = 10

    def get_context_data(self, *, assets=None, **kwargs):
        context = super(Results, self).get_context_data()
        context['profiles'] = Profile.objects.filter(name__startswith=self.request.GET.get('item')) \
            .exclude(user=self.request.user)
        return context


@login_required
def sendrequest(request, pk):
    to_user = get_object_or_404(Profile, pk=pk)
    if not to_user.relationships.filter(pk=request.user.profile.pk).exists():
        request.user.profile.add_relationship(to_user, 1)
        messages.info(request, 'Request Sent to ' + to_user.name)
        rmessage = Notifications(from_user=request.user, to_user=to_user.user,
                                 notification_type=0, action=request.user.profile.name + " sent you a friend request ")
        rmessage.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        messages.info(request, 'Relationship already exists with ' + to_user.name)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def acceptrequest(request, pk):
    pg = int(pk)
    from_user = get_object_or_404(Profile, pk=pg)
    try:
        relationship = Relationship.objects.get(from_person=request.user.profile, to_person=from_user, status=1)
    except Relationship.DoesNotExist:
        relationship = None

    if relationship:
        request.user.profile.friend_relationship(from_user)

        rmessage = Notifications(from_user=request.user, to_user=from_user.user,
                                 notification_type=1,
                                 action=request.user.profile.name + " accepted your friend request ")
        rmessage.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class FriendRequests(LoginRequiredMixin, ListView):
    model = Profile
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'friendrequestpage.html'
    paginate_by = 5

    def get_context_data(self, *, assets=None, **kwargs):
        friends = Notifications.objects.filter(to_user=self.request.user, notification_type=0, read=False)
        friends.update(read=True)
        context = super(FriendRequests, self).get_context_data()
        context['notifications'] = self.request.user.profile.get_relationships(1) \
            .exclude(id=self.request.user.profile.id).distinct()
        return context


class Notification(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = Notifications
    redirect_field_name = 'redirect_to'
    template_name = 'notifications.html'
    paginate_by = 5

    def get_context_data(self, *, assets=None, **kwargs):
        noti = Notifications.objects.filter(to_user=self.request.user, notification_type=1, read=False)
        context = super(Notification, self).get_context_data()
        context['notifications'] = noti.values('id', 'action', 'created', 'from_user__profile__profile_picture')
        return context


@login_required
def markasread(request, pk):
    pg = int(pk)
    noti = get_object_or_404(Notifications, pk=pg)
    if noti.to_user == request.user:
        noti.read = True
        noti.save()

    return redirect('all-notifications')


@login_required
def markallasread(request):
    noti = Notifications.objects.filter(to_user=request.user, notification_type=1, read=True)
    noti.update(read=True)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class MessageView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = Profile
    redirect_field_name = 'redirect_to'
    template_name = 'messages.html'

    def get_context_data(self, *, assets=None, **kwargs):
        context = super(MessageView, self).get_context_data()
        context['friends'] = self.request.user.profile.get_relationships(0)
        return context


@login_required
def getmessages(request, pk):
    from_user = get_object_or_404(Profile, pk=pk)
    try:
        relationship = Relationship.objects.get(from_person=request.user.profile, to_person=from_user, status=0)
    except Relationship.DoesNotExist:
        relationship = None

    if relationship:
        mess = Messages.objects.filter(Q(to_user=request.user, opened=False, from_user=from_user.user) |
                                       Q(to_user=from_user.user, opened=False, from_user=request.user)) \
            .order_by('created')

        return render(request, 'chatpage.html', {'friend': from_user, 'messages': mess})

    else:
        return redirect('message-view')


def send(request):
    pk = request.POST.get('id')
    time = float(request.POST.get('time'))
    #print(type(time))
    t=datetime.fromtimestamp(time)
    mess = request.POST.get('message')
    to_user = get_object_or_404(User, pk=pk)
    b = timezone.now()
    rec = Messages(from_user=request.user, to_user=to_user, text=mess, created=t)
    rec.save()
    dict_obj = []
    serialized_obj = json.dumps(dict_obj)
    #print(serialized_obj)
    return JsonResponse(serialized_obj, safe=False)
