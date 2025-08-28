
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm
from .models import User
from outpasses.models import Outpass
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import user_passes_test

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()
            messages.success(request, 'Registration successful. Please login.')
            return redirect('login')
        else:
            # Print form errors to the terminal for debugging
            print("DEBUG: Registration form errors ->", form.errors)
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
        messages.error(request, 'Invalid credentials.')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def dashboard(request):
    user = request.user
    if user.role == 'student':
        recent = Outpass.objects.filter(student=user).order_by('-created_at')[:5]
        staff_list = User.objects.filter(role__in=['warden', 'faculty'])
        return render(request, 'dashboards/student.html', {
            'recent': recent,
            'staff_list': staff_list
        })
    elif user.role in ['faculty','warden']:
        pending = Outpass.objects.filter(status='pending').order_by('created_at')[:10]
        return render(request, 'dashboards/staff.html', {'pending': pending})
    return redirect('home')

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

def is_staff(user):
    return user.is_authenticated and user.role in ['faculty','warden']

@login_required
@user_passes_test(is_staff)
def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    return render(request, 'accounts/profile_view.html', {'profile_user': profile_user})



from django.contrib.auth.decorators import login_required
@login_required
def contacts(request):
    from .models import User
    wardens = User.objects.filter(role='warden')
    faculty = User.objects.filter(role='faculty')
    return render(request, 'accounts/contacts.html', {'wardens': wardens, 'faculty': faculty})
