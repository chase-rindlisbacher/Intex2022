from django.shortcuts import render, redirect
from .models import *
import datetime as dt
import dateutil.relativedelta as rd
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth import authenticate


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

        user = authenticate(username=uname, password=pword)

        if user is not None:
            login(request, user)
            fname = user.first_name
            nutrients = Nutrient.objects.filter(frequency = 'daily').order_by('name')

            context = {
                'fname': fname, 
                'nutrients': nutrients
            }
            return render(request, 'client_app/index.html', context)
        else:
            messages.error(request, 'Bad credentials')
            return redirect('new_user')
    else: 
        nutrients = Nutrient.objects.filter(frequency = 'daily').order_by('name')
        context = {
            'nutrients': nutrients
        }
        return render(request, 'client_app/login.html', context)

def newAccountPageView(request) :
    if (request.method == 'POST'):
        try:
            username = request.POST.get('username')
            email = request.POST.get('email')
            pass1 = request.POST['password']

            new_user = User.objects.create_user(username, email, pass1)
            new_user.first_name = request.POST.get('fname')
            new_user.last_name = request.POST.get('lname')

            new_user.save()
            messages.success(request, 'You did it!')

            person = SiteUser()
            person.username = request.POST.get('username')
            person.first_name = request.POST.get('fname')
            person.last_name = request.POST.get('lname')
            person.phone = request.POST.get('phone')
            person.email = request.POST.get('email')
            person.save()

            patient = Patient()
            patient.patient = SiteUser.objects.get(first_name = request.POST.get('fname'), last_name = request.POST.get('lname'), phone = request.POST.get('phone'), email = request.POST.get('email'))
            patient.username = request.POST.get('username')
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

            return redirect('login')
        except:
            exists = 'Username taken. Login or create a new one'
            diagnoses = Condition.objects.all()

            context = {
                'success': exists,
                'diagnoses': diagnoses
            }
            return render(request, 'client_app/new_user.html', context)
    diagnoses = Condition.objects.all()
    context = {
        'success': '',
        'diagnoses': diagnoses
    }
    return render(request, 'client_app/new_user.html', context)

def myMenuView(request):
    return render(request, 'client_app/mymenu.html')
    
def myMenuAdd(request):
    if (request.method == 'POST'):
        name = request.POST.get('name')
        description = request.POST.get('desc')
        sodium = request.POST.get('na')
        protein = request.POST.get('protein')
        potassium = request.POST.get('k')
        phosphorus = request.POST.get('phos')
        day = request.POST.get('day')
        meal = request.POST.get('eating_time')
        quant = request.POST.get('quantity')
    return render(request, 'client_app/addfoods.html')

def myFoodJournalView(request):
    if request.user.is_authenticated:
        try:
            foods = Report_Food.objects.get(username = request.user.get_username())
            drinks = Report_Drink.objects.get(username = request.user.get_username())

            context = {
                'foods': foods,
                'drinks': drinks
            }

            return render(request, 'client_app/myfoodjournal.html', context)
        except:
            return render(request, 'client_app/myfoodjournal.html')
    else:
        return redirect('login')

def myFoodJournalAdd(request):
    if (request.method == 'POST'):
        if (request.POST.get('form_type') == 'food'):
            if (request.POST.get('existing') == 'no-exist'):
                posted_date = request.POST.get('day')
                new_food = Food_Item()
                new_food.food_type = Food_Type.objects.get(id = int(request.POST.get('food_type')))
                new_food.name = request.POST.get('name')
                new_food.description = request.POST.get('desc')
                new_food.units = Food_Units(id=request.POST.get('units'))
                new_food.sodium = float(request.POST.get('na'))
                new_food.protein = float(request.POST.get('protein'))
                new_food.potassium = float(request.POST.get('k'))
                new_food.phosphorus = float(request.POST.get('phos'))
                new_food.save()

                food_entry = Report_Food()
                food_entry.username = request.POST.get('username')
                food_entry.patient = Patient.objects.get(username = request.POST.get('username'))
                food_entry.date = dt.datetime.strptime(posted_date, '%Y-%m-%d')
                food_entry.eating_time = request.POST.get('eating_time')
                food_entry.units_count = request.POST.get('units')
                food_entry.food = Food_Item.objects.get(name = request.POST.get('name'))
                food_entry.save()

            else:
                posted_date = request.POST.get('day')
                food_entry = Report_Food()
                food = Food_Item.objects.get(name = request.POST.get('combo_food'))
                food_entry.patient = Patient.objects.get(username = request.POST.get('username'))
                food_entry.food = food
                food_entry.username = request.POST.get('username')
                food_entry.patient = Patient.objects.get(username = request.POST.get('username'))
                food_entry.date = dt.datetime.strptime(posted_date, '%Y-%m-%d')
                food_entry.eating_time = request.POST.get('eating_time')
                food_entry.units_count = float(request.POST.get('units'))
                food_entry.save()
        else:
            return None

    foods = Food_Item.objects.all()
    food_types = Food_Type.objects.all()
    drinks = Drink_Item.objects.all()
    fluid_types = Fluid_Type.objects.all()
    food_units = Food_Units.objects.all()

    context = {
        'foods': foods,
        'food_types': food_types,
        'drinks': drinks,
        'fluid_types': fluid_types,
        'food_units': food_units
    }

    return render(request, 'client_app/addjournalentry.html', context)

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

def logoutUser(request):
    logout(request)
    return redirect('index')