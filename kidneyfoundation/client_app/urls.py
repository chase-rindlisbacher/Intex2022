from django.urls import path
from .views import indexPageView

urlpatterns = [
    path("", indexPageView, name='index'),
    # path('<str:movie>/<int:stars>', showMoviePageView, name='show')
]