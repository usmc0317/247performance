from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def login_view(request):
    """Login view that redirects based on user type"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'core/login.html')

@login_required
def dashboard(request):
    """Dashboard that redirects to appropriate portal based on user type"""
    if request.user.user_type == 'client':
        return redirect('client_dashboard')
    elif request.user.user_type == 'franchisee':
        return redirect('franchisee_dashboard')
    else:
        return redirect('admin:index')

