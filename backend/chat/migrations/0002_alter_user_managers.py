# Generated by Django 4.2.6 on 2023-11-05 11:56

import chat.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', chat.models.UserManager()),
            ],
        ),
    ]
