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

    def authenticate(self):
        self.authenticated = True
        self.user.is_staff = True
        self.user.save()
        self.save()

    class Meta:
        ordering = ('-pk',)


class Bookmark(models.Model):

    CHOICES = (
        ('series', 'Series'),
        ('tutorial', 'Tutorial'),
    )

    model_pk = models.BigIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    model_type = models.CharField(choices=CHOICES, max_length=8)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.author} - {self.model_type} : {self.model_pk}'


# noinspection PyUnusedLocal
@receiver(post_save, sender=User)
def author_generate_token(sender, instance: User = None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
