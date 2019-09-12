from django.conf.urls import url
from django.urls import include, re_path, path
from .views import Login, AddCategory, AddEvent, Main, Results, FriendRequests, Notification, MessageView
from . import views

urlpatterns = [
    path('', Main.as_view(), name='start'),
    re_path(r'^main', Main.as_view(), name='main'),
    re_path(r'^login', Login.as_view(), name='login'),
    re_path(r'^logout',views.logout,name='logout'),
    re_path(r'^search',views.Search,name='search'),
    re_path(r'^results/$',Results.as_view(),name='results'),
    re_path(r'^signup', views.signup, name='Sign-UP'),
    re_path(r'^add-category', AddCategory.as_view(), name='add-category'),
    re_path(r'^create-event', AddEvent.as_view(), name='create-event'),
    re_path(r'^messages', views.message, name='message'),
    re_path(r'^friend', views.friend, name='friend'),
    re_path(r'^request/(?P<pk>\d+)/', views.sendrequest, name='send-request'),
    re_path(r'^accept/(?P<pk>\d+)/', views.acceptrequest, name='accept-request'),
    re_path(r'^allrequests', FriendRequests.as_view(), name='all-request'),
    re_path(r'^allnotifications', Notification.as_view(), name='all-notifications'),
    re_path(r'^markasread/(?P<pk>\d+)/', views.markasread, name='mark-read'),
    re_path(r'^markall', views.markallasread, name='mark-all'),
    re_path(r'^messageview', MessageView.as_view(), name='message-view'),
    re_path(r'^getmessages/(?P<pk>\d+)/', views.getmessages, name='get-messages'),
    re_path(r'^send', views.send, name='send-messages'),
    re_path(r'^notification', views.notification, name='notification')
]

