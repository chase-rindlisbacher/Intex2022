from django.shortcuts import render, redirect
from .models import *
import datetime as dt
import dateutil.relativedelta as rd


# Create your views here.
def indexPageView(request) :
    nutrients = Nutrient.objects.filter(frequency = 'daily').order_by('name')

    context = {
        'nutrients': nutrients
    }
    return render(request, 'client_app/index.html', context)

def loginPageView(request) :
    if (request.method == 'POST'):
        uname = request.POST.get('username')
        pword = request.POST.get('password')

        try:
            user = Patient_Login.objects.get(username=uname, password = pword)
            return redirect('index')
        except:
            context = {
                'success': 'Login failed. Enter correct info, or create an account.'
            }
            return render(request, 'client_app/login.html', context)
    else:
        return render(request, 'client_app/login.html')

def newAccountPageView(request) :
    if (request.method == 'POST'):
        try:
            user = User()
            user.first_name = request.POST.get('fname')
            user.last_name = request.POST.get('lname')
            user.phone = request.POST.get('phone')
            user.email = request.POST.get('email')
            user.save()

            patient = Patient()
            patient.patient = User.objects.get(first_name = request.POST.get('fname'), last_name = request.POST.get('lname'), phone = request.POST.get('phone'), email = request.POST.get('email'))
            today = dt.datetime.today()
            bday = request.POST.get('bday')
            age = rd.relativedelta(today, dt.datetime.strptime(bday, '%Y-%m-%d'))
            patient.age = age.years
            patient.height = request.POST.get('height')
            patient.weight = request.POST.get('weight')
            patient.sex = request.POST.get('sex')
            patient.diagnosis = Condition.objects.get(id=request.POST.get('diagnosis'))
            patient.birthday = request.POST.get('bday')
            patient.save()

            login = Patient_Login()
            login.patient = User.objects.get(first_name = request.POST.get('fname'), last_name = request.POST.get('lname'), phone = request.POST.get('phone'), email = request.POST.get('email'))
            login.username = request.POST.get('username')
            login.password = request.POST.get('password')
            login.save()

            return redirect('login')
        except:
            exists = 'It looks like you have an account! Please login'
            context = {
                'success': exists
            }
            return render(request, 'client_app/new_user.html', context)
    else:
        diagnoses = Condition.objects.all()

        context = {
            'diagnoses': diagnoses
        }
        return render(request, 'client_app/new_user.html', context)

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
        'mg_nutrients': mg_nutrients,
    }

    return render(request, 'client_app/mydashboard.html', context)

def myProfileView(request):
    return render(request, 'client_app/myprofile.html')

def myCommunityView(request):
    return render(request, 'client_app/mycommunity.html')