from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('game/', views.game_board, name='game_board'),
    path('start_game/', views.start_game, name='start_game'),
    path('resolve_game/', views.resolve_game, name='resolve_game'),
    path('quit_game/', views.quit_game, name='quit_game'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout_view'),
]
