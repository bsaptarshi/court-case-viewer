from django.shortcuts import render
from lawCalender.webscrapping import scrapehelper

# Create your views here.


def home(request):
    return scrapehelper()