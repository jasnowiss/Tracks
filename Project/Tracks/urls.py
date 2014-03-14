from django.conf.urls import patterns, include, url
from Tracks import views
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^$', views.index, name='index'),

    #url(r'^$', views.tracks, name='tracks'),
    #url(r'^upload_MP3', views.upload_MP3, name='upload_MP3'),
    url(r'^get_tracks_for_current_user_JSON', views.get_tracks_for_current_user_JSON, name='get_tracks_for_current_user_JSON'),
    url(r'^finalize_collaboration', views.finalize_collaboration, name='finalize_collaboration'),
    #url(r'^signin', views.signIn, name='SignIn'),
    #url(r'^signup', views.signUp, name='SignUp'),
    #url(r'^about.html', views.about, name='About'),
    url(r'^userpage/$',views.userpage, name='userpage'),
    url(r'^userpage/(?P<user_email>\w+)/$',views.userpage, name='userpage'),
    url(r'^userprofile/$', views.userprofile, name='userprofile'),
    url(r'^userprofile/(?P<user_email>\w+)/$', views.userprofile, name='userprofile'),

    url(r'(?i)^$', views.tracks, name='tracks'),
    #url(r'(?i)^upload/?$',views.index, name='index'),
    url(r'(?i)^upload_MP3/?$', views.upload_MP3, name='upload_MP3'),
    url(r'(?i)^signin/?$', views.signIn, name='SignIn'),
    url(r'(?i)^about.html$', views.about, name='About'),
    url(r'(?i)^register/?$', views.register, name='Register'),
    url(r'(?i)^logout/?$', views.logout, name='Logout'),
    url(r'(?i)^downbeat/?$', views.downbeat, name='Downbeat'),

)
