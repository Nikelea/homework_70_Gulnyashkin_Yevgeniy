# Generated by Django 4.0 on 2022-02-28 09:41

from django.db import migrations, models
import django.db.models.deletion
import todoapp.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('git_hub', models.CharField(blank=True, max_length=500, null=True, verbose_name='Ссылка на github')),
                ('bio', models.TextField(blank=True, max_length=500, null=True, validators=[todoapp.validators.WordLengthValidator(50)], verbose_name='О себе')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='user_pics', verbose_name='Аватар')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='auth.user', verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Профиль',
                'verbose_name_plural': 'Профили',
            },
        ),
    ]
