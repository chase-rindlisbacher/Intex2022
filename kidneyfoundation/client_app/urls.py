from django.urls import path
from .views import *

urlpatterns = [
    path('login/', loginPageView, name='login'),
    path('create/', newAccountPageView, name='new_user'),
    path('mymenu/', myMenuView, name='mymenu'),
    path('mymenu/add', myMenuAdd, name='mymenuadd'),
    path('myfoodjournal/', myFoodJournalView, name='myfoodjournal'),
    path('myfoodjournal/add', myFoodJournalAdd, name='myfoodjournaladd'),
    path('mydashboard/', myDashboardView, name='mydashboard'),
    path('', indexPageView, name='index'),
]