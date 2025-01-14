from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User


def user_login(req):
    if req.method == 'POST':
        email = req.POST.get('email').lower()
        password = req.POST.get('password')
        
        # Authenticate the user
        user = authenticate(req, email=email, password=password)
        
        if user is not None:
            login(req, user)  # Log in the user
            # check if user needs to change their pasword
            if user.needs_password_change == True:
                messages.warning(req, 'Please change your password.')
                return redirect('account:change_password')
            return redirect('core:home')  
        else:
            messages.warning(req, 'Invalid email or password.')  # Show an error message
    return render(req, 'account/login.html')


def user_logout(req):
    logout(req)  
    return redirect('account:login')  


@login_required(login_url='account:login')
def user_profile(req):
    context = {"page_title": "User Profile"}
    if req.method == 'POST':
        first_name = req.POST.get('first_name')
        last_name = req.POST.get('last_name')

        # Update the user's profile
        user = req.user
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        messages.success(req, 'Your profile has been updated successfully!')
        return redirect('account:profile')
    return render(req, "account/user_profile.html", context)


@login_required  
def change_password(req):
    if req.method == 'POST':
        current_password = req.POST.get('current_password')
        new_password = req.POST.get('new_password')
        confirm_password = req.POST.get('confirm_password')

        user = req.user  # The logged-in user

        # Check the current password
        if not user.check_password(current_password):
            messages.warning(req, 'Current password is incorrect.')
            return redirect('account:change_password')

        # Check if new passwords match
        if new_password != confirm_password:
            messages.warning(req, 'New passwords do not match.')
            return redirect('account:change_password')

        # Change password
        user.set_password(new_password)
        user.needs_password_change = False  # Reset the flag
        user.save()

        # Update the session hash to keep the user logged in after password change
        update_session_auth_hash(req, user)

        messages.success(req, 'Your password has been changed successfully!')
        return redirect('account:profile')  

    return render(req, 'account/change_password.html')  # Render the password change template
