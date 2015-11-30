from django.conf.urls import include, url,patterns
from home.api import JudgeResources, LawyersResources, UserProfileResources,UserResources

tasks_resource = JudgeResources()
laywer_resource = LawyersResources()
user_profile_resource = UserProfileResources()
user_resource = UserResources()


urlpatterns = patterns('home.views',
    # Examples:
   #url(r'^$', 'home'),

    url(r'^login/','login'),
    url(r'^logout/','logout'),
    url(r'^api/', include(tasks_resource.urls)), 
    url(r'^api/', include(laywer_resource.urls)), 
    url(r'^api/', include(user_profile_resource.urls)), 
    url(r'^api/', include(user_resource.urls)),
    
    
   #  url(r'^$', include('home.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     #url(r'^admin/', include(admin.site.urls)),
)