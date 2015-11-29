from django.test import TestCase, Client
from tastypie.test import ResourceTestCase
from django.contrib.auth.models import User
import json, os, ast

from cases.models import Cases, CasesDay
# Create your tests here.

file_path =  os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/cases/"

class WebScrapingCodeTest(TestCase):
    #fixtures = ['fixtures.json']

    def setUp(self):
        super(WebScrapingCodeTest, self).setUp()
        self.member = Client()
        # Create a user.
        self.username = 'daniel'
        self.password = 'pass'
        self.user = User.objects.create_user(self.username, 'daniel@example.com', self.password)
        self.detail_url = '/cases/scrape/'
    def testWebScraping(self):
        json_data = json.load(open(file_path+"json_sample"))
        json_data =  ast.literal_eval(json.dumps(json_data))  
        
        self.assertTrue(User.objects.all().count()==1)              
        self.assertTrue(Cases.objects.all().count()==0)
        self.assertTrue(CasesDay.objects.all().count()==0)
        response = self.member.post(self.detail_url,json_data,content_type="application/json")    
        self.assertTrue(response.status_code==200) 
        self.assertTrue(Cases.objects.all().count()==4)
        self.assertTrue(User.objects.all().count()==15)
        self.assertTrue(CasesDay.objects.all().count()==5)


class CasesTest(TestCase):
    fixtures = ['fixtures.json']
    
    
    def setUp(self):
        print "SETTING UP?"
        self.user_name = "admin"
        self.password = "admin"
        self.member1 = Client()
        self.member1.login(username=self.user_name,password=self.password)
    def tearDown(self):
        print "Tear Down"
        
    def test_cases_for_a_day(self):
        
        date = "2015-11-24"
        json_data = {'date':date,"limit":10}
        response = self.member1.get('/cases/api/caseday/?format=json', json_data, content_type="application/json")        
        self.assertTrue(response.status_code == 200)  
        
    def test_cases_for_a_day_invalid_date(self):
       
        date = "2015/11/24" 
        json_data = {'date':date,"limit":10}
        response = self.member1.get('/cases/api/caseday/?format=json', json_data, content_type="application/json")                
        self.assertTrue(response.status_code == 400)  
    
    def test_cases_for_a_day_limit(self):
        
        date = "2015-11-24"
        limit = 10
        json_data = {'date':date,"limit":limit}
        response = self.member1.get('/cases/api/caseday/?format=json', json_data, content_type="application/json")       
        self.assertTrue(response.status_code == 200)  
        json_data =  json.loads(response.content)                 
        self.assertTrue(len(json_data['objects']) <= limit) 
        
    def test_cases_for_a_day_case_no(self):
       
        case_no = "C.A. No. 2884/2006"
        limit = 10
        json_data = {'case__name':case_no,"limit":limit}
        response = self.member1.get('/cases/api/caseday/?format=json', json_data, content_type="application/json")       
        json_data =  json.loads(response.content)                         
        self.assertTrue(len(json_data['objects']) >= 0) 
        self.assertTrue(response.status_code == 200)
        
    def test_cases_for_a_day_case_no_invalid(self):
       
        case_no = "fsfsadfsadf"
        limit = 10
        json_data = {'case__name':case_no,"limit":limit}
        response = self.member1.get('/cases/api/caseday/?format=json', json_data, content_type="application/json")       
        json_data =  json.loads(response.content)           
        self.assertTrue(len(json_data['objects']) == 0)  
             
    def test_cases_for_a_day_court_no(self):
        
        court_number = "10"
        limit = 10
        json_data = {'court__number':court_number,"limit":limit}
        response = self.member1.get('/cases/api/caseday/?format=json', json_data, content_type="application/json")       
        json_data =  json.loads(response.content)                         
        self.assertTrue(len(json_data['objects']) >= 0) 
        self.assertTrue(response.status_code == 200) 
        
    def test_cases_for_a_day_court_no_invalid(self):
      
        court_number = "100"
        limit = 10
        json_data = {'court__number':court_number,"limit":limit}
        response = self.member1.get('/cases/api/caseday/?format=json', json_data, content_type="application/json")       
        json_data =  json.loads(response.content)                         
        self.assertTrue(len(json_data['objects']) == 0) 
        self.assertTrue(response.status_code == 200)


    
    
class CasesResourceTest(ResourceTestCase):
    # Use ``fixtures`` & ``urls`` as normal. See Django's ``TestCase``
    # documentation for the gory details.
    fixtures = ['fixtures.json']

    def setUp(self):
        super(CasesResourceTest, self).setUp()

        # Create a user.
        self.username = 'daniel'
        self.password = 'pass'
        self.user = User.objects.create_user(self.username, 'daniel@example.com', self.password)
        self.detail_url = '/cases/api/cases/'
    def tearDown(self):
        print "Tear Down"
    def get_credentials(self):
        return self.create_basic(username=self.username, password=self.password)


    def test_get_list_xml(self):
        self.assertValidXMLResponse(self.api_client.get('/cases/api/cases/', format='xml', authentication=self.get_credentials()))
    def test_get_detail_json(self):
        resp = self.api_client.get(self.detail_url, format='json', authentication=self.get_credentials())
        self.assertValidJSONResponse(resp)

    
    def test_get_detail_xml(self):
        self.assertValidXMLResponse(self.api_client.get(self.detail_url, format='xml', authentication=self.get_credentials()))
        
        
        
class CasesDayResourceTest(ResourceTestCase):
    # Use ``fixtures`` & ``urls`` as normal. See Django's ``TestCase``
    # documentation for the gory details.
    fixtures = ['fixtures.json']

    def setUp(self):
        super(CasesDayResourceTest, self).setUp()

        # Create a user.
        self.username = 'daniel'
        self.password = 'pass'
        self.user = User.objects.create_user(self.username, 'daniel@example.com', self.password)
        self.detail_url = '/cases/api/caseday/'
    def tearDown(self):
        print "Tear Down"
    def get_credentials(self):
        return self.create_basic(username=self.username, password=self.password)


    def test_get_list_xml(self):
        self.assertValidXMLResponse(self.api_client.get('/cases/api/caseday/', format='xml', authentication=self.get_credentials()))

    def test_get_detail_json(self):
        resp = self.api_client.get(self.detail_url, format='json', authentication=self.get_credentials())
        self.assertValidJSONResponse(resp)

    
    def test_get_detail_xml(self):
        self.assertValidXMLResponse(self.api_client.get(self.detail_url, format='xml', authentication=self.get_credentials()))
        
class CourtResourceTest(ResourceTestCase):
    # Use ``fixtures`` & ``urls`` as normal. See Django's ``TestCase``
    # documentation for the gory details.
    fixtures = ['fixtures.json']

    def setUp(self):
        super(CourtResourceTest, self).setUp()

        # Create a user.
        self.username = 'daniel'
        self.password = 'pass'
        self.user = User.objects.create_user(self.username, 'daniel@example.com', self.password)
        self.detail_url = '/cases/api/court/'
    def tearDown(self):
        print "Tear Down"
    def get_credentials(self):
        return self.create_basic(username=self.username, password=self.password)


    def test_get_list_xml(self):
        self.assertValidXMLResponse(self.api_client.get('/cases/api/court/', format='xml', authentication=self.get_credentials()))

    def test_get_detail_json(self):
        resp = self.api_client.get(self.detail_url, format='json', authentication=self.get_credentials())
        self.assertValidJSONResponse(resp)

    
    def test_get_detail_xml(self):
        self.assertValidXMLResponse(self.api_client.get(self.detail_url, format='xml', authentication=self.get_credentials()))
    


class CaseFilterResourceTest(ResourceTestCase):
    # Use ``fixtures`` & ``urls`` as normal. See Django's ``TestCase``
    # documentation for the gory details.
    fixtures = ['fixtures.json']

    def setUp(self):
        super(CaseFilterResourceTest, self).setUp()

        # Create a user.
        self.username = 'daniel'
        self.password = 'pass'
        self.user = User.objects.create_user(self.username, 'daniel@example.com', self.password)
        self.detail_url = '/cases/api/casefilter/'
      
    def get_credentials(self):
        return self.create_basic(username=self.username, password=self.password)


    def test_get_list_xml(self):
        self.assertValidXMLResponse(self.api_client.get(self.detail_url, format='xml', authentication=self.get_credentials()))

    def test_get_detail_json(self):
        resp = self.api_client.get(self.detail_url, format='json', authentication=self.get_credentials())
        self.assertValidJSONResponse(resp)

    
    def test_get_detail_xml(self):
        self.assertValidXMLResponse(self.api_client.get(self.detail_url, format='xml', authentication=self.get_credentials()))
        
class CaseSearchResourceTest(ResourceTestCase):
    # Use ``fixtures`` & ``urls`` as normal. See Django's ``TestCase``
    # documentation for the gory details.
    fixtures = ['fixtures.json']

    def setUp(self):
        super(CaseSearchResourceTest, self).setUp()

        # Create a user.
        self.username = 'daniel'
        self.password = 'pass'
        self.user = User.objects.create_user(self.username, 'daniel@example.com', self.password)
        self.detail_url = '/cases/api/casesearch/'
      
    def get_credentials(self):
        return self.create_basic(username=self.username, password=self.password)


    def test_get_list_xml(self):
        self.assertValidXMLResponse(self.api_client.get(self.detail_url, format='xml', authentication=self.get_credentials()))

    def test_get_detail_json(self):
        resp = self.api_client.get(self.detail_url, format='json', authentication=self.get_credentials())
        self.assertValidJSONResponse(resp)

    
    def test_get_detail_xml(self):
        self.assertValidXMLResponse(self.api_client.get(self.detail_url, format='xml', authentication=self.get_credentials()))
        
        
        
class CaseRelatedResourceTest(ResourceTestCase):
    # Use ``fixtures`` & ``urls`` as normal. See Django's ``TestCase``
    # documentation for the gory details.
    fixtures = ['fixtures.json']

    def setUp(self):
        super(CaseRelatedResourceTest, self).setUp()

        # Create a user.
        self.username = 'daniel'
        self.password = 'pass'
        self.user = User.objects.create_user(self.username, 'daniel@example.com', self.password)
        self.detail_url = '/cases/api/caserelated/'
      
    def get_credentials(self):
        return self.create_basic(username=self.username, password=self.password)


    def test_get_list_xml(self):
        self.assertValidXMLResponse(self.api_client.get(self.detail_url, format='xml', authentication=self.get_credentials()))

    def test_get_detail_json(self):
        resp = self.api_client.get(self.detail_url, format='json', authentication=self.get_credentials())
        self.assertValidJSONResponse(resp)

    
    def test_get_detail_xml(self):
        self.assertValidXMLResponse(self.api_client.get(self.detail_url, format='xml', authentication=self.get_credentials()))
