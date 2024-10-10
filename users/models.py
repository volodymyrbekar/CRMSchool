from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from centers.models import Center


class CustomUser(AbstractUser):
    ROLE_ADMIN = 'admin'
    ROLE_OPERATOR = 'operator'

    ROLES = [
        (ROLE_ADMIN, 'Адміністратор'),
        (ROLE_OPERATOR, 'Оператор'),
    ]

    role = models.CharField(choices=ROLES, default=ROLE_OPERATOR, max_length=20)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    username = models.CharField(max_length=150, unique=True)
    centers = models.ManyToManyField(Center, blank=True)

    groups = models.ManyToManyField(Group, blank=True)
    user_permissions = models.ManyToManyField(Permission, blank=True)

    def has_access_to_center(self, center):
        return self.centers.filter(pk=center.pk).exists()

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = self.ROLE_ADMIN
        super(CustomUser, self).save(*args, **kwargs)
        is_new = self.pk is None  # check if the user is new
        # if is_new:
        # self.user_permissions.clear()  # clear all permissions

        if self.role == self.ROLE_OPERATOR:
            permissions = Permission.objects.filter(codename__in=[
                'can_edit_first_call', 'can_edit_second_call', 'can_add_students'
            ])  # get the specific permissions
            self.user_permissions.add(*permissions)
        elif self.role == self.ROLE_ADMIN:
            permissions = Permission.objects.exclude(codename__in='can_access_admin')  # get all permissions except 'can_access_admin'
            self.user_permissions.add(*permissions)

    class Meta:
        permissions = [
            ('can_edit_first_call', 'Can edit first call'),
            ('can_edit_second_call', 'Can edit second call'),
            ("can_add_students", "Can add students"),
            ("can_access_admin", "Can access Django admin"),
            ("can_add_centers", "Can add centers"),
            ("can_add_grouptrial", "Can add groups trial"),
            ("can_add_grouppermanent", "Can add groups permanent"),
        ]
