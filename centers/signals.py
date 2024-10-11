from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Student


@receiver(post_delete, sender=Student)
def reorder_student_ids(sender, instance, **kwargs):
    students = Student.objects.filter(center=instance.center).order_by('custom_id')
    for index, student in enumerate(students, start=1):
        student.custom_id = index
        student.save(update_fields=['custom_id'])