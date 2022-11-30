from django.shortcuts import render, HttpResponse
from .models import *
import pandas as pd

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
    if (request.method == 'POST'):
        user = User()
        user.first_name = request.POST.get('fname')
        user.last_name = request.POST.get('lname')
        user.phone = request.POST.get('phone')
        user.email = request.POST.get('email')
        user.save()

        patient = Patient()
        patient.patient = User.objects.get(first_name = request.POST.get('fname'), last_name = request.POST.get('lname'), phone = request.POST.get('phone'), email = request.POST.get('email'))
        patient.age = request.POST.get('age')
        patient.height = request.POST.get('height')
        patient.weight = request.POST.get('weight')
        patient.sex = request.POST.get('sex')
        patient.diagnosis = request.POST.get('diagnosis')
        patient.diagnosis_date = request.POST.get('diagnosis_date')
        patient.birthday = request.POST.get('bday')
        patient.save()

        login = Patient_Login()
        login.username = request.POST.get('username')
        login.password = request.POST.get('password')
        login.save()


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
    mg_nutrients = Nutrient.objects.filter(units='mg', frequency='daily')

    context = {
        'mg_nutrients': mg_nutrients
    }

    return render(request, 'client_app/mydashboard.html', context)

def myProfileView(request):
    return render(request, 'client_app/myprofile.html')

def myCommunityView(request):
    return render(request, 'client_app/mycommunity.html')