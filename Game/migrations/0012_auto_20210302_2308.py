# Generated by Django 3.1 on 2021-03-02 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Game', '0011_auto_20210302_2242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='ID',
            field=models.IntegerField(auto_created=True, unique=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='Name',
            field=models.CharField(max_length=200, primary_key=True, serialize=False, unique=True, verbose_name='name'),
        ),
    ]
