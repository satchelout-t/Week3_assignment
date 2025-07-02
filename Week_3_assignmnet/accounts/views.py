# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm # Django's built-in login form
from django.contrib.auth.decorators import login_required


# For simulated email verification, we'll use user.pk as a token
# In a real application, you'd generate a more secure, time-limited token (e.g., using Django's Signer)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate user until verified
            user.save()

            # --- Simulated Email Verification ---
            # In a real app: generate unique token, save it (e.g., in a separate model, or email_confirmation table)
            # and send email with link like: /verify/?token=<actual_secure_token>
            # For this assignment, we use user.pk as a simple token.
            verification_token = user.pk
            messages.success(request, "Account created successfully! Please check your (simulated) email for verification.")
            return redirect('verify_account', token=verification_token)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def verify_account(request, token):
    try:
        # In a real app, you'd decode a secure token, check expiry, etc.
        # For this assignment, 'token' is assumed to be the user's primary key (pk)
        user = User.objects.get(pk=token)
        if not user.is_active:
            user.is_active = True
            user.save()
            messages.success(request, "Account Verified Successfully! You can now log in.")
        else:
            messages.info(request, "Your account is already verified.")
    except User.DoesNotExist:
        messages.error(request, "Invalid verification link or user does not exist.")
    return render(request, 'accounts/verify.html')

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active: # Check if user is active (verified)
                    login(request, user)
                    messages.success(request, f"Welcome back, {username}!")
                    return redirect('dashboard') # Redirect to dashboard after login
                else:
                    messages.warning(request, "Your account is not active. Please verify your email first.")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.") # Catches non-field errors from form
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('user_login') # Redirect to login page after logout
@login_required(login_url='user_login') # Redirects unauthenticated users to the login page
def dashboard(request):
    return render(request, 'accounts/dashboard.html', {'user': request.user})