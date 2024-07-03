from django.contrib import admin
from django.urls import path, include
from .views import *
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('item/<int:id>/<str:pk>/', views.ItemDetailView.as_view(), name='item_detail'),
    path('update/<int:id>/<str:pk>/', views.ItemUpdateView.as_view(), name='item_update'),
    path('create-list/', views.ToDoListCreateView.as_view(), name='list_create'),
    path('list-update/<int:pk>/', views.ToDoListUpdateView.as_view(), name='list_update'),
    path('delete-list/<int:pk>/', views.ToDoListDeleteView.as_view(), name='list_delete'),
    path('create/', views.ItemCreateView.as_view(), name='item_create'),
    path('delete/<int:id>/<str:pk>/', views.ItemDeleteView.as_view(), name='item_delete'),
    path('accounts/signup/', CustomSignupView.as_view(), name='account_signup'),
]