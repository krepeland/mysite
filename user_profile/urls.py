from django.urls import path
from . import views

urlpatterns = [
    path('click/', views.callClick, name="click"),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
]
