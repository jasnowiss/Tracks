from django.conf.urls import patterns, include, url
from Tracks import views
from django.conf import settings
from django.conf.urls.static import static
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^(?i)$', views.tracks, name='tracks'),
    url(r'^(?i)upload_MP3/?$', views.upload_MP3, name='upload_MP3'),
    url(r'^(?i)get_tracks_for_current_user_JSON', views.get_tracks_for_current_user_JSON, name='get_tracks_for_current_user_JSON'),
    url(r'^(?i)get_collab_settings_JSON/$', views.get_collab_settings_JSON, name='get_collab_settings_JSON'),
    url(r'^(?i)get_update_collab_JSON/$', views.get_update_collab_JSON, name='get_update_collab_JSON'),
    url(r'^(?i)finalize_collaboration', views.finalize_collaboration, name='finalize_collaboration'),
    url(r'^(?i)userprofile/$',views.userprofile, name='userprofile'),
    url(r'^(?i)userprofile/(?P<user_id>\d+)/$', views.userprofile, name='userprofile'),
    url(r'^(?i)userpage/$',views.userpage, name='userpage'),
    url(r'^(?i)userpage/(?P<user_id>\d+)/$',views.userpage, name='userpage'),
    url(r'^(?i)signin/?$', views.signIn, name='SignIn'),
    url(r'^(?i)about.html/?$', views.about, name='About'),
    url(r'^(?i)register/?$', views.register, name='register'),
    url(r'^(?i)logout/?$', views.logout_view, name='Logout'),
    url(r'^(?i)downbeat/?$', views.downbeat, name='Downbeat'),
    url(r'^(?i)search/?$', views.search, name='search'),
    url(r'^(?i)record/?$', views.record, name='record'),
    url(r'^(?i)handleRecord/?$', views.handleRecord, name='handleRecord'),
    url(r'^(?i)delete_track_from_server', views.delete_track_from_server, name='delete_track_from_server'),
    url(r'^(?i)change_permission_of_collab', views.change_permission_of_collab, name='change_permission_of_collab'),
    url(r'^(?i)add_user_to_collab', views.add_user_to_collab, name='add_user_to_collab'),
    url(r'^(?i)remove_user_from_collab', views.remove_user_from_collab, name='remove_user_from_collab'),
    url(r'^(?i)editTrack/$', views.editTrack, name='editTrack'),
    url(r'^(?i)editTrack/(?P<track_id>\d+)/$', views.editTrack, name='editTrack'),
    url(r'^(?i)edit/$', views.edit, name='edit'),
    url(r'^(?i)edit/(?P<collaboration_id>\d+)/$', views.edit, name='edit'),
    url(r'^(?i)edit/(?P<collaboration_id>\d+)/change_name/$', views.change_name, name='change_name'),
    url(r'^(?i)edit/(?P<collaboration_id>\d+)/handleRecord$', views.handleRecordFromEdit, name="handleRecordFromEdit"),
    url(r'^(?i)get_JSON_for_search/?$', views.get_JSON_for_search, name="get_JSON_for_search"),
    # url(r'^$', views.index, name='index'),
    #url(r'^$', views.tracks, name='tracks'),
    #url(r'^upload_MP3', views.upload_MP3, name='upload_MP3'),
    #url(r'^signin', views.signIn, name='SignIn'),
    #url(r'^signup', views.signUp, name='SignUp'),
    #url(r'^about.html', views.about, name='About'),
    #url(r'(?i)^upload/?$',views.index, name='index'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^user_mp3_files/(?P<path>.*)$', views.play_MP3),
        url(r'^resetFixture/$', views.resetFixture),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
   )
