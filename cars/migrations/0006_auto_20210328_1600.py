# Generated by Django 3.1.7 on 2021-03-28 16:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0005_auto_20210328_0723'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='car',
            name='avg_rating',
        ),
        migrations.RemoveField(
            model_name='car',
            name='rates_number',
        ),
    ]
