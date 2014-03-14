from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)
from django.utils import timezone
import os

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


class Track(models.Model):
    filename = models.CharField(max_length=50)
    filepath = models.CharField(max_length=200)

    def __unicode__(self):
        return self.filename


def handle_upload_file(f, track, path="..\\Project\\Tracks\\user_mp3_files"):
    ##print(path)
    temp_dest = os.path.join(path, timezone.datetime.now().strftime('%m-%d-%Y_%H-%M-%S'))
    print(temp_dest)
    with open(temp_dest,'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    track.filepath = temp_dest
    track.save()
    return temp_dest
    
