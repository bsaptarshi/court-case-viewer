from django.contrib import admin
from cases.models import Court, CaseFilter, CaseSearch, Cases
# Register your models here.

admin.site.register(Court)
admin.site.register(CaseFilter)
admin.site.register(CaseSearch)
admin.site.register(Cases)