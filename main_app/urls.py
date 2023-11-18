from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('start/', views.start_game, name='start_game'),
    path('guess/', views.make_guess, name='make_guess'),
    path('reset/', views.reset_game, name='reset_game'),
]
