from django.contrib import admin
from django.urls import path, include
import debug_toolbar
from rest_framework import routers
from main_app.views import UserViewSet, GroupViewSet
from main_app.api_views import StartGameView, MakeGuessView, EndGameView
from main_app import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/game/start', StartGameView.as_view(), name='start_game'),
    path('api/game/guess', MakeGuessView.as_view(), name='make_guess'),
    path('api/game/end', EndGameView.as_view(), name='end_game'),
    path('__debug__/', include(debug_toolbar.urls)),
]
