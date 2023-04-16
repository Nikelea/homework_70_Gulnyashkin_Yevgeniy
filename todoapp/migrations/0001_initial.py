# Generated by Django 4.0 on 2022-01-20 04:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TaskStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=10, verbose_name='Статус')),
            ],
        ),
        migrations.CreateModel(
            name='TaskType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=10, verbose_name='Тип задачи')),
            ],
        ),
        migrations.CreateModel(
            name='TodoTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=25, verbose_name='Название задачи')),
                ('description', models.TextField(blank=True, max_length=500, null=True, verbose_name='Описание задачи')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Время изменения')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='todoapp.taskstatus')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='todoapp.tasktype')),
            ],
        ),
    ]
