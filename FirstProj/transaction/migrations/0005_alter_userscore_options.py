# Generated by Django 4.2.4 on 2023-09-09 10:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0004_alter_userscore_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userscore',
            options={'permissions': [('Has_score_permission', 'Has score permission')]},
        ),
    ]
