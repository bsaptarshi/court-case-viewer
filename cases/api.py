from cases.models import Cases, CaseFilter, CaseSearch, Court
from home.api import UserResources
from lawCalender.utils import urlencodeSerializer

from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie.authentication import Authentication
from tastypie import fields


class CasesResources(ModelResource):
    defendent = fields.ForeignKey(UserResources, 'defendent')
    respondant = fields.ForeignKey(UserResources, 'respondant')
    defense_lawyers = fields.ForeignKey(UserResources, 'defense_lawyers')
    respondant_lawyers = fields.ForeignKey(UserResources, 'respondant_lawyers')
    class Meta:
        queryset = Cases.objects.filter()
        resource_name = 'cases'
        authorization = Authorization()
        authentication = Authentication()
        excludes = [ 'datetime']
        allowed_methods = ['get','post','put','patch']
        serializer = urlencodeSerializer()
        always_return_data = True
        
class CaseSearchResources(ModelResource):
    user = fields.ForeignKey(UserResources, 'user')
    class Meta:
        queryset = CaseSearch.objects.filter()
        resource_name = 'casesearch'
        authorization = Authorization()
        authentication = Authentication()
        excludes = [ 'datetime']
        allowed_methods = ['get','post','put','patch']
        serializer = urlencodeSerializer()
        always_return_data = True
        
class CaseFilterResources(ModelResource):
    search = fields.ForeignKey(CaseSearchResources, 'search')
    class Meta:
        queryset = CaseFilter.objects.filter()
        resource_name = 'casefilter'
        authorization = Authorization()
        authentication = Authentication()
        excludes = [ 'datetime']
        allowed_methods = ['get','post','put','patch']
        serializer = urlencodeSerializer()
        always_return_data = True
        
class CourtResources(ModelResource):
    class Meta:
        queryset = Court.objects.filter()
        resource_name = 'court'
        authorization = Authorization()
        authentication = Authentication()
        excludes = [ 'datetime']
        allowed_methods = ['get','post','put','patch']
        serializer = urlencodeSerializer()
        always_return_data = True