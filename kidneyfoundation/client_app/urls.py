from django.urls import path
from .views import *

urlpatterns = [
    path('login/', loginPageView, name='login'),
    path('create/', newAccountPageView, name='new_user'),
    path('mymenu/', myMenuView, name='mymenu'),
    path('myfoodjournal/', myPostsView, name='myfoodjournal'),
    path('mydashboard/', myStatsView, name='mydashboard'),
    path('', indexPageView, name='index'),
]