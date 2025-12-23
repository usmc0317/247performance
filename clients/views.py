from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def client_dashboard(request):
    """Client dashboard view"""
    if request.user.user_type != 'client':
        return redirect('dashboard')
    return render(request, 'clients/dashboard.html')

@login_required
def client_profile(request):
    """Client profile view"""
    return render(request, 'clients/profile.html')

@login_required
def client_training(request):
    """Client training view"""
    return render(request, 'clients/training.html')

@login_required
def client_progress(request):
    """Client progress tracking view"""
    return render(request, 'clients/progress.html')
