from django.conf.urls import url
from django.urls import include, re_path, path
from .views import Login
from . import views

urlpatterns = [
    re_path(r'^login', Login.as_view(), name='login'),
    re_path(r'^signup', views.signup, name='Sign-UP'),
]