# Generated by Django 3.2 on 2023-02-26 11:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='user',
            name='unique_name',
        ),
    ]