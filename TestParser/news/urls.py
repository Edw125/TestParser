from django.urls import path

from news import views

urlpatterns = [
    path('', views.index, name=''),
    path('index/', views.index, name='index'),
    ]
