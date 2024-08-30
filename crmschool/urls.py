from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from users import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('centers.urls')),
    path('', RedirectView.as_view(url='centers/', permanent=True)),
    path('accounts/login/', views.login_user_view, name='login'),
    path('logout/', views.logout_user_view, name='logout'),
]