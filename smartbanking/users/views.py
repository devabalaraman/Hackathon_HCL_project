from ratelimit.decorators import RateLimitDecorator
import bcrypt
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .forms import RegistrationForm, LoginForm, KYCForm
from .models import User, KYC

# Registration
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            role = form.cleaned_data['role']

            hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            user = User.objects.create(username=username, email=email, password=hashed_password, role=role)
            messages.success(request, f"Registration successful as {role}! Please login.")
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})

# Login
@RateLimitDecorator(calls=5, period=60, raise_on_limit=True)
def login_view(request):
        form = LoginForm(request.POST)
        if request.user.is_authenticated:
            if request.user.role == 'customer':
                return redirect('kyc_submit')
            elif request.user.role == 'admin':
                return redirect('view_all_users')
        if request.method == "POST":
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password'].encode()
                try:
                    user = User.objects.get(username=username)
                    if bcrypt.checkpw(password, user.password.encode()):
                        auth_login(request, user)
                        return redirect('kyc_submit')
                    else:
                        messages.error(request, "Invalid credentials")
                except User.DoesNotExist:
                    messages.error(request, "Invalid credentials")
        else:
            form = LoginForm()
        return render(request, 'users/login.html', {'form': form})

# Logout
def logout_view(request):
    auth_logout(request)
    return redirect('login')

# KYC Submission
@login_required(login_url='login')
def kyc_submit(request):
    
    if request.user.role != 'customer':
        return redirect('view_all_users')
    try:
        kyc = KYC.objects.get(user=request.user)
        submitted = True
    except KYC.DoesNotExist:
        submitted = False

    if request.method == "POST":
        form = KYCForm(request.POST, request.FILES)
        if form.is_valid():
            kyc_obj = form.save(commit=False)
            kyc_obj.user = request.user
            kyc_obj.save()
            messages.success(request, "KYC submitted successfully")
            return redirect('kyc_submit')
    else:
        form = KYCForm()
    return render(request, 'users/kyc_submit.html', {'form': form, 'submitted': submitted})

#get all users
@login_required(login_url='login')
def list_all_users(request):
    if request.user.role != 'admin':
        return JsonResponse({'error': 'Permission denied. Admins only.'}, status=403)

    users = User.objects.all()  # Query all users
    return render(request, 'users/admin_users.html', {'users': users})

# Get all KYC submissions with username and status
@login_required(login_url='login')
def list_all_kyc_submissions(request):
    if request.user.role != 'admin':
        return JsonResponse({'error': 'Permission denied. Admins only.'}, status=403)

    kyc_list = KYC.objects.select_related('user').all()
    return render(request, 'users/admin_kyc.html', {'kyc_list': kyc_list})
