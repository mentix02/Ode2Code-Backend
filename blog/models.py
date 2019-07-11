import uuid

from vote.models import VoteModel

from django.db import models
from django.dispatch import receiver
from django.utils.text import slugify
from django.db.models.signals import pre_save

from author.models import Author


class Post(VoteModel, models.Model):

    body = models.TextField()
    title = models.CharField(max_length=100)
    draft = models.BooleanField(default=False)
    description = models.CharField(max_length=250)
    thumbnail = models.URLField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=250, blank=True, unique=True)

    author = models.ForeignKey(Author,
                               related_name='posts',
                               on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-timestamp', '-id')


# noinspection PyUnusedLocal
@receiver(pre_save, sender=Post)
def post_title_to_slug(sender, instance: Post = None, **kwargs):
    instance.slug = slugify(f'{instance.title}')
