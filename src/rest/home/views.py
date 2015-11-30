from django.contrib.auth import authenticate, login as django_login,logout as django_logout
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404
from django.shortcuts import HttpResponse
import json, ast


# Create your views here.
@csrf_exempt
def login(request):
    try:
        try:
            username = request.POST['username']
            password = request.POST['password']
        except:
            data =  ast.literal_eval(request.body)            
            username = data['username']
            password = data['password']             
        user = authenticate(username=username, password=password)
        if user is not None:              
            django_login(request, user)
            return HttpResponse({"Success":True})
    except:
        pass
    raise Http404("User not found")

@csrf_exempt    
def logout(request):       
      
        if request.user and request.user.is_authenticated():           
            django_logout(request)
            return HttpResponse({"Success":True})
        raise Http404("User already logged out")

