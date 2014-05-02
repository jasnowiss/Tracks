# Create your views here.
from django import forms
from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import *
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from Tracks.forms import *
from Tracks.models import *
import Tracks
import os
##import sys
import traceback
import json

from django.views.decorators.csrf import ensure_csrf_cookie

# need these for serving mp3 files from this Django server. If another server handles serving mp3 files, these can be removed.
# see play_mp3 function at bottom of page for more details.
import Project.settings
from django.core.servers.basehttp import FileWrapper



"""
TODO:

"""

def editTrack(request, track_id):
    if request.method == 'GET':
        id_int = int(track_id)
        try:
            track = Track.objects.get(id=id_int)
            return render(request, 'Tracks/index.html', {"track":track_id, "track":track.get_server_filename()})
        except:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



def register(request):
    """Registers a user."""
    email = password = ''
    if request.method == 'POST':
        form = TracksUserCreationForm(request.POST)
        #perhaps need to log in the user as well?
        #Need error handling
        email = request.POST.get('email')
        password = request.POST.get('password')
        #firstName = request.POST.get('firstName')
        #lastName = request.POST.get('lastName')
        #confirm = request.POST.get('confirm')
        #user = TracksUser.objects.create_user(email, firstName, lastName, confirm, password)
        try:
            user = form.save()
            user = authenticate(username=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/Tracks/userpage/')
        except ValueError:
            form = TracksUserCreationForm()
            return render(request, 'Tracks/signup.html', {'form': form, 'session':request.user.is_authenticated(), 'haserror': True})
    else:
        form = TracksUserCreationForm()
        return render(request, 'Tracks/signup.html', {'form': form, 'session':request.user.is_authenticated(),'has_error':False})


def signIn(request):
    """ADD A DESCRIPTION"""
    # Custom login
    email = password = msg = ''
    if request.POST:
        form = TracksUserSignInForm(request.POST)
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        user = authenticate(username=email, password=password) #Unlike the TracksUserCreationForm, this form does not do the required work
        #Need error handling
        if user is not None:
            if user.is_active:
                login(request, user)
                if next in request.POST:
                    #We've been redirected; return the user where they want to go
                    url = request.POST.get('next')
                    HttpResponseRedirect(url)
                return HttpResponseRedirect('/Tracks/userpage') # should be user's profile when ready
            else:
                #Will we ever have inactive users? Maybe instead of deletion?
                #msg = 'That user is inactive!' (does this reveal too much information about a user?)
                #render(request, 'Tracks/signin.html', {'form': form, 'msg': msg})
                pass
        else:
            #Invalid password, we need to alert the user
            #msg = 'Invalid username/password combination!'
            #render(request, 'Tracks/signin.html', {'form': form, 'msg': msg})
            pass
    else:
        form = TracksUserSignInForm()
    return render(request, 'Tracks/signin.html', {'form': form, 'session':request.user.is_authenticated()})


def logout_view(request):
    """ADD A DESCRIPTION"""
    logout(request)
    return HttpResponseRedirect('/Tracks') #should be a log out page instead


def tracks(request):
    """ADD A DESCRIPTION"""
    return render(request, 'Tracks/tracks.html',{'session':request.user.is_authenticated()})



def about(request):
    """ADD A DESCRIPTION"""
    if (request.method == 'GET'):
        return render(request, 'Tracks/about.html', {'session':request.user.is_authenticated()})


@login_required
def userprofile(request, user_id=None):
    """ADD A DESCRIPTION"""
    try:
        temp_user, is_disabled = TracksUser.get_desired_user(get_session_user(request), user_id)
        temp_instance = temp_user.get_user_profile()

        if(request.method == 'GET'):
            form = UserProfileForm(instance=temp_instance)
            return render(request, 'Tracks/userprofile.html', {'user' : temp_user, 'form' : form, 'is_disabled' : is_disabled})

        elif (request.method == 'POST'):
            form = UserProfileForm(request.POST, instance=temp_instance)
            if(form.is_valid()):
                try:
                    form.save()
                    return HttpResponseRedirect('/Tracks/userpage/');
                except:
                    response = HttpResponse('userprofile could not be saved') # May need to change message sent
                    print(traceback.format_exc()) # for debugging purposes only. DO NOT USE IN PRODUCTION
                    response.status_code = 500;
                    return response
            else:
                form = UserProfileForm(instance=temp_instance)
                return render(request, 'Tracks/userprofile.html', {'user' : temp_user, 'form' : form})

        else:
            response = HttpResponse('Request was neither a GET or a POST') # Probably a good idea to mark as DO NO USE IN PRODUCTION.
            response.status_code = 500;
            return response

    except:
        response = HttpResponse('error in userprofile') # May need to change message sent
        print(traceback.format_exc())  # for debugging purposes only. DO NOT USE IN PRODUCTION
        response.status_code = 500;
        return response


@login_required
def userpage(request, user_id=None):
    """ADD A DESCRIPTION"""
    try:
        session_user = get_session_user(request)
        temp_user, is_disabled = TracksUser.get_desired_user(session_user, user_id)

        if(request.method == "GET"):
            form = UploadFileForm()
            list_of_tracks = temp_user.get_tracks_list()
            list_of_collaborations = temp_user.get_collaborations_list()
            return render(request, 'Tracks/userpage.html', {'user' : temp_user, 'session_user' : session_user, 'form' : form, 'is_disabled' : is_disabled,
                                                                'list_of_tracks' : list_of_tracks, 'list_of_collaborations' : list_of_collaborations})

    except:
        response = HttpResponse('error in userpage') # May need to change message sent
        print(traceback.format_exc())  # for debugging purposes only. DO NOT USE IN PRODUCTION
        response.status_code = 500;
        return response


@login_required
def search(request):
    """ADD A DESCRIPTION"""
    if(request.method == "GET"):
        searchString = request.GET.get('search', None)
        # TODO: for security purposes, need to make sure that searchString does not contain any malicious code. Check to see if Django provides some help for this.
        filtered_query_set = search_relevant_models(searchString)
        return render(request, 'Tracks/search.html', {'filtered_query_set' : filtered_query_set, 'session' : request.user.is_authenticated()})
    else:
        response = HttpResponse('you did not send a GET request to search') # message string probably needs to change for production version
        response.status_code = 500;
        return response


@login_required
def downbeat(request):
    """ADD A DESCRIPTION"""
    if (request.method == 'GET'):
        # don't actually need the value of is_disabled, but getting it anyway as it is returned by the function
        temp_user, is_disabled = TracksUser.get_desired_user(get_session_user(request), None)
        downbeat_list = History.get_downbeat_for(temp_user)
        return render(request, 'Tracks/downbeat.html', {'user' : temp_user, 'downbeat_list' : downbeat_list})


# Function for JSON Call
def get_tracks_for_current_user_JSON(request):
    """ADD A DESCRIPTION"""
    try:
        # don't actually need the value of is_disabled, but getting it anyway as it is returned by the function
        temp_user, is_disabled = TracksUser.get_desired_user(get_session_user(request), None)
        response_data = temp_user.get_tracks_list_JSON()
        response = HttpResponse(json.dumps(response_data), content_type="application/json")
        return response
    except:
        response = HttpResponse('error trying to send list of tracks for current user') # May need to change message sent
        print(traceback.format_exc())  # for debugging purposes only. DO NOT USE IN PRODUCTION
        response.status_code = 500;
        return response

# Function for JSON Call
def get_collab_settings_JSON(request):
    try:
        collab_id = int(request.GET.get('collab_id'))
        collab = Collaboration.objects.get(id=collab_id)
        response_data = collab.get_settings_list_JSON()
        response = HttpResponse(json.dumps(response_data), content_type="application/json")
        return response
    except:
        response = HttpResponse('error trying to get settings for collaboration') # May need to change message sent
        print(traceback.format_exc())  # for debugging purposes only. DO NOT USE IN PRODUCTION
        response.status_code = 500;
        return response

# Function for JSON Call
def get_update_collab_JSON(request):
    try:
        collab_id = int(request.GET.get('collab_id'))
        collab_last_history_id = request.GET.get('collab_last_history_id')
        session_user = get_session_user(request)
        collab = Collaboration.objects.get(id=collab_id)
        response_data = collab.get_update_data_JSON(session_user, collab_last_history_id)
        print(response_data)
        response = HttpResponse(json.dumps(response_data), content_type="application/json")
        return response
    except:
        response = HttpResponse('error trying to update collaboration') # May need to change message sent
        print(traceback.format_exc())  # for debugging purposes only. DO NOT USE IN PRODUCTION
        response.status_code = 500;
        return response

# Function for AJAX Call
def finalize_collaboration(request):
    """ADD A DESCRIPTION"""
    try:
        track1_id = int(request.POST.get('track1_id', 0))
        track2_id = int(request.POST.get('track2_id', 0))
        collab_id = int(request.POST.get('collab_id', 0))
        mod_type = request.POST['mod_type']

        temp_user, is_disabled = TracksUser.get_desired_user(get_session_user(request), None)
        collab = Collaboration.handle_finalization(temp_user, track1_id, track2_id, collab_id, mod_type)

        response = HttpResponse('success') ## render(request, 'Tracks/collaboration_for_AJAX.html', {'collaboration' : collab})
        response.status_code = 200
        return response
    except:
        response = HttpResponse('error trying to finalize collaboration') # May need to change message sent
        print(traceback.format_exc())  # for debugging purposes only. DO NOT USE IN PRODUCTION
        response.status_code = 500
        return response


# Function for AJAX Call
def delete_track_from_server(request):
    try:
        track_id = int(request.POST.get('track_id', 0))
        if (Track.handle_delete_track(track_id)):
            response = HttpResponse('success')
            response.status_code = 200
            return response
        else:
            response = HttpResponse('no such track exists')
            response.status_code = 400
            return response
    except:
        response = HttpResponse('error trying to delete track') # May need to change message sent
        print(traceback.format_exc())  # for debugging purposes only. DO NOT USE IN PRODUCTION
        response.status_code = 500
        return response

# Function for AJAX Call
def change_permission_of_collab(request):
    try:
        collab_id = int(request.POST.get('collab_id'))
        bool_permission = request.POST.get('bool_permission')
        ##print(bool_permission)
        temp_user, is_disabled = TracksUser.get_desired_user(get_session_user(request), None)

        collab = Collaboration.objects.get(id=collab_id)
        collab.set_permission_level(temp_user, bool_permission=bool_permission)

        response = HttpResponse('success')
        response.status_code = 200
        return response
    except:
        response = HttpResponse('error trying to change permission of collaboration') # May need to change message sent
        print(traceback.format_exc())  # for debugging purposes only. DO NOT USE IN PRODUCTION
        response.status_code = 500
        return response

# Function for AJAX Call
def add_user_to_collab(request):
    try:
        collab_id = int(request.POST.get('collab_id'))
        searchString = request.POST.get('searchString')

        session_user = get_session_user(request)

        collab = Collaboration.objects.get(id=collab_id)
        temp_user = collab.add_user_using_searchString(session_user, searchString)

        if(temp_user == None):
            response = HttpResponse("could not find user") # May need to change message sent
            response.status_code = 400
        else:
            response_data = { "user_id" : temp_user.id, "name_to_display" : temp_user.get_name_to_display() }
            response = HttpResponse(json.dumps(response_data), content_type="application/json")
            response.status_code = 200

        return response
    except:
        response = HttpResponse('error trying to add user to collaboration') # May need to change message sent
        print(traceback.format_exc())  # for debugging purposes only. DO NOT USE IN PRODUCTION
        response.status_code = 500
        return response

# Function for AJAX Call
def remove_user_from_collab(request):
    try:
        user_id = int(request.POST.get('user_id'))
        collab_id = int(request.POST.get('collab_id'))

        temp_user, is_disabled = TracksUser.get_desired_user(get_session_user(request), None)
        collab = Collaboration.objects.get(id=collab_id)
        if(collab.remove_user(temp_user, user_id)):
            response = HttpResponse('success')
            response.status_code = 200
        else:
            response = HttpResponse("could not remove user") # May need to change message sent
            print("could not remove user. either user does not exist or user is the last user remaining(and therefore can not be removed)") # for debugging purposes only. DO NOT USE IN PRODUCTION
            response.status_code = 400

        return response
    except:
        response = HttpResponse('error trying to remove user from collaboration') # May need to change message sent
        print(traceback.format_exc())  # for debugging purposes only. DO NOT USE IN PRODUCTION
        response.status_code = 500
        return response

# Fuction for AJAX Call
@login_required
def upload_MP3(request):
    """ADD A DESCRIPTION"""
    try:
        if (request.method == 'POST'):
            form = UploadFileForm(request.POST, request.FILES)
            if (form.is_valid()):
                temp_file = request.FILES['file']
                # don't actually need the value of is_disabled, but getting it anyway as it is returned by the function
                temp_user, is_disabled = TracksUser.get_desired_user(get_session_user(request), None)
                server_filename, track_id, error = Track.handle_music_file_upload(temp_user, temp_file)
                if(error != None):
                    response = HttpResponse(error)
                    response.status_code = 400;
                    return response

                response_data = {"server_filename" : server_filename, "track_id" : track_id}
                response = HttpResponse(json.dumps(response_data), content_type="application/json")
                response.status_code = 200;
                return response
            else:
                response = HttpResponse('form not valid')
                response.status_code = 400;
                return response
        else:
            response = HttpResponse('method not post')
            response.status_code = 400;
            return response

    except:
        response = HttpResponse('error with userprofile') # May need to change message sent
        print(traceback.format_exc())  # for debugging purposes only. DO NOT USE IN PRODUCTION
        response.status_code = 500;
        return response


def get_session_user(request):
    """Helper function for getting session. SHOULD NOT BE REQUESTED BY THE CLIENT"""
    return request.user

def play_MP3(request, path):
    """Allows the server to serve audio/mpeg files (e.g. mp3 files).

    Note: Can be removed if another server is responsible for serving audio/mpeg files.

    """
    filepath = os.path.join(Project.settings.MEDIA_ROOT, path).replace('\\', '/')
    #print(filepath)
    wrapper = FileWrapper(open(filepath, 'rb'))
    response = StreamingHttpResponse(wrapper, content_type='audio/mpeg')
    response['Content-Length'] = os.path.getsize(filepath)
    response['Content-Disposition'] = 'attachment; filename=%s' % path
    return response


@login_required
@ensure_csrf_cookie
def record(request):
    #get user
    user, is_disabled = TracksUser.get_desired_user(get_session_user(request), None)
    if not is_disabled:
        return render(request, 'Tracks/record.html', {'user': user})
    else:
        return render(request, 'Tracks/disabled')

@login_required
def handleRecordFromEdit(request, collaboration_id):
    """
    Saves a user-recorded blob as an .mp3.
    """
    if not request.method == 'POST' or not request.is_ajax():
        raise Http404
    file_name = request.POST.get('filename')
    audio = request.FILES.get('audio')
    ##SIZE_LIMIT = 5242880 #Should probably be made global, currently same as upload_mp3's SIZE_LIMIT
    try:
##        if audio.size > SIZE_LIMIT:
##            #handle size error
##            pass
        #need to convert from WAV to MP3
        temp_user, is_disabled = TracksUser.get_desired_user(get_session_user(request), None)
##        new_track = Track(user=temp_user, filename=file_name)
##        new_track.handle_upload_file(audio)
        server_filename, track_id, error = Track.handle_music_file_upload(temp_user, audio)
##        History.add_history(new_track.user, new_track, ADDED_HISTORY)
        if(error == None):
            collab = Collaboration.handle_finalization(temp_user, track_id, 0, collaboration_id, "add")
            response = HttpResponse('success')
            response.status_code = 200;
            return response
        else:
            response = HttpResponse(error)
            response.status_code = 500;
            return response
    except:
        #handle error
        pass

@login_required
def handleRecord(request):
    """
    Saves a user-recorded blob as an .mp3.
    """
    if not request.method == 'POST' or not request.is_ajax():
        raise Http404
    file_name = request.POST.get('filename')
    audio = request.FILES.get('audio')
    ##SIZE_LIMIT = 5242880 #Should probably be made global, currently same as upload_mp3's SIZE_LIMIT
    try:
##        if audio.size > SIZE_LIMIT:
##            #handle size error
##            pass
        #need to convert from WAV to MP3
        temp_user, is_disabled = TracksUser.get_desired_user(get_session_user(request), None)
##        new_track = Track(user=temp_user, filename=file_name)
##        new_track.handle_upload_file(audio)
        server_filename, track_id, error = Track.handle_music_file_upload(temp_user, audio)
        ##History.add_history(new_track.user, new_track, ADDED_HISTORY)
        if(error == None):
            response = HttpResponse('success')
            response.status_code = 200
            return response
        else:
            response = HttpResponse(error)
            response.status_code = 500;
            return response
    except:
        #handle error
        pass

def resetFixture(request):
    reset_fixture()
    return HttpResponse("Fixture reset")

@login_required
def edit(request, collaboration_id):
    collaboration = Collaboration.objects.get(id=collaboration_id)
    return render(request, 'Tracks/edit.html', {"collaboration": collaboration})

def change_name(request, collaboration_id):
    collaboration = Collaboration.objects.get(id=collaboration_id)
    new_name = request.POST['new_name']
    collaboration.handle_change_name(new_name)
    return render(request, 'Tracks/edit.html', {"collaboration": collaboration})


