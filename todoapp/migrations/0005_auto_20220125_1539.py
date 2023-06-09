# Generated by Django 4.0 on 2022-01-25 09:39

from django.db import migrations


def transfer_types(apps, schema_editor):
    Task = apps.get_model('todoapp.TodoTask')
    for task in Task.objects.all():
        task.types_new.set(task.types_old.all())


def rollback_transfer(apps, schema_editor):
    Task = apps.get_model('webapp.task')
    for task in Task.objects.all():
        task.types_old.set(task.types_new.all())


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0004_remove_todotask_types_todotask_types_new_and_more'),
    ]

    operations = [
        migrations.RunPython(code=transfer_types, reverse_code=rollback_transfer)
    ]
