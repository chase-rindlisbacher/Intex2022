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
    return render(request, 'client_app/view_items.html')
    
def myMenuAdd(request):
    return render(request, 'client_app/add_item.html')

def myPostsView(request):
    return render(request, 'client_app/view_posts.html')

def myPostsAdd(request):
    return render(request, 'client_app/add_post.html')

def myStatsView(request):
    return render(request, 'client_app/highlights.html')