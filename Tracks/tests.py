"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase, Client
from Tracks.models import *
from selenium import webdriver

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

class GetTest(TestCase):
  def setUp(self):
    self.c = Client()

  def test_get_home(self):
    response = self.c.get('/Tracks/')
    self.assertEqual(response.status_code, 200)

  def test_get_register(self):
    response = self.c.get('/Tracks/register/')
    self.assertEqual(response.status_code, 200)

  def test_get_signin(self):
    response = self.c.get('/Tracks/signin')
    self.assertEqual(response.status_code, 200)

class SignUpTest(TestCase):
  def setUp(self):
    self.c = Client()
    response = self.c.post('/Tracks/register/',{'firstName':'a','lastName':'b','email':'a@a.a', 'password':'a', 'confirm':'a'}, follow=True)

  def test_new_user(self):
    response = self.c.post('/Tracks/register/',{'firstName':'a','lastName':'b','email':'b@b.b', 'password':'b', 'confirm':'b'})
    self.assertEqual(response.status_code, 302)

  def test_duplicate_email(self):
    a = 1
    try:
      response = self.c.post('/Tracks/register/',{'firstName':'c','lastName':'c','email':'a@a.a','password':'c','confirm':'b'},follow=True)
      print(response.status_code)
      print(response.redirect_chain)
    except:
      a = 0
    self.assertEqual(a, 0)
"""
  def test_bad_email(self):
    a = 0
    try:
      response = self.c.post('/Tracks/register/',{'firstName':'','lastName':'','email':'','password':'','confirm':''}, follow=True)
    except:
      a = 1
    print(response.status_code)
    print("redirect: " , response.redirect_chain)
    self.assertEqual(a,1)
"""
class SignInTest(TestCase):
  def setUp(self):
    self.c = Client()
    response = self.c.post('/Tracks/register/', {'firstName':'a','lastName':'a','email':'a@a.a','password':'a','confirm':'a'})

  def test_sign_in(self):
    response = self.c.post('/Tracks/signin/',{'email':'a@a.a','password':'a'})
    self.assertEqual(response.status_code, 302)
  def test_user_doesnt_exist(self):
    a = 0
    try:
      response = self.c.post('/Tracks/signin/',{'email':'z@z.z','password':'z'})
      a = response.templates[0].name
    except:
      a = '0'
    self.assertEqual(a, 'Tracks/signin.html')

  def test_wrong_passsword(self):
    a = 0
    try:
      response = self.c.post('/Tracks/signin/',{'email':'a@a.a','password':'1'})
      a = response.templates[0].name
    except:
      a = '0'
    self.assertEqual(a,'Tracks/signin.html')



class UserProfileTest(TestCase):
    def setUp(self):
        self.c = Client()
        response = self.c.post('/Tracks/register/', {'firstName':'a','lastName':'a','email':'a@a.a','password':'a','confirm':'a'})

    def test_going_to_user_profile(self):
        response = self.c.get('/Tracks/userprofile/')
        self.assertEqual(response.status_code, 302)

    def test_saving_data_to_user_profile(self):
        response = self.c.post('/Tracks/userprofile/', {'instrument':'guitar','field2' : 'test data', 'field3' : 'another test data', 'field4' : 'more test data'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.redirect_chain) != 0, True)

        response = self.c.post('/Tracks/userprofile/', {'instrument':'guitar','field2' : 'test data', 'field3' : 'another test data', 'field4' : 'more test data'}, follow=True)
        self.assertEqual(response.status_code, 200)


    def test_saving_empty_data(self):
        response = self.c.post('/Tracks/userprofile/', {'instrument':'','field2' : '', 'field3' : '', 'field4' : ''}, follow=True)
        self.assertEqual(response.status_code, 200)
"""
class UploadMusicTest(TestCase):
    def setUp(self):
        self.c = Client()
        response = self.c.post('/Tracks/register', {'firstName':'a','lastName':'a','email':'a@a.a','password':'a','confirm':'a'})
        response = self.c.post('/Tracks/signin', {'email':'a@a.a','password':'a'})

    def test_upload_file(self):
        response = self.c.post('/Tracks/userpage', {'file':'user_mp3_files/1_03-24-2014_03-57-18.mp3'})
        self.assertEqual(response.status_code, 200)
        response = self.c.get('/Tracks/userpage')
        self.assertContains(response, "user_mp3_files") #check that the file we uploaded is there

    def test_publish_collaboration(self):
        response = self.c.post('/Tracks/userpage', {'file':'../user_mp3_files/1_03-24-2014_.mp3'})
        response = self.c.get('/Tracks/finalize_collaboration/')
        self.assertNotEqual(response.status_code, 500)
"""
class LogoutTest(TestCase):
    def setUp(self):
        self.c = Client()
        response = self.c.post('/Tracks/register', {'firstName':'a','lastName':'a','email':'a@a.a','password':'a','confirm':'a'})
        response = self.c.post('/Tracks/signin', {'email':'a@a.a','password':'a'})

    def test_logout(self):
        response = self.c.get('/Tracks/logout')
        self.assertEqual(response.status_code, 302)
        response = self.c.get('Tracks/userprofile')
        self.assertNotEqual(response.status_code, 200)



class DownbeatTest(TestCase):
    def setUp(self):
        """
        Create user 'a'
        upload a track
        finalize the collaboration
        """
        self.c = Client()
        response = self.c.post('/Tracks/register', {'firstName':'a','lastName':'a','email':'a@a.a','password':'a','confirm':'a'})
        response = self.c.post('/Tracks/signin', {'email':'a@a.a','password':'a'})
        response = self.c.post('/Tracks/userpage', {'file':'../user_mp3_files/1_03-24-2014_03-57-18.mp3'})
        response = self.c.get('/Tracks/finalize_collaboration/')

    def test_downbeat(self):
        downbeat = self.c.get('/Tracks/downbeat')
        self.assertEqual(downbeat.status_code, 200)
        #self.assertContains(downbeat, "User a published this collaboration") #This should be what it actually says, fix this


class SearchTest(TestCase):

    def uploadtrack(file):
        temp_file = file
        temp_user, is_disabled = TracksUser.get_desired_user(get_session_for_user(request), None)
        server_filename, track_id, error = Track.handle_music_file_upload(temp_user, temp_file)
        if(error != None):
            response = HttpResponse(error)
            response.status_code = 400;
            return response
        response_data = {"server_filename" : server_filename, "track_id" : track_id}
        response = HttpResponse(json.dumps(response_data), content_type="application/json")
        response.status_code = 200;
        return response

    def setUp(self):
        self.c = Client()
        response = self.c.post('/Tracks/register', {'firstName':'george','lastName':'necula','email':'a@a.a','password':'a','confirm':'a'})
        response = self.c.post('/Tracks/signin', {'email':'a@a.a', 'password':'a'})
        #response = self.c.post('/Tracks/test')
        

    def test_search_user(self):
        response = self.c.get('/Tracks/search', {'search':'george'}, follow=True)
        self.assertContains(response, "User", status_code=200)

    def test_search_collaboration(self):
        response = self.c.get('/Tracks/search', {'search':'collab'}, follow=True)
        #self.assertContains(response, "Collaboration", status_code=200)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Search Results")

    def test_search_track(self):
        response = self.c.get('/Tracks/search', {'search':'raptor'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Search Results")
        #self.assertContains(response, "Track", status_code=200)

class GuiTest(TestCase):
    def setUp(self):
        self.driver = webdriver.Ie()

        self.driver.get('http://localhost:8000/Tracks/register')
        fname = self.driver.find_element_by_id('id_firstName')
        lname = self.driver.find_element_by_id('id_lastName')
        email = self.driver.find_element_by_id('id_email')
        pword = self.driver.find_element_by_id('id_password')
        confirm = self.driver.find_element_by_id('id_confirm')

        fname.send_keys("j")
        lname.send_keys("j")
        email.send_keys("j@j.com")
        pword.send_keys("j")
        confirm.send_keys("j")

        form = self.driver.find_element_by_id("signin")
        confirm.submit()

    """
    This class needs a teardown method added to it
    because selenium uses the local database, not a
    temporary one like the TestCase does. This means
    that tests which pass the first time may not pass
    the second time.

    A temporary work-around is to run
    "python manage.py flush"
    between tests.
    """

    
    def test_nav_bar_logged_out(self):
        self.driver.get('http://localhost:8000/Tracks')

        about_link = self.driver.find_element_by_id("about")
        about_link.click()
        self.assertEqual(self.driver.current_url,"http://localhost:8000/Tracks/about.html")

        tracks_home = self.driver.find_element_by_id("tracks_home")
        tracks_home.click()
        self.assertEqual(self.driver.current_url, "http://localhost:8000/Tracks/")

        downbeat = self.driver.find_element_by_id("downbeat")
        downbeat.click()
        self.assertEqual(self.driver.current_url, "http://localhost:8000/Tracks/signin/?next=/Tracks/downbeat/")

        self.driver.close()

    def test_register_gui(self):
        self.driver.get('http://localhost:8000/Tracks/register')
        fname = self.driver.find_element_by_id('id_firstName')
        lname = self.driver.find_element_by_id('id_lastName')
        email = self.driver.find_element_by_id('id_email')
        pword = self.driver.find_element_by_id('id_password')
        confirm = self.driver.find_element_by_id('id_confirm')

        fname.send_keys("g")
        lname.send_keys("n")
        email.send_keys("g@g.g")
        pword.send_keys("g")
        confirm.send_keys("g")

        form = self.driver.find_element_by_id("signin")
        confirm.submit()

        self.assertEqual(self.driver.current_url, "http://localhost:8000/Tracks/userpage")

        self.driver.close()
    
    def test_signin_and_upload_gui(self):
        self.driver.get('http://localhost:8000/Tracks/signin')
        email = self.driver.find_element_by_id("email")
        password = self.driver.find_element_by_id("password")
        """
        J is a test account in the database
        """
        email.send_keys("j@j.com")
        password.send_keys("j")
        password.submit()

        self.assertEqual(self.driver.current_url, "http://localhost:8000/Tracks/userpage/")

        upload = self.driver.find_element_by_id("id_file")
        import os
        cwd = os.getcwd()
        filepath = os.path.join(cwd, 'Tracks/user_mp3_files/').replace('/','\\')
        filepath = os.path.join(filepath, '1_03-24-2014_03-57-18.mp3').replace('/','\\')
        print(filepath)
        upload.send_keys(filepath)

        tracks_list = self.driver.find_element_by_id('tracks_list')
        was_track_uploaded = '1_03-24-2014_03-57-18.mp3' in tracks_list.text
        self.assertEqual(was_track_uploaded, True)

        self.driver.close()

    def test_nav_bar_logged_in(self):
        self.driver.get('http://localhost:8000/Tracks')
        
        profile_link = self.driver.find_element_by_id("profile")
        profile_link.click()
        self.assertEqual(self.driver.current_url, "http://localhost:8000/Tracks/userprofile/")

        collabs_link = self.driver.find_element_by_id("collab")
        collabs_link.click()
        self.assertEqual(self.driver.current_url,"http://localhost:8000/Tracks/userpage/")

        upload_link = self.driver.find_element_by_id("upload")
        upload_link.click()
        widget = self.driver.find_element_by_class_name("ui-dialog")
        self.assertNotEqual(widget, "")

        signout_link = self.driver.find_element_by_id("signout")
        signout_link.click()
        self.assertEqual(self.driver.current_url, "http://localhost:8000/Tracks/")

        collabs_link = self.driver.find_element_by_id("collab")
        collabs_link.click()
        self.assertEqual(self.driver.current_url,"http://localhost:8000/Tracks/signin/?next=/Tracks/userpage/")

        self.driver.close()

    def test_record(self):
        self.driver.get('http://localhost:8000/Tracks/userpage/')

        record_link = self.driver.find_element_by_id("record")
        record_link.click()
        self.assertEqual(self.driver.current_url, "http://localhost:8000/Tracks/record/")

        self.driver.close()








"""
class TrackTest(TestCase):
class CollaborationTest(TestCase):
class UploadFileTest(TestCase):
    def test_valid_mp3_upload(self):
        filepathOfMp3 = '~/user_mp3_files/valid.mp3'
        #make a request with this file path
        request = self.assertEqual(upload_mp3(request), 'success')
        #then check if the file exists and is identical
        self.assertEqual(getFileFromDatabase, file(filepathOfMp3))
    def test_invalid_file_extension(self):
        filepathOfMp3 = '~/user_mp3_files/badExt.ogg'
        #make a request with this file path
        request = self.assertEqual(self.upload_mp3(request), 'File extension not supported')


    def test_sizeLimitExceeded_file(self):
        filepathOfMp3 = '~/user_mp3_files/long.mp3'
        #make a request with this file path
        request = self.assertEqual(self.upload_mp3(request), 'File exceeding size limit')


    def test_null_name(self):
        filepathOfMp3 = '~/user_mp3_files/ .mp3'
        #make a request with this file path
        request = self.assertEqual(self.upload_mp3(request), 'form not valid')

    def test_filenameTooLong_file(self):
        filepathOfMp3 = '~/user_mp3_files/qweirouqwepiorqwpjfslfj asjkdfhsjkfhiwqehr quiwerh qwiuerh qwuier hqwuierh qwic vhmc hvmc hvcm hv qweruqiwerhqwouiehfskvnkjsadfbkjsadfhjsfhsjkdf wqierhwiuerhqwuierhw uifahsd fuahsdfiu sfhuiasd fhuiasdfhuiasd fhisahfisd fhuias dfhiasf iasdfaidfsadfhasd.mp3'
        request = self.assertEqual(self.upload_mp3(request), 'form not valid')

    def test_invalidChars_file(self):
        filepathOfMp3 = '~/user_mp3_files/@#ds!fd.mp3'
        #make a request with this file path
        request = self.assertEqual(self.upload_mp3(request), 'form not valid')
"""
