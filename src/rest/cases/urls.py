from django.conf.urls import include, url,patterns
from cases.api import CaseFilterResources, CaseSearchResources, CourtResources, CasesResources, CasesDayResources, CaseRelatedResources

case_filter_resource = CaseFilterResources()
case_search_resource = CaseSearchResources()
court_resource = CourtResources()
case_resource = CasesResources()
case_day_resource = CasesDayResources()
case_related_resource = CaseRelatedResources()
urlpatterns = patterns('cases.views',
    # Examples:
    url(r'^scrape/','webScraping'),
    url(r'^api/', include(case_filter_resource.urls)), 
    url(r'^api/', include(case_search_resource.urls)), 
    url(r'^api/', include(court_resource.urls)), 
    url(r'^api/', include(case_resource.urls)),
    url(r'^api/', include(case_related_resource.urls)),
    url(r'^api/', include(case_day_resource.urls)),
   #  url(r'^$', include('home.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     #url(r'^admin/', include(admin.site.urls)),
)