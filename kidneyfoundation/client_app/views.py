from django.shortcuts import render, HttpResponse

# Create your views here.
def indexPageView(request) :
    return render(request, 'client_app/index.html')

def loginPageView(request, user_type) :
    context = {
        'type': user_type
    }
    return render(request, 'client_app/login.html', context)

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