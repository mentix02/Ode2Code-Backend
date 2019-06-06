import uuid

from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from rest_framework.authtoken.models import Token


class Author(models.Model):

    bio = models.TextField(max_length=260)
    authenticated = models.BooleanField(default=False)
    secret_key = models.UUIDField(default=uuid.uuid4, blank=True)

    user = models.OneToOneField(User,
                                unique=True,
                                on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ('-pk',)


# noinspection PyUnusedLocal
@receiver(post_save, sender=User)
def author_generate_token(sender, instance: User = None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
