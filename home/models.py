import uuid
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
# Create your models here.
def get_photo_storage_path(photo_obj, filename):         
    storage_path = 'img/'+str(uuid.uuid1())+"_"+filename
    return storage_path 

class UserProfile(models.Model):
    user = models.ForeignKey(User)
    image = models.ImageField(upload_to = get_photo_storage_path,null = True, blank =  True)
    about_me = models.TextField(null = True, blank =  True)
    details = models.TextField(null = True, blank =  True)    
    datetime = models.DateTimeField(auto_now_add = True)

JUDGE_CHOICES = (
    ("Supreme Court", "Supreme Court"),
)
    
class Judge(models.Model):
    user = models.ForeignKey(User)
    type = models.CharField(max_length = 200,choices = JUDGE_CHOICES)
    
LAWYER_CHOICES = (
    ("Supreme Court", "Supreme Court"),
)
    
class Lawyers(models.Model):
    user = models.ForeignKey(User)
    type = models.CharField(max_length = 200, choices = LAWYER_CHOICES)