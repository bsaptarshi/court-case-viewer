from django.conf.urls import include, url,patterns
from cases.api import CaseFilterResources, CaseSearchResources, CourtResources, CasesResources

case_filter_resource = CaseFilterResources()
case_search_resource = CaseSearchResources()
court_resource = CourtResources()
case_resource = CasesResources()

urlpatterns = patterns('home.views',
    # Examples:
   
    url(r'^api/', include(case_filter_resource.urls)), 
    url(r'^api/', include(case_search_resource.urls)), 
    url(r'^api/', include(court_resource.urls)), 
    url(r'^api/', include(case_resource.urls)), 
    
    
   #  url(r'^$', include('home.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     #url(r'^admin/', include(admin.site.urls)),
)