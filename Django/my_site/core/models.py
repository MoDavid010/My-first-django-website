from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from .validators import validate_birth_date


def user_avatar_path(instance, filename):
    user_id = instance.id
    return "user_avatars/user-{}/{}".format(user_id, filename)


class CustomUser(AbstractUser):
    birth_date = models.DateField(blank=True, null=True, validators=[validate_birth_date, ])
    about = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to=user_avatar_path)
    friends = models.ManyToManyField('self', blank=True)

    def get_absolute_url(self):
        return reverse('core:profile', kwargs={'user_id': self.pk})