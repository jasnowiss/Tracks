from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)
from django.utils import timezone
import os
from django.db.models import Q

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

    def get_unique_identifier(self):
        return self.email


    @classmethod
    def get_user_desired_to_be_viewed(cls, request, user_id):
        if(user_id != None):
            temp_user = cls.objects.get(id=user_id)
            is_disabled = True
        else:
            temp_user = cls.objects.get(email=request.session.get('email'))
            is_disabled = False
        return temp_user, is_disabled

    @classmethod
    def filter_for_search(cls, searchString):
        list_to_return = []
        if(searchString != None and searchString !=''):
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
    field2 = models.CharField(max_length=200)
    field3 = models.CharField(max_length=200)
    field4 = models.CharField(max_length=200)

    def __unicode__(self):
        return "profile of: " + self.user.username


class Track(models.Model):
    user = models.ForeignKey(TracksUser)
    filename = models.CharField(max_length=50)
    filepath = models.CharField(max_length=200)

    def __unicode__(self):
        return self.filename

    def handle_upload_file(self, f, path="..\\Project\\Tracks\\user_mp3_files"):
        ##print(path)
        ##temp_dest = os.path.join(path, str(self.user.get_unique_identifier()) + "_" + self.filename) # need to change later to be a more unique identifier
        # using user.id and timestamp to decrease chance of filename collisions
        temp_dest = os.path.join(path, str(self.user.id) + "_" + timezone.datetime.now().strftime('%m-%d-%Y_%H-%M-%S'))
        print(temp_dest)
        with open(temp_dest,'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

        self.filepath = temp_dest
        self.save()
        return temp_dest

    @classmethod
    def filter_for_search(cls, searchString):
        list_to_return = []
        if(searchString != None and searchString !=''):
            list_to_return = cls.objects.filter(Q(filename__contains=searchString))
        return list_to_return


class Collaboration(models.Model):
    users = models.ManyToManyField(TracksUser)
    tracks = models.ManyToManyField(Track)

    def __unicode__(self):
        return str(self.id)


##    @classmethod
##    def filter_for_search(cls, searchString):
##        list_to_return = []
##        if(searchString != None and searchString !=''):
##            list_to_return = cls.filter(Q(filename__contains=searchString))
##        return list_to_return



# TODO: in later iterations this function should return a sorted query set
# TODO: for security purposes, need to make sure that searchString does not contain any malicious code. Check to see if Django provides some help for this
def search_relevant_models(searchString):
    list_of_relevant_models = [TracksUser, Track] ## ,Collaboration]
    temp_query_set = []
    for model in list_of_relevant_models:
        temp_query_set += model.filter_for_search(searchString)
    return temp_query_set






