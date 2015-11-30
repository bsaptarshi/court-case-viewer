from django.contrib import admin
from home.models import UserProfile, Lawyers, Judge, Test
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Lawyers)
admin.site.register(Judge)
admin.site.register(Test)