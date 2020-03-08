from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    return HttpResponse('<h1>home<h1/>')

def stats(request):
    return HttpResponse('<h1>stats<h1/>')

def rules(request):
    return HttpResponse('<h1>rules<h1/>')
