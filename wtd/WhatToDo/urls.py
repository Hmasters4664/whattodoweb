from django.conf.urls import url
from django.urls import include, re_path, path
from .views import Login, AddCategory, AddEvent, Main, Results, FriendRequests, Notification, MessageView, \
    UpdateProfile, AddPost, ViewProfile, CalendarView, PostView, EventDetailView
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
    re_path(r'^updateprofile/(?P<slug>[\w-]+)/$', UpdateProfile.as_view(), name='modify-profile'),
    re_path(r'^profile/(?P<slug>[\w-]+)/$', ViewProfile.as_view(), name='view-profile'),
    re_path(r'^like/', views.like, name='like-event'),
    re_path(r'^postlike/', views.likepost, name='like-post'),
    re_path(r'^addPost/', AddPost.as_view(), name='add-post'),
    re_path(r'^eventsearch/$',views.event_search,name='event-search'),
    re_path(r'^eventselect/$',views.event_select,name='event-select'),
    re_path(r'^messages', views.message, name='message'),
    re_path(r'^addSchedule/(?P<pk>\d+)/', views.addtoschedule, name='schedule-add'),
    re_path(r'^calender/', CalendarView.as_view(), name='calender'),
    re_path(r'^posts/', PostView.as_view(), name='posts'),
    re_path(r'^eventdetail/(?P<slug>[\w-]+)/$', EventDetailView.as_view(), name='event-detail'),
    re_path(r'^notification-count', views.notification_count, name='notification-count'),
    re_path(r'^Friends-count', views.friend_count, name='friend-count'),
    re_path(r'^message-count', views.message_count, name='message-count'),
    re_path(r'^notification', views.notification, name='notification')
]

