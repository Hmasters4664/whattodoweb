from django.conf.urls import url
from django.urls import include, re_path, path
from .views import Login, Main, AddCategory, AddEvent
from . import views

urlpatterns = [
    path('', Main.as_view(), name='start'),
    re_path(r'^main', Main.as_view(), name='main'),
    re_path(r'^login', Login.as_view(), name='login'),
    re_path(r'^signup', views.signup, name='Sign-UP'),
    re_path(r'^add-category', AddCategory.as_view(), name='add-category'),
    re_path(r'^create-event', AddEvent.as_view(), name='create-event'),
]