from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def franchisee_dashboard(request):
    """Franchisee dashboard view"""
    if request.user.user_type != 'franchisee':
        return redirect('dashboard')
    return render(request, 'franchisees/dashboard.html')

@login_required
def franchisee_analytics(request):
    """Franchisee analytics view"""
    return render(request, 'franchisees/analytics.html')

@login_required
def franchisee_clients(request):
    """Franchisee client management view"""
    return render(request, 'franchisees/clients.html')
