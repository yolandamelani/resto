from django.urls import path, include
from api import views
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (
    TableRestoListApiView, TableRestoDetailApiView, RegisterUserAPIView, LoginView,
)
app_name = 'api'

urlpatterns = [
    #path('api/v1/login', LoginView.as_view()),
    #path('api/v1/Logout', LogoutView.as_view()),
    path('api/table_resto', views.TableRestoListApiView.as_view()),
    path('api/table_resto/<int:id>', views.TableRestoDetailApiView.as_view()),
    path('api/register', RegisterUserAPIView.as_view()),
    path('api/login', LoginView.as_view()),
    path('api/menu-resto', views.MenuRestoView.as_view()),
    path('api/menu-resto-filter/', views.MenuRestoFilterAPi.as_view()),
]