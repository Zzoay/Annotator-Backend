# Generated by Django 3.1.14 on 2022-06-16 04:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='creator',
        ),
        migrations.RemoveField(
            model_name='user',
            name='modifier',
        ),
    ]
