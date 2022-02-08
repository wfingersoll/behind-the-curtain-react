#Soren Wilson >:[

from django.urls import path, re_path
from .views import views

views = views()

urlpatterns = [
    path('', views.index),
    path('search/', views.search),
    path('search/movie/<str:search_title>/', views.movie),
    path('search/<str:name>/', views.actor_and_company)
]
