from django.db import models
from django.contrib.auth.models import User


class Image(models.Model):
    image = models.ImageField(
        upload_to='media/',
        blank=False,
        null=False)
    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              blank=False,
                              null=False,
                              related_name='+')
    public = models.BooleanField(default=False)
