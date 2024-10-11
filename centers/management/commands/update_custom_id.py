from django.core.management.base import BaseCommand
from centers.models import Center, Student


class Command(BaseCommand):
    help = 'Update custom_id for all students based on student_add_date'

    def handle(self, *args, **kwargs):
        centers = Center.objects.all()
        for center in centers:
            students = Student.objects.filter(center=center).order_by('student_add_date')
            custom_id = 1
            for student in students:
                student.custom_id = custom_id
                student.save(update_fields=['custom_id'])
                custom_id += 1
        self.stdout.write(self.style.SUCCESS('Successfully updated custom_id for all students'))