from django.conf.urls import patterns, include, url
from Tracks import views
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^upload_MP3/', views.upload_MP3, name='upload_MP3')
)
