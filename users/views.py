from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.safestring import mark_safe


def login_user_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        request.session['username'] = username
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            success_message = f'Вітаю <strong>{username}</strong> в системі'
            # messages.success(request, f'Welcome <strong>{username}</strong>')
            messages.success(request, mark_safe(success_message))
            return redirect('centers_list')
        else:
            messages.success(request, 'Неправильний логін або пароль. Спробуйте ще раз...')
            return redirect('login')
    else:
        return render(request, 'users/login.html', {'title': 'Login'})


def logout_user_view(request):
    logout(request)
    messages.success(request, 'Ви успішно вийшли з системи')
    return redirect('login')

