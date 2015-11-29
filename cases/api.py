from cases.models import Cases, CaseFilter, CaseSearch, Court, CasesDay, CaseRelated
from home.api import UserResources, LawyersResources
from lawCalender.utils import urlencodeSerializer

from tastypie.resources import ModelResource, ALL,ALL_WITH_RELATIONS
from tastypie.authorization import Authorization
from tastypie.authentication import Authentication
from tastypie import fields



class CasesResources(ModelResource):  
    defense_lawyers = fields.ToManyField(LawyersResources, 'defense_lawyers',related_name="defense_lawyers_user",  full=True, null=True, blank=True)
    respondant_lawyers = fields.ToManyField(LawyersResources, 'respondant_lawyers', related_name="respondant_lawyers_user",full=True, null=True, blank=True)     
    defendent = fields.ToManyField(UserResources, 'defendent',related_name="defendent_user", full=True, null=True, blank=True)
    respondant = fields.ToManyField(UserResources, 'respondant', related_name="respondant_user", full=True, null=True, blank=True)
    class Meta:
        queryset = Cases.objects.filter()
        resource_name = 'cases'
        authorization = Authorization()
        authentication = Authentication()
        excludes = [ 'datetime']
        allowed_methods = ['get','post','put','patch']
        serializer = urlencodeSerializer()
        always_return_data = True
        filtering = {}       
        for field in Cases.__dict__['_meta'].fields:        
            filtering.update({field.name : ALL_WITH_RELATIONS})
        
        
        
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
        filtering = {}
        for field in CaseSearch.__dict__['_meta'].fields:
            filtering.update({field.name : ALL_WITH_RELATIONS})
        
class CaseFilterResources(ModelResource):
    search = fields.ForeignKey(CaseSearchResources, 'search',full=True)
    class Meta:
        queryset = CaseFilter.objects.filter()
        resource_name = 'casefilter'
        authorization = Authorization()
        authentication = Authentication()
        excludes = [ 'datetime']
        allowed_methods = ['get','post','put','patch']
        serializer = urlencodeSerializer()
        always_return_data = True
        filtering = {}
        for field in CaseFilter.__dict__['_meta'].fields:
            filtering.update({field.name : ALL_WITH_RELATIONS})
        
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
        filtering = {}
        for field in Court.__dict__['_meta'].fields:
            filtering.update({field.name : ALL_WITH_RELATIONS})

class CasesDayResources(ModelResource):
    case = fields.ForeignKey(CasesResources, 'case',full=True)
    court = fields.ForeignKey(CourtResources, 'court',full=True)
    class Meta:
        queryset = CasesDay.objects.all()
        resource_name = 'caseday'
        authorization = Authorization()
        authentication = Authentication()
        excludes = [ 'datetime']
        allowed_methods = ['get','post','put','patch']
        serializer = urlencodeSerializer()
        always_return_data = True
        filtering = {}
        for field in CasesDay.__dict__['_meta'].fields:
            filtering.update({field.name : ALL_WITH_RELATIONS})
            

class CaseRelatedResources(ModelResource):
    primary_case = fields.ForeignKey(CasesResources, 'primary_case',full= True)
    class Meta:
        queryset = CaseRelated.objects.filter()
        resource_name = 'caserelated'
        authorization = Authorization()
        authentication = Authentication()
        excludes = [ 'datetime']
        allowed_methods = ['get','post','put','patch']
        serializer = urlencodeSerializer()
        always_return_data = True
        filtering = {}
        for field in CaseRelated.__dict__['_meta'].fields:
            filtering.update({field.name : ALL_WITH_RELATIONS})
            
            
            
            
            
            
            
            
            
            
            
            
            