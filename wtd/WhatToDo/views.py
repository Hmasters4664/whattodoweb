# from django.contrib.auth.models import User
from django.shortcuts import render

from django.shortcuts import render_to_response, get_object_or_404
from django.utils.http import is_safe_url
import csv
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.utils.safestring import mark_safe

from user.models import User
from .models import Event, Venue, Organiser, Category, Profile, Notifications, Messages, RELATIONSHIP_REQUESTED, \
    RELATIONSHIP_FOLLOWING, Relationship, Post, Schedule
from django.views.generic import CreateView
from django.views.generic.edit import FormView
from django.views.generic.base import View, TemplateView
from django.core import serializers
import json
from .forms import EventForm, ProfileForm, UserForm, VenueForm, PostForm
from django.views.generic.list import ListView
from django.views.generic import UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime, date, timedelta
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
from .validators import validate_characters
import firebase_admin
from firebase_admin import credentials, firestore
from django.db.models import Count
from .calender import Calendar
import calendar
from bootstrap_modal_forms.generic import BSModalCreateView,BSModalReadView
from django.urls import reverse_lazy

cred = credentials.Certificate("secrets.json")
firebase_admin.initialize_app(cred)


class Main(LoginRequiredMixin, ListView):
    model = Event
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'main.html'

    def get_context_data(self, *, assets=None, **kwargs):
        d = Event.objects.all()
        context = super(Main, self).get_context_data()
        context['events'] = d
        context['uevents'] = d.order_by('-startDate')[:5]
        context['tops'] = d.annotate(l_count=Count('interest')).order_by('-l_count')[:5]
        context['schedules'] = Schedule.objects.filter(creator=self.request.user).order_by('start_time')[:5]
        context['categories'] = Category.objects.filter(parent__isnull=True)
        context['cities'] = Venue.objects.values('city').distinct()
        return context

@login_required
def event_search(request):
    var1 = request.POST.get('item', '')
    d = Event.objects.filter(name__startswith=var1)

    print(d)
    return render(request, 'temp.html', {'events': d})

@login_required
def event_select(request):
    var1 = request.POST.get('city', '')
    var2 = request.POST.get('category', '')
    d = Event.objects.filter(venue__city__startswith=var1, category__name__startswith=var2)

    print(d)
    return render(request, 'temp.html', {'events': d})


@login_required
def notification_count(request):
    count = Notifications.objects.filter(to_user=request.user, notification_type=1, read=False).count()

    return JsonResponse(count, safe=False)

@login_required
def friend_count(request):
    count = Notifications.objects.filter(to_user=request.user, notification_type=0, read=False).count()
    return JsonResponse(count, safe=False)


@login_required
def message_count(request):
    count = Messages.objects.filter(to_user=request.user, opened=False).count()
    return JsonResponse(count, safe=False)


@login_required
def notification(request):
    notifications = Notifications.objects.filter(to_user=request.user, notification_type=1, read=False)

    return render(request,'generalnotifications.html', {'notifications': notifications})


@login_required
def friend(request):
    notifications = Notifications.objects.filter(to_user=request.user, notification_type=0, read=False)
    return render(request,'friendnotifications.html', {'notifications': notifications})


@login_required
def message(request):
    mess = Messages.objects.filter(to_user=request.user, opened=False)
    return render(request,'messagenotifications.html', {'messages': mess})


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
            user = authenticate(username=user.email, password=raw_password)
            login(request, user)
            return redirect('main')
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


class UpdateProfile(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'forms.html'
    success_url = '/main/'
    login_url = '/login/'
    form_class = ProfileForm
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
        ven = Venue(name=form.cleaned_data.get('venueName'), addressline1=form.cleaned_data.get('Adress1'),
                    addressline2=form.cleaned_data.get('Adress2'), city=form.cleaned_data.get('city'),
                    province=form.cleaned_data.get('province'), country=form.cleaned_data.get('country'), )
        ven.save()
        event = form.save(commit=False)
        event.startDate = form.cleaned_data.get('start')
        event.endDate = form.cleaned_data.get('end')
        event.venue = ven
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
        context['notifications'] = noti
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
        mess= Messages.objects.filter(to_user=request.user, from_user=from_user.user, opened=False)
        mess.update(opened=True)
        return render(request, 'chatpage.html', {'friend': from_user, 'chatkey': relationship.uuid})

    else:
        return redirect('message-view')


def send(request):
    pk = request.POST.get('id')
    time = float(request.POST.get('time'))
    # print(type(time))
    t = datetime.fromtimestamp(time)
    mess = request.POST.get('message')
    to_user = get_object_or_404(User, pk=pk)
    b = timezone.now()
    rec = Messages(from_user=request.user, to_user=to_user, text=mess, created=t)
    mess = Messages.objects.filter(to_user=request.user, opened=False, from_user=to_user)
    mess.update(opened=True)
    db = firestore.client()
    rec.save()
    dict_obj = []
    serialized_obj = json.dumps(dict_obj)
    # print(serialized_obj)
    return JsonResponse(serialized_obj, safe=False)


@login_required
def like(request):
    id = request.POST.get('key')
    event = get_object_or_404(Event, pk=id)
    if request.user.profile in event.interest.all():
        event.interest.remove(request.user.profile)
        dict_obj = {'itemz': 'ion-android-favorite-outline', 'counter': event.interest.count()}
        serialized_obj = json.dumps(dict_obj)
        print(serialized_obj)

    else:
        event.interest.add(request.user.profile)
        dict_obj = {'itemz': 'ion-android-favorite', 'counter': event.interest.count()}
        serialized_obj = json.dumps(dict_obj)
        print(serialized_obj)

    return JsonResponse(serialized_obj, safe=False)

#class PublisherDetail(DetailView):


@login_required
def likepost(request):
    id = request.POST.get('key')
    post = get_object_or_404(Post, pk=id)
    if request.user.profile in post.likes.all():
        post.likes.remove(request.user.profile)
        dict_obj = {'itemz': 'ion-android-favorite-outline', 'counter': post.likes.count()}
        serialized_obj = json.dumps(dict_obj)
        print(serialized_obj)

    else:
        post.likes.add(request.user.profile)
        dict_obj = {'itemz': 'ion-android-favorite', 'counter': post.likes.count()}
        serialized_obj = json.dumps(dict_obj)
        print(serialized_obj)

    return JsonResponse(serialized_obj, safe=False)


class AddPost(LoginRequiredMixin, FormView):
    model = Post
    template_name = 'Post_Form.html'
    success_url = '/main/'
    login_url = '/login/'
    form_class = PostForm
    redirect_field_name = 'redirect_to'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.picture = self.request.FILES['myfile']
        post.author = self.request.user
        post.save()
        return super().form_valid(form)


class ViewProfile(LoginRequiredMixin, ListView):
    model = Post
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'true_profile.html'

    def get_context_data(self, *, assets=None, **kwargs):
        context = super(ViewProfile, self).get_context_data()
        context['posts'] = Post.objects.filter(author=self.request.user)
        context['count'] = Post.objects.filter(author=self.request.user).count()
        context['fcount'] = self.request.user.profile.count_relationships(0)
        return context


class CalendarView(ListView):
    model = Event
    template_name = 'calander.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = get_date(self.request.GET.get('month', None))
        #print(d)
        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month, self.request.user)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        #print(mark_safe(html_cal))
        #print(prev_month(d))
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        context['calandar'] = mark_safe(html_cal)
        return context


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

@login_required
def addtoschedule(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if event:
        schedule = Schedule(creator=request.user, title=event.name, start_time=event.startDate, end_time=event.endDate)
        schedule.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class PostView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'userpost.html'

    def get_context_data(self, **kwargs):
        context = super(PostView, self).get_context_data()
        relatioships = self.request.user.profile.get_relationships(0)
        context['posts'] = Post.objects.filter(Q(author__profile__in=relatioships) | Q(author=self.request.user))
        context['friends'] = relatioships
        return context


class EventDetailView(BSModalReadView):
    model = Event

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context