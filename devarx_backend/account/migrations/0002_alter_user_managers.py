# Generated by Django 4.2.1 on 2023-08-14 08:43

import account.managers
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', account.managers.CustomUserManager()),
            ],
        ),
    ]
