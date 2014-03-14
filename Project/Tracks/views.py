# Create your views here.
from django import forms
from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, Http404, HttpResponseForbidden, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.utils import timezone
# from TracksApp_forms import *
from Tracks.forms import *
from Tracks.forms import UploadFileForm
from Tracks.models import *
from Tracks.models import TracksUser
from Tracks.models import Track
import os
import sys
import traceback


##def index(request):
##    form = UploadFileForm()
##    return render(request, 'Tracks/index.html', {'form': form})


def register(request):
    """Register a user."""
    pass


""" # Julian's version, undo when ready
def signIn(request):
    # Custom login
    email = password = ''
    if request.POST:
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(username=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('')

    return render_to_response('login.html', {'email': email})
"""


def tracks(request):
    return render(request, 'Tracks/tracks.html',{})


def signIn(request):
    if (request.method == 'GET'):
        return render(request, 'Tracks/welcome.html',{})


def signUp(request):
    if (request.method == 'GET'):
        return render(request, 'Tracks/signup.html', {})


def about(request):
    if (request.method == 'GET'):
        return render(request, 'Tracks/about.html', {})


def userprofile(request):
    try:
        temp_user = TracksUser.objects.get(email='test') #temporary line. FOR TESTING ONLY
#    temp_user = TracksUser.objects.get(email=request.session.get('email'))
    except:
        response = HttpResponse(traceback.format_exc()) # Currently sends a response with the traceback of the error. DO NOT USE IN PRODUCTION.
        response.status_code = 500;
        return response

    if(TracksUser.has_userprofile(temp_user)):
        temp_instance = temp_user.userprofile
    else:
        temp_instance = UserProfile(user=temp_user)

    if (request.method == 'POST'):
        form = UserProfileForm(request.POST, instance=temp_instance)
        if(form.is_valid):
            try:
                form.save()
                return HttpResponseRedirect('userpage.html');
            except:
                response = HttpResponse(traceback.format_exc()) # Currently sends a response with the traceback of the error. DO NOT USE IN PRODUCTION.
                response.status_code = 500;
                return response
        else:
            form = UserProfileForm(instance=temp_instance)
            return render(request, 'Tracks/userprofile.html', {'user' : temp_user, 'form' : form})

    else: # GET
        form = UserProfileForm(instance=temp_instance)
        return render(request, 'Tracks/userprofile.html', {'user' : temp_user, 'form' : form})


def userpage(request):
    try:
        temp_user = TracksUser.objects.get(email='test') #temporary line. FOR TESTING ONLY
#    temp_user = TracksUser.objects.get(email=request.session.get('email'))
    except:
        response = HttpResponse(traceback.format_exc()) # Currently sends a response with the traceback of the error. DO NOT USE IN PRODUCTION.
        response.status_code = 500;
        return response

    form = UploadFileForm()
    #return render(request, 'Tracks/index.html', {'form': form})
    return render(request, 'Tracks/userpage.html', {'user' : temp_user, 'form' : form})


def upload_MP3(request):
    #print('entered uploadmp3')
    if (request.method == 'POST'):
        form = UploadFileForm(request.POST, request.FILES)
        if (form.is_valid):
            try:
                temp_user = TracksUser.objects.get(email=request.POST['user_email'])
                print temp_user
                temp_mp3 = request.FILES['file']
                new_track = Track(user = temp_user, filename=temp_mp3.name)
                new_track.handle_upload_file(temp_mp3)
                response = HttpResponse('success')
                response.status_code = 200;
                return response
            except:
                response = HttpResponse(traceback.format_exc()) # Currently sends a response with the traceback of the error. DO NOT USE IN PRODUCTION.
                response.status_code = 500;
                return response
        else:
            response = HttpResponse('form not valid')
            response.status_code = 400;
            return response
    else:
        response = HttpResponse('method not post')
        response.status_code = 400;
        return response
