# Generated by Django 4.1.3 on 2023-04-20 18:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recommendation',
            name='avatar',
        ),
    ]
