from django.urls import path
from . import views

urlpatterns = [
    path('notebook', views.notes_list, name="notebook"),
    path('new-note', views.notes_creating, name="new-note"),
    path('logout/', views.notes_logout, name="logout"),
]
