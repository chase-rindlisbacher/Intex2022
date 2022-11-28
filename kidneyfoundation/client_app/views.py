from django.shortcuts import render

# Create your views here.
def indexPageView(request) :
    return render(request, 'client_app.index.html')