"""Adapted from Jonathan Chu's example: https://github.com/jonathanchu/django-custom-user-example/blob/master/customuser/accounts/forms.py """

from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.forms import ModelForm
from Tracks.models import *

class TracksUserSignInForm(forms.ModelForm):
  error_messages = {}
  email = forms.CharField(label="Email Address", max_length=254)
  password = forms.CharField(label="Password", widget=forms.PasswordInput)

  class Meta:
    model = TracksUser
    fields = ("email",)

class TracksUserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'alreadyExists': "A account with that e-mail adress already exists!",
        'password_mismatch': "The two password fields don't match!",
    }
    firstName = forms.CharField(label="First Name", max_length=45)
    lastName = forms.CharField(label="Last Name", max_length=45)
    email = forms.EmailField(label="Email Address", max_length=254)
    password = forms.CharField(label="Password",
        widget=forms.PasswordInput)
    confirm = forms.CharField(label="Password confirmation",
        widget=forms.PasswordInput,
        help_text="Enter the same password as above, for verification.")

    class Meta:
        # Point to TracksUser here instead of default `User`
        model = TracksUser
        fields = ("email", "firstName", "lastName","password","confirm")

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["email"]
        try:
            # Refer to TracksUser here instead of default `User`
            TracksUser._default_manager.get(username=username)
        except TracksUser.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['alreadyExists'])

    def clean_confirm(self):
        password = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm")
        if password and confirm and password == confirm:
            return confirm
        raise forms.ValidationError(
            self.error_messages['password_mismatch'])

    def save(self, commit=True):
        # Make sure we pass back in our TracksUserCreationForm and not the
        # default `UserCreationForm`
        user = super(TracksUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class TracksUserChangeForm(forms.ModelForm):
    firstName = forms.CharField(label="First Name", max_length=45)
    lasttName = forms.CharField(label="Last Name", max_length=45)
    password = ReadOnlyPasswordHashField(label="Password")

    class Meta:
        # Point to our TracksUser here instead of default `User`
        model = TracksUser

    def __init__(self, *args, **kwargs):
        # Make sure we pass back in our TracksUserChangeForm and not the
        # default `UserChangeForm`
        super(TracksUserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        """Regardless of what the user provides, return the initial value.
        This is done here, rather than on the field, because the
        field does not have access to the initial value"""
        return self.initial["password"]


class UploadFileForm(forms.Form):
    file  = forms.FileField()


class UserProfileForm(ModelForm):

##    INSTRUMENT_CHOICES = (
##            ('BASS', 'Bass'),
##            ('DRUMS', 'Drums'),
##            ('GUITAR', 'Guitar'),
##            ('VOCALS', 'Vocals')
##    )
##    Instrument = forms.MultipleChoiceField(choices=INSTRUMENT_CHOICES, widget=forms.CheckboxSelectMultiple(), required=True)
##
##    GENRE = (
##        ('CLASSICAL', 'Classical'),
##        ('JAZZ', 'Jazz'),
##        ('HIP-HOP', 'Hip-Hop'),
##        ('FUNK', 'Funk'),
##        ('CONTEMPORARY','Contemporary')
##
##    )
##    Genre = forms.MultipleChoiceField(choices=GENRE, widget=forms.CheckboxSelectMultiple(), required=True)
    instruments = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(), queryset=Instrument.objects.all(), required=True)
    genres = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(), queryset=Genre.objects.all(), required=True)
    class Meta:
        model = UserProfile
        fields = ('display_name', 'years_of_experience', 'favorite_musician', 'instruments', 'genres')


##    def __init__(self, readonly_form=False, *args, **kwargs):
##            super(UserProfileForm, self).__init__(*args, **kwargs)
##            if readonly_form:
##                for field in self.fields:
##                    self.fields[field].widget.attrs['readonly'] = True
##



