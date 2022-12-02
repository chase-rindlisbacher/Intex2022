from django.shortcuts import render, redirect
from .models import *
import datetime as dt
import dateutil.relativedelta as rd
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth import authenticate
import psycopg2


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
            failed = True

            context = {
                'success': exists,
                'diagnoses': diagnoses,
                'failed' : failed
            }
            return render(request, 'client_app/new_user.html', context)
    diagnoses = Condition.objects.all()
    context = {
        'success': '',
        'diagnoses': diagnoses
    }
    return render(request, 'client_app/new_user.html', context)

def myFoodJournalView(request):
    if request.user.is_authenticated:
        foods = Report_Food.objects.filter(username = request.user.get_username()).order_by('-date')

        max_potassium = Nutrient.objects.get(name = 'potassium', frequency='daily').patient_target_max
        min_potassium = Nutrient.objects.get(name = 'potassium', frequency='daily').patient_target_min

        max_sodium = Nutrient.objects.get(name = 'sodium', frequency='daily').patient_target_max
        min_sodium = Nutrient.objects.get(name = 'sodium', frequency='daily').patient_target_min

        max_phosphorus = Nutrient.objects.get(name = 'phospherus', frequency='daily').patient_target_max
        min_phosphorus = Nutrient.objects.get(name = 'phospherus', frequency='daily').patient_target_min

        max_protein = Nutrient.objects.get(name = 'protein', frequency='daily').patient_target_max
        min_protein = Nutrient.objects.get(name = 'protein', frequency='daily').patient_target_min

        max_water_man = Nutrient.objects.get(name = 'water', frequency='daily', gender_specific='male').patient_target_max
        min_water_man = Nutrient.objects.get(name = 'water', frequency='daily', gender_specific='male').patient_target_min

        username = request.user.get_username()

        conn = psycopg2.connect(host="localhost", port = 5432, database="kidneys", user="postgres", password="joRdaN23#1")
        cur = conn.cursor()
        cur.execute(""" SELECT sum(Potassium) as potassium
        FROM
        (SELECT date,username,(potassium * Quantity) as Potassium
        FROM
        (SELECT date,sum(units_count) as Quantity,food_id,username
        FROM report_food
        GROUP BY food_id, date,username) AS sq1
        INNER JOIN food_item as fi ON sq1.food_id = fi.id) sq2
        GROUP BY date,username
        HAVING (sq2.username = %s) and (cast(sq2.date as date) = CURRENT_DATE)
        ORDER BY sq2.date asc; """, (username,))

        user_potassium = cur.fetchall()
        cur.close()
        conn.close()
        potassium = [item for t in user_potassium for item in t]

        context = {
            'foods': foods,
            'potassium': potassium,
            'min-potassium': min_potassium,
            'max-potassium': max_potassium,
            'min-sodium': min_sodium,
            'max-sodium': max_sodium,
            'min-phospherus': min_phosphorus,
            'max-phospherus': max_phosphorus,
            'min-protein': min_protein,
            'max-protein': max_protein,
            'min-water': min_water_man,
            'max-water': max_water_man,
        }

        return render(request, 'client_app/myfoodjournal.html', context)
    else:
        return redirect('login')

def myFoodJournalAdd(request):
    if (request.method == 'POST'):
        if (request.POST.get('existing') == 'no-exist'):
            posted_date = request.POST.get('day')
            new_food = Food_Item()
            new_food.food_type = Food_Type.objects.get(id = int(request.POST.get('food_type')))
            new_food.name = request.POST.get('name').lower()
            new_food.description = request.POST.get('desc').lower()
            new_food.units = Food_Units.objects.get(id=request.POST.get('units'))
            new_food.sodium = float(request.POST.get('na'))
            new_food.protein = float(request.POST.get('protein'))
            new_food.potassium = float(request.POST.get('k'))
            new_food.phosphorus = float(request.POST.get('phos'))
            new_food.water = float(request.POST.get('water'))
            new_food.save()

            food_entry = Report_Food()
            food_entry.username = request.POST.get('username')
            food_entry.patient = Patient.objects.get(username = request.POST.get('username'))
            food_entry.date = dt.datetime.strptime(posted_date, '%Y-%m-%d')
            food_entry.eating_time = request.POST.get('eating_time')
            food_entry.units_count = float(request.POST.get('quantity'))
            food_entry.food = Food_Item.objects.get(name = request.POST.get('name'))
            food_entry.water = (float(request.POST.get('water')) * float(request.POST.get('quantity')))
            food_entry.sodium = (float(request.POST.get('na')) * float(request.POST.get('quantity')))
            food_entry.potassium = (float(request.POST.get('k')) * float(request.POST.get('quantity')))
            food_entry.phosphorus = (float(request.POST.get('phos')) * float(request.POST.get('quantity')))
            food_entry.protein = (float(request.POST.get('protein')) * float(request.POST.get('quantity')))
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
            food_entry.units_count = float(request.POST.get('quantity'))
            food_entry.sodium = (float(request.POST.get('quantity')) * float(food.sodium))
            food_entry.potassium = (float(request.POST.get('quantity')) * float(food.potassium))
            food_entry.phosphorus = (float(request.POST.get('quantity')) * float(food.phosphorus))
            food_entry.protein = (float(request.POST.get('quantity')) * float(food.protein))
            food_entry.save()
        
    foods = Food_Item.objects.all()
    food_types = Food_Type.objects.all()
    food_units = Food_Units.objects.all()

    context = {
        'foods': foods,
        'food_types': food_types,
        'food_units': food_units,
        #'potassium': potassium_level,
        #'sodium': sodium_level,
        #'phosphorus': phosphorus_level,
        #'protein': protein_level,
        #'water': water_level,
    }
    return render(request, 'client_app/addjournalentry.html', context)

def myDashboardView(request):
    import psycopg2
    mg_nutrients = Nutrient.objects.filter(units='mg', frequency='daily')
    g_nutrients = Nutrient.objects.filter(units='g/kg bd wt', frequency='daily')
    L_day = Nutrient.objects.filter(units='L/day', frequency='daily')
    if request.user.is_authenticated:
        try:
            username = request.user.get_username()
            conn = psycopg2.connect(host="localhost", port = 5432, database="kidneys", user="postgres", password="joRdaN23#1")
            cur = conn.cursor()
            cur.execute(""" SELECT sum(Sodium) as sodium
            FROM
            (SELECT date,username,(sodium * Quantity) as Sodium,(potassium * Quantity) as Potassium,(phosphorus * Quantity) as Phosphorus
            FROM
            (SELECT date,sum(units_count) as Quantity,food_id,username
            FROM report_food
            GROUP BY food_id, date,username) AS sq1
            INNER JOIN food_item as fi ON sq1.food_id = fi.id) sq2
            GROUP BY date,username
            HAVING (sq2.username = %s) and (cast(sq2.date as date) = CURRENT_DATE)
            ORDER BY sq2.date asc; """, (username,))
            user_sodium = cur.fetchall()
            cur.close()
            conn.close()
            sodium = [item for t in user_sodium for item in t]

            conn = psycopg2.connect(host="localhost", port = 5432, database="kidneys", user="postgres", password="joRdaN23#1")
            cur = conn.cursor()
            cur.execute(""" SELECT sum(Potassium) as potassium
            FROM
            (SELECT date,username,(potassium * Quantity) as Potassium
            FROM
            (SELECT date,sum(units_count) as Quantity,food_id,username
            FROM report_food
            GROUP BY food_id, date,username) AS sq1
            INNER JOIN food_item as fi ON sq1.food_id = fi.id) sq2
            GROUP BY date,username
            HAVING (sq2.username = %s) and (cast(sq2.date as date) = CURRENT_DATE)
            ORDER BY sq2.date asc; """, (username,))

            user_potassium = cur.fetchall()
            cur.close()
            conn.close()
            potassium = [item for t in user_potassium for item in t]

            conn = psycopg2.connect(host="localhost", port = 5432, database="kidneys", user="postgres", password="joRdaN23#1")
            cur = conn.cursor()
            cur.execute(""" SELECT sum(Phosphorus) as phosphorus
            FROM
            (SELECT date,username,(phosphorus * Quantity) as Phosphorus
            FROM
            (SELECT date,sum(units_count) as Quantity,food_id,username
            FROM report_food
            GROUP BY food_id, date,username) AS sq1
            INNER JOIN food_item as fi ON sq1.food_id = fi.id) sq2
            GROUP BY sq2.date,sq2.username
            HAVING (sq2.username = %s) and (cast(sq2.date as date) = CURRENT_DATE)
            ORDER BY sq2.date asc; """, (username,))

            user_phosphorus = cur.fetchall()
            cur.close()
            conn.close()
            phosphorus = [item for t in user_phosphorus for item in t]

            conn = psycopg2.connect(host="localhost", port = 5432, database="kidneys", user="postgres", password="joRdaN23#1")
            cur = conn.cursor()
            cur.execute(""" SELECT sum(Protein) as protein
            FROM
            (SELECT date,username,(protein * Quantity) as Protein
            FROM
            (SELECT date,sum(units_count) as Quantity,food_id,username
            FROM report_food
            GROUP BY food_id, date,username) AS sq1
            INNER JOIN food_item as fi ON sq1.food_id = fi.id) sq2
            GROUP BY sq2.date,sq2.username
            HAVING (sq2.username = %s) and (cast(sq2.date as date) = CURRENT_DATE)
            ORDER BY sq2.date asc; """, (username,))

            user_protein = cur.fetchall()
            cur.close()
            conn.close()
            protein = [item for t in user_protein for item in t]

            conn = psycopg2.connect(host="localhost", port = 5432, database="kidneys", user="postgres", password="joRdaN23#1")
            cur = conn.cursor()
            cur.execute(""" SELECT sum(Water) as water
            FROM
            (SELECT date,username,(water * Quantity) as Water
			 FROM
            (SELECT date,sum(units_count) as Quantity,food_id,username
            FROM report_food
            GROUP BY food_id, date,username) AS sq1
            INNER JOIN food_item as fi ON sq1.food_id = fi.id) sq2
            GROUP BY date,username
            HAVING (sq2.username = %s ) and (cast(sq2.date as date) = CURRENT_DATE)
            ORDER BY sq2.date asc; """, (username,))

            user_water = cur.fetchall()
            cur.close()
            conn.close()
            water = [item for t in user_water for item in t]

            conn = psycopg2.connect(host="localhost", port = 5432, database="kidneys", user="postgres", password="joRdaN23#1")
            cur = conn.cursor()
            cur.execute(""" SELECT weight FROM patient
            WHERE username= %s; """,(username,))

            user_weight = cur.fetchall()
            cur.close()
            conn.close()
            weight = [item for t in user_weight for item in t]
            weight[0] = weight[0] * 0.6
            context = {
            'mg_nutrients': mg_nutrients,
            'g_nutrients': g_nutrients,
            'L_day' : L_day,
            'user_sodium' : sodium,
            'user_potassium' : potassium,
            'user_phosphorus' : phosphorus,
            'user_protein' : protein,
            'user_water' : water,
            'user_weight' : weight,
            }
            # sq_food = Report_Food.objects.raw(f'SELECT ')
            # sq1 = Report_Food.objects.raw(f'SELECT * FROM report_food WHERE username={username}')
            # sq2 = Report_Food.objects.raw(f'SELECT * FROM report_drink WHERE username={username}')
            # ungrouped = sq1.objects.raw(f'SELECT * FROM {sq1} INNER JOIN {sq2} ON {sq1}.username = {sq2}.username')
            # ungrouped.objects.raw(f'SELECT ')
        except:
            context = {
            'mg_nutrients': mg_nutrients,
            'g_nutrients': g_nutrients,
            'L_day' : L_day,
            }
    else: 
        context = {

        }

    return render(request, 'client_app/mydashboard.html', context)

def myProfileView(request):
    return render(request, 'client_app/myprofile.html')

def myCommunityView(request):
    return render(request, 'client_app/mycommunity.html')

def logoutUser(request):
    logout(request)
    return redirect('index')