# Generated by Django 2.2.2 on 2019-06-14 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutorial', '0002_auto_20190611_1137'),
    ]

    operations = [
        migrations.AddField(
            model_name='series',
            name='thumbnail',
            field=models.URLField(blank=True, null=True),
        ),
    ]
