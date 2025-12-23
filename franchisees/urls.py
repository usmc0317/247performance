from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.franchisee_dashboard, name='franchisee_dashboard'),
    path('analytics/', views.franchisee_analytics, name='franchisee_analytics'),
    path('clients/', views.franchisee_clients, name='franchisee_clients'),
]
