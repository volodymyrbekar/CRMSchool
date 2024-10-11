from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.crypto import get_random_string
from crmschool.settings import ALLOWED_HOSTS

from .choices import CHOICES_FIRST_CALL_STATUS, CHOICES_TRIAL_STATUS

User = settings.AUTH_USER_MODEL


class Center(models.Model):
    center_name = models.CharField(max_length=300)
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    unique_link = models.URLField(default=None, blank=True, null=True)

    def generate_unique_link(self):
        token = get_random_string(20)
        self.unique_link = f"https://www.webuniverseua.com:8085/centers/{self.pk}/students/create/{token}/"
        self.save(update_fields=['unique_link'])

    def deactivate_unique_link(self):
        self.unique_link = None
        self.save()

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
    parent_full_name = models.CharField(max_length=200, blank=True, null=True)
    school = models.TextField(max_length=50, blank=True, null=True)
    class_number = models.PositiveIntegerField(default=1, choices=((i, i) for i in range(1, 12)))
    student_add_date = models.DateTimeField(auto_now_add=True)
    order = models.PositiveIntegerField(default=0)
    custom_id = models.IntegerField(default=0)

    first_call = models.CharField(max_length=80, blank=True, null=True)
    first_call_status = models.CharField(max_length=80, blank=True, null=True, choices=CHOICES_FIRST_CALL_STATUS)
    trial_registration = models.ForeignKey(GroupTrial, on_delete=models.SET_NULL, null=True, blank=True)  # trial_registration запис на пробне
    trial_status = models.CharField(max_length=80, blank=True, null=True, choices=CHOICES_TRIAL_STATUS)  # чи був на пробному?
    comment_first_call = models.CharField(max_length=250, blank=True, null=True)

    second_call = models.CharField(max_length=80, blank=True, null=True)
    second_call_status = models.CharField(max_length=80, blank=True, null=True)
    add_to_group = models.ForeignKey(GroupPermanent, on_delete=models.SET_NULL, null=True, blank=True)
    comment_second_call = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return(f"{self.student_full_name} {self.student_phone_number} {self.parent_phone_number} {self.school}")

    def save(self, *args, **kwargs):
        if not self.pk:  # If the student is new
            last_student = Student.objects.filter(center=self.center).order_by('custom_id').last()
            if last_student:
                self.custom_id = last_student.custom_id + 1
            else:
                self.custom_id = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        center_students = Student.objects.filter(center=self.center).order_by('custom_id')
        for student in center_students:
            if student.custom_id > self.custom_id:
                student.custom_id -= 1
                student.save(update_fields=['custom_id'])
        super().delete(*args, **kwargs)