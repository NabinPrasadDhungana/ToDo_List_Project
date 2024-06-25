from django.contrib import admin
from django.urls import path, include
from .views import *
from . import views

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('item/<int:id>/<str:pk>/', ItemDetailView.as_view(), name='item_detail'),
    path('update/<int:id>/<str:pk>/', ItemUpdateView.as_view(), name='item_update'),
    path('create/', ItemCreateView.as_view(), name='item_create'),
]