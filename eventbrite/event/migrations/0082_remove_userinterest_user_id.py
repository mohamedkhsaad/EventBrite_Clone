# Generated by Django 4.2b1 on 2023-04-27 13:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0081_userinterest_user_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinterest',
            name='User_id',
        ),
    ]
