import uuid
import typing

from django.db import models
from django.dispatch import receiver
from django.utils.text import slugify
from django.db.models.signals import pre_save

from author.models import Author


class Series(models.Model):

    CHOICES: typing.List[typing.Tuple[str, str]] = [
        ('design', 'Design'),
        ('language', 'Language'),
        ('algorithms', 'Algorithms'),
        ('technology', 'Technology'),
        ('miscellaneous', 'Miscellaneous'),
        ('data_structures', 'Data Structures'),
    ]

    name = models.CharField(max_length=160)
    description = models.TextField(max_length=300)
    timestamp = models.DateTimeField(auto_now_add=True)
    type_of = models.CharField(choices=CHOICES, max_length=20)
    creator = models.ForeignKey(Author, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=200, blank=True, unique=True)

    def get_tutorials(self):
        return self.tutorials.filter(draft=False)

    def get_tutorial_count(self):
        return self.tutorials.filter(draft=False).count()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Series'
        verbose_name_plural = 'Series'
        ordering = ('-timestamp', '-pk')


class Tutorial(models.Model):

    content = models.TextField()
    title = models.CharField(max_length=100)
    draft = models.BooleanField(default=False)
    description = models.CharField(max_length=250)
    timestamp = models.DateTimeField(auto_now_add=True)
    number = models.PositiveSmallIntegerField(default=1)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=250, blank=True, unique=True)

    series = models.ForeignKey(Series,
                               null=True,
                               blank=True,
                               related_name='tutorials',
                               on_delete=models.CASCADE)

    author = models.ForeignKey(Author,
                               related_name='tutorials',
                               on_delete=models.CASCADE)

    class Meta:
        ordering = ('-timestamp', '-id')

    def __str__(self):
        return self.title


# noinspection PyUnusedLocal
@receiver(pre_save, sender=Tutorial)
def tutorial_title_to_slug(sender, instance: Tutorial = None, **kwargs):
    instance.slug = slugify(f'{instance.title}')

# noinspection PyUnusedLocal
@receiver(pre_save, sender=Series)
def series_title_to_slug(sender, instance: Series = None, **kwargs):
    instance.slug = slugify(f'{instance.name}')
