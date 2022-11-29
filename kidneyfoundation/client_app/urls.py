from django.urls import path
from .views import *

urlpatterns = [
    path('<str:user_type>/login/', loginPageView, name='login'),
    path('mymenu/', myMenuView, name='mymenu'),
    path('mymenu/add/', myMenuAdd, name='mymenu_add'),
    path('myposts/', myPostsView, name='myposts'),
    path('myposts/add/', myPostsAdd, name='myposts_add'),
    path('mystats/', myStatsView, name='mystats'),
    path('', indexPageView, name='index'),
]