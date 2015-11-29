from django.test import TestCase, Client
from tastypie.test import ResourceTestCase
from django.contrib.auth.models import User

import json

# Create your tests here.
class HomeTests(TestCase):
    fixtures = ['fixtures.json']
    
    def setUp(self):
        super(HomeTests, self).setUp()
        print "SETTING UP?"
        self.user_name = "admin"
        self.password = "admin"

        
    def tearDown(self):
        super(HomeTests, self).tearDown()
        print "Tear Down"
    
      
    def test_register_user(self):
        member1 = Client()
        json_data = json.dumps({'username':'test','password':'test','email':'test@b.com'})        
        response = member1.post("/home/api/user/",json_data, content_type="application/json")
        self.assertTrue(response.status_code == 201)  
        testUser = User.objects.last()        
        self.assertTrue(testUser.username == "test")  
    
    def test_register_login(self):
        member1 = Client()
        json_data = json.dumps({'username':'test','password':'test','email':'test@b.com'})        
        response = member1.post("/home/api/user/",json_data, content_type="application/json")
        self.assertTrue(response.status_code == 201)             
        response = member1.post("/home/login/",json_data,content_type="application/json",**{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertTrue(response.status_code == 200) 
    
    def test_register_invalid_login(self):
        member1 = Client()
        json_data = json.dumps({'username':'test','password':'test','email':'test@b.com'})                            
        response = member1.post("/home/login/",json_data,content_type="application/json",**{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertTrue(response.status_code == 404) 
        
    def test_register_user_same_username(self):
        member1 = Client()
        json_data = json.dumps({'username':'test','password':'test','email':'test@b.com'})        
        response = member1.post("/home/api/user/",json_data, content_type="application/json")
        self.assertTrue(response.status_code == 201)  
        testUser = User.objects.last()        
        self.assertTrue(testUser.username == "test") 
        json_data = json.dumps({'username':'test','password':'test','email':'test@b.com'})        
        response = member1.post("/home/api/user/",json_data, content_type="application/json") 
        self.assertTrue(response.status_code == 400) 
        
    def test_logout(self):
        member1 = Client()
        json_data = json.dumps({'username':'test','password':'test','email':'test@b.com'})        
        response = member1.post("/home/api/user/",json_data, content_type="application/json")
        self.assertTrue(response.status_code == 201)             
        response = member1.post("/home/login/",json_data,content_type="application/json",**{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertTrue(response.status_code == 200)
        response = member1.post("/home/logout/")
        self.assertTrue(response.status_code == 200)
    
    def test_logout_invalid(self):
        member1 = Client()
        json_data = json.dumps({'username':'test','password':'test','email':'test@b.com'})        
        response = member1.post("/home/api/user/",json_data, content_type="application/json")
        self.assertTrue(response.status_code == 201)             
        response = member1.post("/home/login/",json_data,content_type="application/json",**{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertTrue(response.status_code == 200)
        response = member1.post("/home/logout/")
        self.assertTrue(response.status_code == 200)
        response = member1.post("/home/logout/")
        self.assertTrue(response.status_code == 404)
        


class UserResourceTest(ResourceTestCase):
    # Use ``fixtures`` & ``urls`` as normal. See Django's ``TestCase``
    # documentation for the gory details.
    fixtures = ['fixtures.json']

    def setUp(self):
        super(UserResourceTest, self).setUp()

        # Create a user.
        self.username = 'daniel'
        self.password = 'pass'
        self.user = User.objects.create_user(self.username, 'daniel@example.com', self.password)
        self.detail_url = '/home/api/user/'
      
    def get_credentials(self):
        return self.create_basic(username=self.username, password=self.password)


    def test_get_list_xml(self):
        self.assertValidXMLResponse(self.api_client.get(self.detail_url, format='xml', authentication=self.get_credentials()))

    def test_get_detail_json(self):
        resp = self.api_client.get(self.detail_url, format='json', authentication=self.get_credentials())
        self.assertValidJSONResponse(resp)
    
    def test_get_detail_xml(self):
        self.assertValidXMLResponse(self.api_client.get(self.detail_url, format='xml', authentication=self.get_credentials()))
        
class JudgeResourceTest(ResourceTestCase):
    # Use ``fixtures`` & ``urls`` as normal. See Django's ``TestCase``
    # documentation for the gory details.
    fixtures = ['fixtures.json']

    def setUp(self):
        super(JudgeResourceTest, self).setUp()

        # Create a user.
        self.username = 'daniel'
        self.password = 'pass'
        self.user = User.objects.create_user(self.username, 'daniel@example.com', self.password)
        self.detail_url = '/home/api/judge/'
      
    def get_credentials(self):
        return self.create_basic(username=self.username, password=self.password)


    def test_get_list_xml(self):
        self.assertValidXMLResponse(self.api_client.get(self.detail_url, format='xml', authentication=self.get_credentials()))

    def test_get_detail_json(self):
        resp = self.api_client.get(self.detail_url, format='json', authentication=self.get_credentials())
        self.assertValidJSONResponse(resp)
    
    def test_get_detail_xml(self):
        self.assertValidXMLResponse(self.api_client.get(self.detail_url, format='xml', authentication=self.get_credentials()))
        
class LawyersResourceTest(ResourceTestCase):
    # Use ``fixtures`` & ``urls`` as normal. See Django's ``TestCase``
    # documentation for the gory details.
    fixtures = ['fixtures.json']

    def setUp(self):
        super(LawyersResourceTest, self).setUp()

        # Create a user.
        self.username = 'daniel'
        self.password = 'pass'
        self.user = User.objects.create_user(self.username, 'daniel@example.com', self.password)
        self.detail_url = '/home/api/lawyers/'
      
    def get_credentials(self):
        return self.create_basic(username=self.username, password=self.password)


    def test_get_list_xml(self):
        self.assertValidXMLResponse(self.api_client.get(self.detail_url, format='xml', authentication=self.get_credentials()))

    def test_get_detail_json(self):
        resp = self.api_client.get(self.detail_url, format='json', authentication=self.get_credentials())
        self.assertValidJSONResponse(resp)
    
    def test_get_detail_xml(self):
        self.assertValidXMLResponse(self.api_client.get(self.detail_url, format='xml', authentication=self.get_credentials()))