# Generated by Django 5.0.1 on 2024-02-17 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('centers', '0004_alter_student_add_to_group_alter_student_first_call_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='trial_status',
            field=models.TextField(blank=True, max_length=20, null=True),
        ),
    ]
