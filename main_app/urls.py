from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('game/', views.game_board, name='game_board'),
    path('start_game/', views.start_game, name='start_game'),
    path('resolve_game/', views.resolve_game, name='resolve_game'),
]
