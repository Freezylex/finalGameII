# Generated by Django 3.1 on 2021-05-13 13:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Game', '0011_auto_20210513_1612'),
    ]

    operations = [
        migrations.AddField(
            model_name='factor',
            name='UserID',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='Game.player'),
            preserve_default=False,
        ),
    ]
