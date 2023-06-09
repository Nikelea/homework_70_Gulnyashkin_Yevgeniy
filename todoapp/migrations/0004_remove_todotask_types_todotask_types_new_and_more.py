# Generated by Django 4.0 on 2022-01-25 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0003_todotype_remove_todotask_type_todotask_types_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='todotask',
            name='types',
        ),
        migrations.AddField(
            model_name='todotask',
            name='types_new',
            field=models.ManyToManyField(blank=True, related_name='types', to='todoapp.TaskType', verbose_name='Тип'),
        ),
        migrations.AddField(
            model_name='todotask',
            name='types_old',
            field=models.ManyToManyField(blank=True, related_name='types_old', through='todoapp.TodoType', to='todoapp.TaskType', verbose_name='Тип'),
        ),
    ]
