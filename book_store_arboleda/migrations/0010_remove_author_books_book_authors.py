# Generated by Django 4.1.7 on 2023-06-14 00:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_store_arboleda', '0009_alter_author_books'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='books',
        ),
        migrations.AddField(
            model_name='book',
            name='authors',
            field=models.ManyToManyField(to='book_store_arboleda.author'),
        ),
    ]
