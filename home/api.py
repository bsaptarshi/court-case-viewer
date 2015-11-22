from lawCalender.utils import urlencodeSerializer
from home.models import Judge, Lawyers, UserProfile

from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie.authentication import Authentication


class JudgeResources(ModelResource):
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
    class Meta:
        queryset = Lawyers.objects.filter()
        resource_name = 'lawyers'
        authorization = Authorization()
        authentication = Authentication()
        excludes = [ 'datetime']
        allowed_methods = ['get','post','put','patch']
        serializer = urlencodeSerializer()
        always_return_data = True

class UserProfileResources(ModelResource):
    class Meta:
        queryset = UserProfile.objects.filter()
        resource_name = 'userprofile'
        authorization = Authorization()
        authentication = Authentication()
        excludes = [ 'datetime']
        allowed_methods = ['get','post','put','patch']
        serializer = urlencodeSerializer()
        always_return_data = True 
