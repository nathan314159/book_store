# Generated by Django 4.1.7 on 2023-04-20 13:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20230419_0940'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]
