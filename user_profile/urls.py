from django.urls import path
from . import views
from pages_render import views as render_views

urlpatterns = [
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('cycles/', views.CycleList.as_view()),
    path('cycles/<int:pk>/', views.CycleDetail.as_view()),
    path('boosts/<int:mainCycle>/', views.BoostList.as_view()),
    path('buyBoost/', views.buyBoost, name="buyBoost"),
    path('logout/', render_views.user_logout),
    path('set_main_cycle/', views.set_main_cycle),
]
