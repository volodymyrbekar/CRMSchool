from django.db import models
from django.db.models import Q
from django.conf import settings

from .choices import CHOICES_FIRST_CALL_STATUS, CHOICES_TRIAL_STATUS, CHOICES_FIRST_CALL_OPERATOR

User = settings.AUTH_USER_MODEL


class Center(models.Model):
    # user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    center_name = models.CharField(max_length=300)
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_student_num(self):
        return self.student_set.all().count()

    def __str__(self):
        return(f"{self.center_name} {self.location}")


class GroupTrial(models.Model):
    center = models.ForeignKey(Center, on_delete=models.CASCADE)
    group_name = models.CharField(max_length=100)

    def __str__(self):
        return(f"{self.group_name}")


class GroupPermanent(models.Model):
    center = models.ForeignKey(Center, on_delete=models.CASCADE)
    group_name = models.CharField(max_length=100)

    def __str__(self):
        return(f"{self.group_name}")


class Student(models.Model):
    center = models.ForeignKey(Center, on_delete=models.CASCADE)
    student_full_name = models.CharField(max_length=200, blank=True, null=True)
    student_phone_number = models.CharField(max_length=30, blank=True, null=True)
    parent_phone_number = models.CharField(max_length=30, blank=True, null=True)
    school = models.TextField(max_length=50, blank=True, null=True)
    class_number = models.PositiveIntegerField(default=1, choices=((i, i) for i in range(1, 12)))
    student_add_date = models.DateTimeField(auto_now_add=True)

    first_call = models.CharField(max_length=80, blank=True, null=True, choices=CHOICES_FIRST_CALL_OPERATOR)
    first_call_satus = models.CharField(max_length=80, blank=True, null=True, choices=CHOICES_FIRST_CALL_STATUS)
    trial_registration = models.CharField(max_length=80, blank=True, null=True)  # trial_registration запис на пробне
    trial_status = models.CharField(max_length=80, blank=True, null=True, choices=CHOICES_TRIAL_STATUS)  # чи був на пробному?
    comment_first_call = models.CharField(max_length=250, blank=True, null=True)

    second_call = models.CharField(max_length=80, blank=True, null=True)
    second_call_satus = models.CharField(max_length=80, blank=True, null=True)
    add_to_group = models.CharField(max_length=100, blank=True, null=True)
    comment_second_call = models.CharField(max_length=250, blank=True, null=True)

    # def clean_fields(self, exclude=None):
    #     for field in self._meta.fields:
    #         value = getattr(self, field.attname)
    #         if value is None:
    #             setattr(self, field.attname, '')
    #     super().clean_fields(exclude=exclude)


    def __str__(self):
        return(f"{self.student_full_name} {self.student_phone_number} {self.parent_phone_number} {self.school}")



# class CenterQuerySet(models.QuerySet):
#     def search(self, query=None):
#         if query is None or query == "":
#             return self.none()
#         lookups = Q(center_name__icontains=query) | Q(location__icontains=query)
#         return self.filter(lookups)
#
#
# class CenterManager(models.Manager):
#     def get_queryset(self):
#         return CenterQuerySet(self.model, using=self._db)
#
#     def search(self, query=None):
#         return self.get_queryset().search(query=query)