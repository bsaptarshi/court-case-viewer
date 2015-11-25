from django.contrib.auth import authenticate, login,logout as django_logout
from django.http import Http404
from home.models import Test



# Create your views here.

def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:        
        login(request, user)
        return 
    else:
        return Http404("User not found")
    
def logout(self, request):       
      
        if request.user and request.user.is_authenticated():           
            django_logout(request)
            return 
        return Http404("User not found")
    
def webScraping(request):
    Test.objects.create()
    return  