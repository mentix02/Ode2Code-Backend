# Generated by Django 2.2.4 on 2019-08-16 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutorial', '0007_auto_20190623_1152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='series',
            name='type_of',
            field=models.CharField(choices=[('other', 'Other'), ('design', 'Design'), ('language', 'Language'), ('algorithms', 'Algorithms'), ('technology', 'Technology'), ('miscellaneous', 'Miscellaneous'), ('data-structures', 'Data Structures')], max_length=50),
        ),
    ]
