from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def login_user_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        request.session['username'] = username
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome {username}')
            return redirect('centers_list')
        else:
            messages.success(request, 'Invalid username or password. Please try again...')
            return redirect('login')
    else:
        return render(request, 'users/login.html', {'title': 'Login'})


def logout_user_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully')
    return redirect('login')

