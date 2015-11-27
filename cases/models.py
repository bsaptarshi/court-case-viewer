from django.db import models
from home.models import User,Lawyers,Judge
# Create your models here.
COURT_CHOICES = (
    ("Supreme Court", "Supreme Court"),
)
    
class Court(models.Model):
    type = models.CharField(max_length = 200, choices = COURT_CHOICES)
    number = models.IntegerField(null = True, blank = True)
    location = models.TextField(null = True, blank = True)

class CaseSearch(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length = 200, null = True, blank = True)
    datetime = models.DateTimeField(auto_now_add = True)
    
class Cases(models.Model):
    name = models.CharField(max_length = 200)
    details = models.TextField(null = True, blank = True)
    type = models.CharField(max_length = 200, null = True, blank = True)
    court = models.ForeignKey(Court)
    defense_lawyers = models.ManyToManyField(Lawyers,related_name="defense_lawyers_user",null = True, blank =  True)
    respondant_lawyers = models.ManyToManyField(Lawyers,related_name = "respondant_lawyers_user",null = True, blank =  True)
    defendent = models.ManyToManyField(User,related_name="defendent_user",null = True, blank =  True)
    respondant = models.ManyToManyField(User,related_name="respondant_user",null = True, blank =  True)
   
    judge = models.ForeignKey(Judge)
    

class CasesDay(models.Model):
    case = models.ForeignKey(Cases)
    serial = models.IntegerField()
    date = models.DateField()
    

class CaseFilter(models.Model):
    search = models.ForeignKey(CaseSearch)
    field = models.CharField(max_length = 200, null = True, blank = True)
    criteria = models.CharField(max_length = 200, null = True, blank = True)
    
class CaseRelated(models.Model):
    primary_case = models.ForeignKey(Cases)
    related_cases = models.ManyToManyField(Cases,related_name = "sub_cases", null = True, blank = True)