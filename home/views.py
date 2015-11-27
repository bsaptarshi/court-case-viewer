from django.contrib.auth import authenticate, login as django_login,logout as django_logout
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404
from django.shortcuts import HttpResponse



# Create your views here.
@csrf_exempt
def login(request):
    
    username = request.POST['username']
    password = request.POST['password']
   

    user = authenticate(username=username, password=password)
    if user is not None:   
       
        django_login(request, user)
        return HttpResponse({"Success":True})
    else:
        return Http404("User not found")

@csrf_exempt    
def logout(self, request):       
      
        if request.user and request.user.is_authenticated():           
            django_logout(request)
            return 
        return Http404("User not found")

