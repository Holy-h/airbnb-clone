# Generated by Django 2.2.5 on 2020-03-01 14:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0004_bookedday'),
    ]

    operations = [
        migrations.DeleteModel(
            name='BookedDay',
        ),
    ]
