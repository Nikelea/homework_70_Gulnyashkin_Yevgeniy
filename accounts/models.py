from django.db import models
from django.contrib.auth import get_user_model
from todoapp.validators import WordLengthValidator


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), related_name='profile', on_delete=models.CASCADE, verbose_name='Пользователь')
    git_hub = models.CharField(max_length=500, null=True, blank=True, verbose_name='Ссылка на github')
    bio = models.TextField(max_length=500, null=True, blank=True, verbose_name='О себе', validators=[WordLengthValidator(50)])
    avatar = models.ImageField(null=True, blank=True, upload_to='user_pics', verbose_name='Аватар')

    def __str__(self):
        return self.user.get_full_name() + "'s Profile"

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
