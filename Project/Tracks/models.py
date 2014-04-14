from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)
from django.utils import timezone
import os
from django.db.models import Q
from itertools import chain
from operator import attrgetter

# Create your models here.


class TracksUserManager(BaseUserManager):
    """A class to manage user creation. May not in fact be necessary."""

    def create_user(self, email, firstName, lastName, confirm, password=None,):
        """Creates a new user and adds their information to the database."""
        if not password:
            #raise
            pass
        user = self.model(
            email=self.normalize_email(email),
            firstName=firstName,
            lastName=lastName
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_super_user(self, email, password):
        """For now, fail."""
        raise



class TracksUser(AbstractBaseUser):
    """The class for Tracks Users."""

    email = models.EmailField(max_length=254, unique=True)
    firstName = models.CharField(max_length=45)
    lastName = models.CharField(max_length=45)
    #add support for middle names?
    #require a birthday (i.e. minimum age)?
    #store joined date?
    is_active = models.BooleanField(default=True)
    objects = TracksUserManager()
    REQUIRED_FIELDS = ['firstName', 'lastName']
    USERNAME_FIELD = 'email'

    def __unicode__(self):
        """Returns the user's username (i.e. email address)."""
        return self.email

    def get_full_name(self):
        """Returns the user's full name."""
        fullName = self.firstName.strip() + " " + self.lastName.strip()
        return fullName

    def get_short_name(self):
        """Returns the user's first name."""
        return self.firstName.strip()

    def has_userprofile(self):
        """Returns whether the user has a personal profile."""
        try:
            self.userprofile
            return True
        except:
            return False

    def get_name_to_display(self):
        """Returns the user's display name if they have one, otherwise first and last name."""
        if(self.has_userprofile()):
            if len(self.userprofile.display_name) != 0:
                return self.userprofile.display_name
        return self.firstName + " " + self.lastName

    def get_tracks_list(self): # TODO: need to check if the filepaths are still accurate
        """Returns a list of the user's tracks."""
        return self.track_set.all()

    def get_collaborations_list(self):
        """Returns a list of the user's collaborations."""
        return self.collaboration_set.all()

    def get_user_profile(self):
        """Returns the user's existing profile, or creates a new one to return."""
        if(self.has_userprofile()):
            temp_instance = self.userprofile
        else:
            temp_instance = UserProfile(user=self)
        return temp_instance

    def get_tracks_list_JSON(self):
        """ADD A DESCRIPTION"""
        response_data = {}
        list_of_tracks = self.get_tracks_list()
        for track in list_of_tracks:
            response_data[track.id] = track.filename
        return response_data

    def get_unique_identifier(self):
        """Returns a unique identifier for the user (i.e. email address)."""
        return self.email

##    @classmethod
##    def get_desired_user(cls, session_user_email, id_of_user_desired_to_be_viewed):
##        """ADD A DESCRIPTION"""
##        if(id_of_user_desired_to_be_viewed != None):
##            temp_user = cls.objects.get(id=id_of_user_desired_to_be_viewed)
##            is_disabled = True
##        else:
##            temp_user = cls.objects.get(email=session_user_email)
##            is_disabled = False
##        return temp_user, is_disabled

    @classmethod
    def get_desired_user(cls, session_user, id_of_user_desired_to_be_viewed):
        """ADD A DESCRIPTION"""
        if(id_of_user_desired_to_be_viewed != None):
            temp_user = cls.objects.get(id=id_of_user_desired_to_be_viewed)
            is_disabled = True
        else:
            temp_user = session_user
            is_disabled = False
        return temp_user, is_disabled

    @classmethod
    def filter_for_search(cls, searchString):
        """ADD A DESCRIPTION"""
        list_to_return = []

        # allow only searchString which won't return every user in the database
        # TODO: Need a better way to guarantee above comment. Current blacklisting might need to be replaced with whitelisting.
        if(searchString != None and searchString !='' and (len(searchString)>4 or '.com'.count(searchString) == 0) and '@'.count(searchString) == 0):
            list_to_return = cls.objects.filter(Q(email__contains=searchString) | Q(firstName__contains=searchString) | Q(lastName__contains=searchString))
        return list_to_return


INSTRUMENT_CHOICES = (
    ('BASS', 'Bass'),
    ('DRUMS', 'Drums'),
    ('GUITAR', 'Guitar'),
    ('VOCALS', 'Vocals')
    )


class UserProfile(models.Model):
    """A class to hold basic information about a user."""

    user = models.OneToOneField(TracksUser)
    instrument = models.CharField(max_length=200, choices=INSTRUMENT_CHOICES)
    display_name = models.CharField(max_length=200)
    field3 = models.CharField(max_length=200)
    field4 = models.CharField(max_length=200)

    def __unicode__(self):
        """Returns the user's username (i.e. email address)."""
        return "profile of: " + self.user.email

    @classmethod
    def filter_for_search(cls, searchString):
        """ADD A DESCRIPTION"""
        list_to_return = []
        profile_list = []
        if(searchString != None and searchString !=''):
            profile_list = cls.objects.filter(Q(instrument__contains=searchString))
            for item in profile_list:
                list_to_return.append([item.instrument, "Instrument", item])
            profile_list = cls.objects.filter(Q(display_name__contains=searchString))
            for item in profile_list:
                list_to_return.append([item.display_name, "Display Name", item])
            profile_list = cls.objects.filter(Q(field3__contains=searchString))
            for item in profile_list:
                list_to_return.append([item.field3, "Field 3", item])
            profile_list = cls.objects.filter(Q(field4__contains=searchString))
            for item in profile_list:
                list_to_return.append([item.field4, "Field 4", item])
        return list_to_return


#list of acceptable extensions. make sure it starts with a dot'
ACCEPTABLE_MUSIC_FORMATS = ['.mp3','.wav']

class Track(models.Model):
    """A class to manage sound files."""

    user = models.ForeignKey(TracksUser)
    filename = models.CharField(max_length=50)
    filepath = models.CharField(max_length=200)
    displayname = models.CharField(max_length=50, default=filename)

    def __unicode__(self):
        """Returns the name of the file."""
        return self.filename

    def get_server_filename(self):
        """ADD A DESCRIPTION"""
        server_filename = '#'
        temp_filepath = self.filepath
        if(os.path.exists(temp_filepath)):
            server_filename = os.path.basename(temp_filepath)
        return server_filename

    def handle_upload_file(self, f, path="../Project/Tracks/user_mp3_files"):
        """ADD A DESCRIPTION"""
        ##print(path)
        ##temp_dest = os.path.join(path, str(self.user.get_unique_identifier()) + "_" + self.filename) # need to change later to be a more unique identifier
        # using user.id and timestamp to decrease chance of filename collisions
        temp_dest = os.path.join(path, str(self.user.id) + "_" + timezone.datetime.now().strftime('%m-%d-%Y_%H-%M-%S') + ".mp3").replace('\\', '/')
        ##print(temp_dest)
        with open(temp_dest,'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

        self.filepath = temp_dest
        self.save()
        return temp_dest

    def getDisplayName(self):
        """
        Returns the track's display name
        """
        return self.displayname

    def rename(self, new_display_name):
        """
        Sets this track's display name to new_display_name. Returns ERR_NAME_TOO_LONG if > 50 characters.
        ALWAYS MAKE SURE TO USE force_escape AND escapejs FILTERS ON DISPLAY
        """
        if len(new_display_name) > 50:
            return ERR_NAME_TOO_LONG
        track = Track.objects.get(displayname=self.displayname)
        track.displayname = new_display_name
        track.save()
        return SUCCESS

    @classmethod
    def is_music_file_valid(cls, temp_file):
        """Returns whether the file is of appropriate size and ends with a valid extension."""
        #currently the size of the file is a static final, however we should consider having a quota per user, in case a user wishes to extend their quota.
        # 2.5MB - 2621440
        # 5MB - 5242880
        # 10MB - 10485760
        # 20MB - 20971520
        # 50MB - 52428800
        # 100MB 104857600
        # 250MB - 214958080
        # 500MB - 429916160
        SIZE_LIMIT = 52428800

        #check the size of the file
        sizeOfFile = temp_file._size
        error = None
        notSupported = True

        for name in ACCEPTABLE_MUSIC_FORMATS:
            if temp_file.name.endswith(name):
               notSupported = False

        if notSupported:
            error = 'File extension not supported'
        if sizeOfFile > SIZE_LIMIT:
            error = 'File exceeding size limit'
        return error

    @classmethod
    def handle_music_file_upload(cls, temp_user, temp_file):
        """ADD A DESCRIPTION"""
        server_filename = ''
        track_id = 0
        error = Track.is_music_file_valid(temp_file)

        if(error == None):
            new_track = Track(user = temp_user, filename=temp_file.name)
            new_track.handle_upload_file(temp_file)
            History.add_history(new_track.user, new_track, ADDED_HISTORY)
            server_filename = new_track.get_server_filename()
            track_id = new_track.id

        return server_filename, track_id, error

    @classmethod
    def filter_for_search(cls, searchString):
        """ADD A DESCRIPTION"""
        list_to_return = []
        if(searchString != None and searchString !=''):
            list_to_return = cls.objects.filter(Q(filename__contains=searchString))
        return list_to_return

    @classmethod
    def handle_delete_track(cls, track_id):
        """ Returns True if track has been successfully deleted from the database and its corresponding file has been deleted from the server.
            Otherwise, returns False """
        track = Track.objects.get(id=track_id)
        if (track == None):
            return False
        temp_filepath = track.filepath
        if (os.path.isfile(temp_filepath)):
            os.remove(temp_filepath)
            track.delete()
            return True
        else:
            return False



class Collaboration(models.Model):
    """A class for managing the layering and editing of Tracks."""

    users = models.ManyToManyField(TracksUser) # In future iterations, this may also play a role in add/modify permissions for a collaboration
    tracks = models.ManyToManyField(Track)
    displayname = models.CharField(max_length=50)

    def __unicode__(self):
        """Returns the default django identifier."""
        return str(self.id)

    def handle_adding_track(self, temp_track):
        """Adds a track to the list of tracks in this collaboration, and adds the user who added it."""
        self.tracks.add(temp_track)
        self.users.add(temp_track.user)

    def handle_removing_track(self, temp_track):
        """Removes a track from the collaboration.

        Note: if temp_track.user has no more tracks in this collaboration,
              then remove him/her from the collaboration.
              Subject to change, depending on how users field ends up being used (in regard to permissions)

        """
        self.tracks.remove(temp_track)

        if(len(self.tracks.filter(user=temp_track.user)) == 0):
            self.users.remove(temp_track.user)

    def getDisplayName(self):
        """
        Returns the collaboration's display name
        """
        return self.displayname

    def rename(self, new_display_name):
        """
        Sets this collaboration's display name to new_display_name. Returns ERR_NAME_TOO_LONG if > 50 characters.
        ALWAYS MAKE SURE TO USE force_escape AND escapejs FILTERS ON DISPLAY
        """
        if len(new_display_name) > 50:
            return ERR_NAME_TOO_LONG
        collaboration = Collaboration.objects.get(displayname=self.displayname)
        collaboration.displayname = new_display_name
        collaboration.save()
        return SUCCESS

    @classmethod
    def handle_finalization(cls, track1_id, track2_id, collab_id, mod_type):
        """ADD A DESCRIPTION"""
        filtered_track1 = Track.objects.filter(id=track1_id)
        filtered_track2 = Track.objects.filter(id=track2_id)
        filtered_collab = Collaboration.objects.filter(id=collab_id)

        if (len(filtered_track1) == 0 and len(filtered_track2) == 0):
            raise LookupError("no such track 1 and track 2")
        else: # at least one of the tracks is exists in the DB
            temp_collab = None
            track1 = None
            track2 = None
            list_of_valid_tracks = []
            if(len(filtered_collab) == 0):
                temp_collab = Collaboration()
                temp_collab.save()
                history_type = ADDED_HISTORY
            else:
                temp_collab = filtered_collab[0]
                history_type = MODIFIED_HISTORY

            if (len(filtered_track1) != 0):
                track1 = filtered_track1[0]
                list_of_valid_tracks.append(track1)

            if(len(filtered_track2) != 0):
                track2 = filtered_track2[0]
                list_of_valid_tracks.append(track2)


            temp_dict = dict()
            for i in xrange(0, len(list_of_valid_tracks)):
                temp_track = list_of_valid_tracks[i]
                if(mod_type.lower().count("remove") != 0):
                    temp_collab.handle_removing_track(temp_track)
                else: # default action is to add
                    temp_collab.handle_adding_track(temp_track)

                if (not temp_dict.has_key(temp_track.user.id)):
                    temp_dict[temp_track.user.id] = 1
                    History.add_history(temp_track.user, temp_collab, history_type)


            temp_collab.save()
            return temp_collab


##    @classmethod
##    def filter_for_search(cls, searchString):
##        list_to_return = []
##        if(searchString != None and searchString !=''):
##            list_to_return = cls.filter(Q())
##        return list_to_return


ADDED_HISTORY = 'added'
MODIFIED_HISTORY = 'modified'

class History(models.Model):
    """ADD A DESCRIPTION"""
    user = models.ForeignKey(TracksUser)
    added = models.BooleanField(default=False)
    modified = models.BooleanField(default=False)
    track = models.ForeignKey(Track, null=True)
    collaboration = models.ForeignKey(Collaboration, null=True)
    timestamp = models.DateTimeField()

    def __unicode__(self):
        """ADD A DESCRIPTION"""
        return "id:" + str(self.id) + " " + "timestamp:" + self.timestamp.strftime('%m/%d/%Y %H:%M:%S')

    @classmethod
    def get_downbeat_for(cls, temp_user):
        """ADD A DESCRIPTION"""
        downbeat_list = None
        for collab in temp_user.collaboration_set.all():
            for collab_friend in collab.users.filter(~Q(email=temp_user.email)):
                if(downbeat_list != None):
                    downbeat_list = chain(downbeat_list, History.get_history_for(collab_friend))
                else:
                    downbeat_list = History.get_history_for(collab_friend)

        if (downbeat_list == None):
            downbeat_list = []
        else:
            downbeat_list = sorted(downbeat_list, key=lambda elem: elem.timestamp, reverse=True)

        return downbeat_list

    @classmethod
    def get_history_for(cls, model_object):
        """ADD A DESCRIPTION"""
        return model_object.history_set.all()

    @classmethod
    def add_history(cls, temp_user, model_object, added_or_modified):
        """ADD A DESCRIPTION"""
        temp_history = History(user=temp_user, timestamp=timezone.datetime.now())
        temp_history.added = True if (added_or_modified == ADDED_HISTORY) else False
        temp_history.modified = True if (added_or_modified == MODIFIED_HISTORY) else False
        if(type(model_object) == Track):
            temp_history.track = model_object
            temp_history.save()
        elif(type(model_object) == Collaboration):
            temp_history.collaboration = model_object
            temp_history.save()


def search_relevant_models(searchString):
    """ ADD A DESCRIPTION

    TODO: in later iterations this function should return a sorted query set
    TODO: for security purposes, need to make sure that searchString does not contain any malicious code. Check to see if Django provides some help for this

    """
    list_of_relevant_models = [TracksUser, Track, UserProfile] ## ,Collaboration]
    temp_query_set = []
    for model in list_of_relevant_models:
        temp_query_set += model.filter_for_search(searchString)
    return temp_query_set

ERR_NAME_TOO_LONG = -1
SUCCESS = 1






