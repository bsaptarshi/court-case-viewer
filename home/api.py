from lawCalender.utils import urlencodeSerializer
from home.models import Judge, Lawyers, UserProfile


from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie.authentication import Authentication
from tastypie import fields

from django.contrib.auth.models import User
from django.db import IntegrityError

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
        filtering = {}
        for field in User.__dict__['_meta'].fields:
            filtering.update({field.name : ALL_WITH_RELATIONS})
    def obj_create(self, bundle, request=None, **kwargs):
        try:
            bundle = super(UserResources, self).obj_create(bundle)
            bundle.obj.set_password(bundle.data.get('password'))
            bundle.obj.save()
        except IntegrityError:
            raise BadRequest('Username already exists')

        return bundle
  

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
        filtering = {}
        for field in Judge.__dict__['_meta'].fields:
            filtering.update({field.name : ALL_WITH_RELATIONS})

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
        filtering = {}
        for field in Lawyers.__dict__['_meta'].fields:
            filtering.update({field.name : ALL_WITH_RELATIONS})
    

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
        filtering = {}
        for field in UserProfile.__dict__['_meta'].fields:
            filtering.update({field.name : ALL_WITH_RELATIONS})
