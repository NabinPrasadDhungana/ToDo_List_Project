from django.contrib import admin
from django.urls import path, include
from .views import *
from . import views

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('item/<int:id>/<str:pk>', ItemDetailView.as_view(), name='item-detail'),
]