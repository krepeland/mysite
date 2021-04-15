from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.index),
    path('login/', views.user_login, name="login"),
    path('logout/', views.user_logout),
    path('registration/', views.user_registration, name="registration"),
]
