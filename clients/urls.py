from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.client_dashboard, name='client_dashboard'),
    path('profile/', views.client_profile, name='client_profile'),
    path('training/', views.client_training, name='client_training'),
    path('progress/', views.client_progress, name='client_progress'),
]
