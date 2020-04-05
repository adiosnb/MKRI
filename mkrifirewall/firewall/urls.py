from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='fw-home'),
    path('stats/', views.stats, name='fw-stats'),
    path('rules/', views.rules, name='fw-rules'),
    path('get/ajax/stats', views.get_traffic_stats, name='ajax/stats'),
]
