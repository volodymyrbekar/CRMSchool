from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Student


@receiver(post_delete, sender=Student)
def reorder_student_ids(sender, instance, **kwargs):
    students = Student.objects.all().order_by('id')
    for index, student in enumerate(students, start=1):
        student.order = index  # Assuming there is an 'order' field to store the order
        student.save(update_fields=['order'])