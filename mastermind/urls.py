from django.contrib import admin
from django.urls import path, include
import debug_toolbar

from main_app import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main_app.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
]
