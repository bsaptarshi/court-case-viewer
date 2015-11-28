from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from cases.models import Cases, Court, CasesDay, COURT_CHOICES, CaseRelated
from home.models import Judge, Lawyers, LAWYER_CHOICES, JUDGE_CHOICES
import json, datetime, re
import ast
# Create your views here.
@csrf_exempt 
def webScraping(request):    
    if request.method=="POST":
        #data =  json.loads(request.body)
        #print data
        court_no = None
        todaysDate = None
        data = request.body              
        data = data.replace("<br>"," ")
        data = data.replace("</br>"," ")        
        data = ast.literal_eval(data)
      
        for k,v in data.items():  
                
            if k == "date":
                todaysDate = datetime.datetime.strptime(v, "%d-%m-%Y").date()
            if k == "courts":                         
                for key,court_cases in v.items():                                                 
                    for court1 in court_cases:  
                        judgeList = []       
                        for key1,court in court1.items():    
                                                                                      
                            if key1=="judge":
                                
                                for c in court.split("HON'BLE MR. JUSTICE"):
                                    judgeObject = createJudge( createJudgeUSer(c))
                                    judgeObject.save()
                                    judgeList.append(judgeObject)
                               
                            if key1=="court_no":                                                      
                                court_no =  court                        
                                try:
                                    courtObject = Court.objects.get(number = court_no,type =COURT_CHOICES[0][0])    
                                except ObjectDoesNotExist:
                                    courtObject = Court.objects.create(number = court_no,type =COURT_CHOICES[0][0]) 
                            if key1=="cases":    
                                prevSerial = None
                                prevPrimaryCase = None
                                for case in court['case']:   
                                                                                        
                                    serial =  case['serial']
                                    case_no =  case['case_no']
                                    petitionar_advocates = []
                                    respondent_advocates = []
                                    petionar = []
                                    respondant = []
                                    
                                    for p in case['petitionar_advocates']:    
                                        petitionar_advocates.append(createLawyer(createUser(p)))
                                    for p in case['party'].split("Vs.")[0].split("&"):                                   
                                        petionar.append(createUser(p))                                    
                                    for p in case['party'].split("Vs.")[1].split("&"):
                                        respondant.append(createUser(p))                                                                    
                                    for r in case['respondent_advocates']:
                                        respondent_advocates.append(createLawyer(createUser(r)))
                                    
                                    try:
                                        caseObject =   Cases.objects.get(name = case_no)
                                    except:
                                        caseObject =   Cases.objects.create(name = case_no)                                
                                    for p  in  petitionar_advocates:
                                        if p not in caseObject.defense_lawyers.all():
                                            caseObject.defense_lawyers.add(p)
                                    for p  in  respondent_advocates:
                                        if p not in caseObject.respondant_lawyers.all():
                                            caseObject.respondant_lawyers.add(p)
                                    for p  in  petionar:
                                        if p not in caseObject.defendent.all():
                                            caseObject.defendent.add(p)
                                    for p  in  respondant:
                                        if p not in caseObject.respondant.all():
                                            caseObject.respondant.add(p)
                                    caseObject.save()
                                                                                       
                            
                        
                                    try:
                                        caseDay  = CasesDay.objects.get(court = courtObject,serial = serial,date = todaysDate, case = caseObject)
                                    except:
                                        serial = re.findall(r'\d+',serial)[0]
                                        caseDay  = CasesDay.objects.create(court = courtObject,serial = int(serial),date = todaysDate, case = caseObject)
                                    
                                    for j in judgeList:
                                        if j not in caseDay.judge.all():
                                            caseDay.judge.add(j)
                                        
                                    caseDay.save()
                                    if prevSerial==serial:
                                        if caseObject not in prevPrimaryCase.related_cases.all():
                                            prevPrimaryCase.related_cases.add(caseObject)
                                    else:
                                        prevPrimaryCase = CaseRelated.objects.create(primary_case = caseObject)
                                    prevSerial = serial
        return  HttpResponse("akash")


def createUser(p):
    username = p 
    p = p.strip().split(" ")      
    try:
        pet = User.objects.get(username = username)
    except ObjectDoesNotExist:
           
        if len(p) ==2 :
            pet = User.objects.create(username = username, first_name = p[0], last_name = p[1])      
        elif len(p) ==3 :
            pet = User.objects.create(username = username, first_name = p[0]+" "+p[1], last_name = p[2])
        else:
            pet = User.objects.create(username = username)   
        pet.save()
        pet.set_unusable_password() 
        pet.save()
    return pet
def createJudgeUSer(p):
    username = "HON'BLE MR. JUSTICE "+p 
    p = p.strip().split(" ")      
    try:
        pet = User.objects.get(username = username)
    except ObjectDoesNotExist:
           
        if len(p) ==2 :
            pet = User.objects.create(username = username, first_name = p[0], last_name = p[1])      
        elif len(p) ==3 :
            pet = User.objects.create(username = username, first_name = p[0]+" "+p[1], last_name = p[2])
        else:
            pet = User.objects.create(username = username)   
        pet.save()
        pet.set_unusable_password() 
        pet.save()
    return pet

    
def createLawyer(userObject):
    try:
        lawyer = Lawyers.objects.get(user = userObject)
    except ObjectDoesNotExist:
        lawyer = Lawyers.objects.create(user = userObject,type = LAWYER_CHOICES[0][0])
        lawyer.save()
    return lawyer 

def createJudge(userObject):
    try:
        judge = Judge.objects.get(user = userObject)
    except:
        judge = Judge.objects.create(user = userObject, type = JUDGE_CHOICES[0][0])
    return judge
