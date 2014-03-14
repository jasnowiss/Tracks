from django.conf.urls import patterns, include, url
from Tracks import views
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^$', views.index, name='index'),
    url(r'^$', views.tracks, name='tracks'),
    url(r'^upload_MP3', views.upload_MP3, name='upload_MP3'),
    url(r'^collaborate_helper', views.collaborate_helper, name='collaborate_helper'),
    url(r'^signin', views.signIn, name='SignIn'),
    url(r'^signup', views.signUp, name='SignUp'),
    url(r'^about.html', views.about, name='About'),
    url(r'^userpage/$',views.userpage, name='userpage'),
    url(r'^userpage/(?P<user_email>\w+)/$',views.userpage, name='userpage'),
    url(r'^userprofile/$', views.userprofile, name='userprofile'),
    url(r'^userprofile/(?P<user_email>\w+)/$', views.userprofile, name='userprofile')
)
