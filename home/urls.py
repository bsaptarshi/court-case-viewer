from django.conf.urls import include, url,patterns
from home.api import JudgeResources, LawyersResources, UserProfileResources

tasks_resource = JudgeResources()
laywer_resource = LawyersResources()
user_profile_resource = UserProfileResources()


urlpatterns = patterns('home.views',
    # Examples:
   #url(r'^$', 'home'),
    url(r'^api/judge/', include(tasks_resource.urls)), 
     url(r'^api/lawyers/', include(laywer_resource.urls)), 
      url(r'^api/userprofile/', include(user_profile_resource.urls)), 
    
    
   #  url(r'^$', include('home.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     #url(r'^admin/', include(admin.site.urls)),
)