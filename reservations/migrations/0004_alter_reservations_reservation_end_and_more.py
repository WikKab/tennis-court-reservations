# Generated by Django 4.0.5 on 2022-07-02 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0003_alter_profile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservations',
            name='reservation_end',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='reservations',
            name='reservation_start',
            field=models.DateTimeField(),
        ),
    ]
