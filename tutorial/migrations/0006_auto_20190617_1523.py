# Generated by Django 2.2.2 on 2019-06-17 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutorial', '0005_auto_20190617_1523'),
    ]

    operations = [
        migrations.AlterField(
            model_name='series',
            name='name',
            field=models.CharField(max_length=160),
        ),
    ]
