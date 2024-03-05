from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .forms import SignUpForm


def home_view(request):
    return render(request, 'home.html', {})


def login_user_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome {username}')
            return redirect('centers_list')
        else:
            messages.success(request, 'Invalid username or password. Please try again...')
            return redirect('login')
    else:
        return render(request, 'users/login.html', {})


def logout_user_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully')
    return redirect('login')


# def register_user_view(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password1']
#             user = authenticate(username=username, password=password)
#             login(request, user)
#             messages.success(request, 'Account created successfully')
#             return redirect('centers_list')
#     else:
#         form = SignUpForm()
#         return render(request, 'users/register.html', {'form': form})
#     return render(request, 'users/register.html', {'form': form})
