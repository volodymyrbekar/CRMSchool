# Generated by Django 5.0.1 on 2024-02-27 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('centers', '0006_alter_student_add_to_group_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='first_call',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='first_call_satus',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='school',
            field=models.TextField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='second_call',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='second_call_satus',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='trial_registration',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='trial_status',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
    ]
