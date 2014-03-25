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
        """For now, fail"""
        raise


class TracksUser(AbstractBaseUser):
    """
    The class for Tracks Users. As of now requires an email address,
    a first name, and a last name.
    """
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
        """Return the username (i.e. email address)"""
        return self.email

    def get_full_name(self):
        """Returns the user's full name."""
        fullName = self.firstName.strip() + " " + self.lastName.strip()
        return firstName

    def get_short_name(self):
        """Returns the user's first name."""
        return self.firstName.strip()

    def has_userprofile(self):
        try:
            self.userprofile
            return True
        except:
            return False

    def get_name_to_display(self):
        if(self.has_userprofile()):
            if(len(self.userprofile.display_name) != 0):
                return self.userprofile.display_name
            else:
                return self.firstName + " " + self.lastName
        else:
            return self.firstName + " " + self.lastName

    def get_tracks_list(self): # TODO: need to check if the filepaths are still accurate
        return self.track_set.all()

    def get_collaborations_list(self):
        return self.collaboration_set.all()

    def get_user_profile(self):
        if(self.has_userprofile()):
            temp_instance = self.userprofile
        else:
            temp_instance = UserProfile(user=self)
        return temp_instance

    def get_tracks_list_JSON(self):
        response_data = {}
        list_of_tracks = self.get_tracks_list()
        for track in list_of_tracks:
            response_data[track.id] = track.filename
        return response_data

    def get_unique_identifier(self):
        return self.email


    @classmethod
    def get_desired_user(cls, session_user_email, id_of_user_desired_to_be_viewed):
        if(id_of_user_desired_to_be_viewed != None):
            temp_user = cls.objects.get(id=id_of_user_desired_to_be_viewed)
            is_disabled = True
        else:
            temp_user = cls.objects.get(email=session_user_email)
            is_disabled = False
        return temp_user, is_disabled

    @classmethod
    def filter_for_search(cls, searchString):
        list_to_return = []

        # allow only searchString which won't return every user in the database
        # TODO: Need a better way to gaurantee above comment. Current blacklisting might need to be replaced with whitelisting.
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
    user = models.OneToOneField(TracksUser)
    instrument = models.CharField(max_length=200, choices=INSTRUMENT_CHOICES)
    display_name = models.CharField(max_length=200)
    field3 = models.CharField(max_length=200)
    field4 = models.CharField(max_length=200)

    def __unicode__(self):
        return "profile of: " + self.user.username


#list of acceptable extensions. make sure it starts with a dot'
ACCEPTABLE_MUSIC_FORMATS = ['.mp3']

class Track(models.Model):
    user = models.ForeignKey(TracksUser)
    filename = models.CharField(max_length=50)
    filepath = models.CharField(max_length=200)

    def __unicode__(self):
        return self.filename

    def get_server_filename(self):
        server_filename = '#'
        temp_filepath = self.filepath
        if(os.path.exists(temp_filepath)):
            server_filename = os.path.basename(temp_filepath)
        return server_filename

    def handle_upload_file(self, f, path="../Project/Tracks/user_mp3_files"):
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

    @classmethod
    def is_music_file_valid(cls, temp_file):
        #currently the size of the file is a static final, however we should consider having a quota per user, in case a user wishes to extend their quota.
        # 2.5MB - 2621440
        # 5MB - 5242880
        # 10MB - 10485760
        # 20MB - 20971520
        # 50MB - 52428800
        # 100MB 104857600
        # 250MB - 214958080
        # 500MB - 429916160
        SIZE_LIMIT = 5242880

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
        list_to_return = []
        if(searchString != None and searchString !=''):
            list_to_return = cls.objects.filter(Q(filename__contains=searchString))
        return list_to_return


class Collaboration(models.Model):
    users = models.ManyToManyField(TracksUser) # In future iterations, this may also play a role in add/modify permissions for a collaboration
    tracks = models.ManyToManyField(Track)

    def __unicode__(self):
        return str(self.id)

    def handle_adding_track(self, temp_track):
        self.tracks.add(temp_track)
        self.users.add(temp_track.user)

    def handle_removing_track(self, temp_track):
        self.tracks.remove(temp_track)

        # if temp_track.user has no more tracks in this collaboration, then remove him/her from the collaboration.
        # Subject to change, depending on how users field ends up being used (in regard to permissions)
        if(len(self.tracks.filter(user=temp_track.user)) == 0):
            self.users.remove(temp_track.user)

    @classmethod
    def handle_finalization(cls, track1_id, track2_id, collab_id, mod_type):
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
    user = models.ForeignKey(TracksUser)
    added = models.BooleanField(default=False)
    modified = models.BooleanField(default=False)
    track = models.ForeignKey(Track, null=True)
    collaboration = models.ForeignKey(Collaboration, null=True)
    timestamp = models.DateTimeField()

    def __unicode__(self):
        return "id:" + str(self.id) + " " + "timestamp:" + self.timestamp.strftime('%m/%d/%Y %H:%M:%S')

    @classmethod
    def get_downbeat_for(cls, temp_user):
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
        return model_object.history_set.all()

    @classmethod
    def add_history(cls, temp_user, model_object, added_or_modified):
        temp_history = History(user=temp_user, timestamp=timezone.datetime.now())
        temp_history.added = True if (added_or_modified == ADDED_HISTORY) else False
        temp_history.modified = True if (added_or_modified == MODIFIED_HISTORY) else False
        if(type(model_object) == Track):
            temp_history.track = model_object
            temp_history.save()
        elif(type(model_object) == Collaboration):
            temp_history.collaboration = model_object
            temp_history.save()



# TODO: in later iterations this function should return a sorted query set
# TODO: for security purposes, need to make sure that searchString does not contain any malicious code. Check to see if Django provides some help for this
def search_relevant_models(searchString):
    list_of_relevant_models = [TracksUser, Track] ## ,Collaboration]
    temp_query_set = []
    for model in list_of_relevant_models:
        temp_query_set += model.filter_for_search(searchString)
    return temp_query_set






