from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

from cases.models import Cases, Court, CasesDay, COURT_CHOICES
from home.models import Judge, Lawyers, UserProfile 
import json
# Create your views here.
@csrf_exempt 
def webScraping(request):    
    if request.method=="POST":
        data =  json.loads(request.body)
        court_no = None
        todaysDate = None
        for k,v in data.items():  
            if k == "date":
                todaysDate = v
            if k == "courts":                
                for key,court_cases in v.items():
                    for court in court_cases:                        
                        court_no =  court['court_no']   
                        try:
                            courtObject = Court.objects.get(number = court_no,type =COURT_CHOICES[0][0])    
                        except ObjectDoesNotExist:
                            courtObject = Court.objects.create(number = court_no,type =COURT_CHOICES[0][0])                
                        for value,cases in court['cases'].items():
                            for case in cases:                                
                                petitionar_advocates = case['petitionar_advocates']
                                for p in case['party'].split(".Vs.")[0].split("&"):
                                    if p!="ORS.":
                                        print p, "petionar"
                                for p in case['party'].split(".Vs.")[1].split("&"):
                                    if p!="ORS.":                                       
                                        print p, "respondant"
                                    
                                serial =  case['serial']
                                case_no =  case['case_no']
                                for r in case['respondent_advocates']:
                                    print r
                            
        return  "akash"