from lawCalender.utils import urlencodeSerializer
from home.models import Judge, Lawyers, UserProfile


from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie.authentication import Authentication
from tastypie import fields

from django.contrib.auth.models import User

class UserResources(ModelResource):
   
    class Meta:
        queryset = User.objects.filter()
        resource_name = 'user'
        authorization = Authorization()
        authentication = Authentication()
        excludes = [ 'datetime','password']
        allowed_methods = ['get','post','put','patch']
        serializer = urlencodeSerializer()
        always_return_data = True
  

class JudgeResources(ModelResource):
    user = fields.ForeignKey(UserResources, 'user',full = True)
    class Meta:
        queryset = Judge.objects.filter()
        resource_name = 'judge'
        authorization = Authorization()
        authentication = Authentication()
        excludes = [ 'datetime']
        allowed_methods = ['get','post','put','patch']
        serializer = urlencodeSerializer()
        always_return_data = True

class LawyersResources(ModelResource):    
    user = fields.ForeignKey(UserResources, 'user',full = True, null=True, blank=True)
    class Meta:
        queryset = Lawyers.objects.filter()
        resource_name = 'lawyers'
        authorization = Authorization()
        authentication = Authentication()        
        allowed_methods = ['get','post','put','patch']
        serializer = urlencodeSerializer()
        always_return_data = True
    

class UserProfileResources(ModelResource):
    user = fields.ForeignKey(UserResources, 'user',full = True)
    class Meta:
        queryset = UserProfile.objects.filter()
        resource_name = 'userprofile'
        authorization = Authorization()
        authentication = Authentication()
        excludes = [ 'datetime']
        allowed_methods = ['get','post','put','patch']
        serializer = urlencodeSerializer()
        always_return_data = True 
