# Generated by Django 5.0.1 on 2024-09-29 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('centers', '0014_alter_center_unique_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='parent_full_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='first_call_satus',
            field=models.CharField(blank=True, choices=[('Так, прийдуть на пробне', 'Так, прийдуть на пробне'), ('Ні', 'Ні'), ('Думають', 'Думають'), ('Невірний номер', 'Невірний номер'), ('На наступний тиждень', 'На наступний тиждень'), ('Передзвонити пізніше', 'Передзвонити пізніше'), ('Примітка', 'Примітка'), ('Не беруть телефон', 'Не беруть телефон')], max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='trial_status',
            field=models.CharField(blank=True, choices=[('----', '----'), ('Так, був на пробному', 'Так, був на пробному'), ('Ні, не був', 'Ні, не був')], max_length=80, null=True),
        ),
    ]
