# Generated by Django 4.2.17 on 2025-03-14 05:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0009_bookinstance_notes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookinstance',
            name='notes',
        ),
    ]
