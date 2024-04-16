from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from users import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('centers.urls')),
    path('', views.home_view, name='home'),
    path('accounts/login/', views.login_user_view, name='login'),
    path('logout/', views.logout_user_view, name='logout'),
    # path('register/', views.register_user_view, name='register'),
]