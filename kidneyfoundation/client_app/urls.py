from django.urls import path
from .views import *

urlpatterns = [
    path('login/', loginPageView, name='login'),
    path('create/', newAccountPageView, name='new_user'),
    path('logout/', logoutUser, name='logout'),
    path('myfoodjournal/', myFoodJournalView, name='myfoodjournal'),
    path('myfoodjournal/add', myFoodJournalAdd, name='myfoodjournaladd'),
    path('mydashboard/', myDashboardView, name='mydashboard'),
    path('myprofile/', myProfileView, name='myprofile'),
    path('mycommunity/', myCommunityView, name='mycommunity'),
    path('', indexPageView, name='index'),
]