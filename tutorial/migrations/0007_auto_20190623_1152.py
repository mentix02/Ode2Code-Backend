# Generated by Django 2.2.2 on 2019-06-23 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutorial', '0006_auto_20190617_1523'),
    ]

    operations = [
        migrations.AlterField(
            model_name='series',
            name='type_of',
            field=models.CharField(choices=[('other', 'Other'), ('design', 'Design'), ('language', 'Language'), ('algorithms', 'Algorithms'), ('technology', 'Technology'), ('miscellaneous', 'Miscellaneous'), ('data_structures', 'Data Structures')], max_length=50),
        ),
    ]
