# Generated by Django 4.1.7 on 2023-06-12 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_store_arboleda', '0006_remove_invoice_detail_cart_invoice_detail_book'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='author',
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, null=True)),
                ('books', models.ManyToManyField(to='book_store_arboleda.book')),
            ],
        ),
    ]