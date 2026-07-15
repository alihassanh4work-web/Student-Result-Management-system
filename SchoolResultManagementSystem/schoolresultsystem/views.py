from django.shortcuts import render , redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
# Create your views here.
def index(request):
    return render(request,'index.html')

def admin_login(request):   
    if request.user.is_authenticated:
        return redirect('admin_dashboard')
    else:
        error=None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            error = 'Invalid username or password'
    return render(request, 'admin_login.html',locals())

def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

def Create_class(request):
    return render(request, 'Create_class.html')