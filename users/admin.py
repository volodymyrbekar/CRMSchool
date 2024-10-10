from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import CustomUser
from django.contrib.auth.models import Permission
from .forms import CustomUserChangeForm


class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'role', 'first_name']
    fieldsets = (
        (None, {'fields': ('username', 'password', 'centers')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'role'),
        }),
    )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.user_permissions.clear()  # clear all permissions

        if obj.role == CustomUser.ROLE_OPERATOR:
            permissions = Permission.objects.filter(codename__in=[
                'can_edit_first_call', 'can_edit_second_call', 'can_add_students'
            ])  # get the specific permissions
            for permission in permissions:
                obj.user_permissions.add(permission)
        elif obj.role == CustomUser.ROLE_ADMIN:
            permissions = Permission.objects.exclude(
                codename__in=['can_access_admin'])  # get all permissions except 'can_access_admin' '
            for permission in permissions:
                obj.user_permissions.add(permission)

        return super(CustomUserAdmin, self).save_model(request, obj, form, change)


admin.site.register(CustomUser, CustomUserAdmin)

