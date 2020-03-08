from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='fw-home'),
    path('stats/', views.stats, name='fw-stats'),
    path('rules/', views.stats, name='fw-rules'),
]
