from django.contrib import admin
from django.urls import path, include
from . import  views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('sign_up/', views.sign_up_view, name='sign_up'),
    path('logout/', views.logout_view, name='logout'),
    path('my-info/', views.my_info_view, name='my_info'),
    
]


