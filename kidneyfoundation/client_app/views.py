from django.shortcuts import render, HttpResponse
from .models import *

# Create your views here.
def indexPageView(request) :
    nutrients = Nutrient.objects.filter(frequency = 'daily').order_by('name')

    context = {
        'nutrients': nutrients
    }

    return render(request, 'client_app/index.html', context)

def loginPageView(request) :
    return render(request, 'client_app/login.html')

def newAccountPageView(request) :
    return render(request, 'client_app/new_user.html')

def myMenuView(request):
    return render(request, 'client_app/mymenu.html')
    
def myMenuAdd(request):
    return render(request, 'client_app/addfoods.html')

def myFoodJournalView(request):
    return render(request, 'client_app/myfoodjournal.html')

def myFoodJournalAdd(request):
    return render(request, 'client_app/addjournalentry.html')

def myDashboardView(request):
    return render(request, 'client_app/mydashboard.html')