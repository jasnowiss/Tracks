"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from Tracks.models import *

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class UserProfileTest(TestCase):



class TrackTest(TestCase):



class CollaborationTest(TestCase):


"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from Tracks.models import *

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class UserProfileTest(TestCase):



class TrackTest(TestCase):



class CollaborationTest(TestCase):
	


class UploadFileTest(TestCase):

	def test_valid_mp3_upload(self):
		filepathOfMp3 = '~/user_mp3_files/valid.mp3'
		#make a request with this file path
		request = 
		self.assertEqual(self.upload_mp3(request), 'success')

		#then check if the file exists and is identical
		self.assertEqual(getFileFromDatabase, file(filepathOfMp3))


	def test_invalid_file_extension(self):
		filepathOfMp3 = '~/user_mp3_files/badExt.ogg'
		#make a request with this file path
		request = 
		self.assertEqual(self.upload_mp3(request), 'File extension not supported')		


	def test_sizeLimitExceeded_file(self):
		filepathOfMp3 = '~/user_mp3_files/long.mp3'
		#make a request with this file path
		request = 
		self.assertEqual(self.upload_mp3(request), 'File exceeding size limit')


	def test_null_name(self):
		filepathOfMp3 = '~/user_mp3_files/ .mp3'
		#make a request with this file path
		request = 
		self.assertEqual(self.upload_mp3(request), 'form not valid')

	def test_filenameTooLong_file(self):
		filepathOfMp3 = '~/user_mp3_files/qweirouqwepiorqwpjfslfj asjkdfhsjkfhiwqehr quiwerh qwiuerh qwuier hqwuierh qwic vhmc hvmc hvcm hv qweruqiwerhqwouiehfskvnkjsadfbkjsadfhjsfhsjkdf wqierhwiuerhqwuierhw uifahsd fuahsdfiu sfhuiasd fhuiasdfhuiasd fhisahfisd fhuias dfhiasf iasdfaidfsadfhasd.mp3'
		request = 
		self.assertEqual(self.upload_mp3(request), 'form not valid')
	
	def test_invalidChars_file(self):
		filepathOfMp3 = '~/user_mp3_files/@#ds!fd.mp3'
		#make a request with this file path
		request = 
		self.assertEqual(self.upload_mp3(request), 'form not valid')
