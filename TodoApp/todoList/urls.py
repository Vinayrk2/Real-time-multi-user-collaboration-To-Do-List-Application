from django.shortcuts import render
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='index'),
    path('create/group/', views.create_group, name='create_group'),
    path('join/<id>', views.join_group, name='join_group'),
]