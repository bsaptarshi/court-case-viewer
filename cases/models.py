from django.db import models
from home.models import User,Lawyers,Judge
# Create your models here.
class Court(models.Model):
    type = models.CharField(max_length = 200)
    number = models.IntegerField()
    location = models.TextField()

class CaseSearch(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length = 200)
    datetime = models.DateTimeField(auto_now_add = True)
    
class Cases(models.Model):
    name = models.CharField(max_length = 200)
    details = models.TextField()
    type = models.CharField(max_length = 200)
    court = models.ForeignKey(Court)
    defendent = models.ForeignKey(User,related_name="defendent_user")
    respondant = models.ForeignKey(User,related_name="respondant_user")
    judge = models.ForeignKey(Judge)
    defense_lawyers = models.ForeignKey(Lawyers,related_name="defense")
    respondant_lawyers = models.ForeignKey(Lawyers,related_name = "respondant")

class CaseFilter(models.Model):
    search = models.ForeignKey(CaseSearch)
    field = models.CharField(max_length = 200)
    criteria = models.CharField(max_length = 200)
    
    
    
    