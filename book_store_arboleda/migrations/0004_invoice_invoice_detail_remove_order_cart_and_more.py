# Generated by Django 4.1.7 on 2023-05-14 17:29

import book_store_arboleda.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('book_store_arboleda', '0003_payment_order_author'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('status_revision', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Invoice_detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.RemoveField(
            model_name='order',
            name='cart',
        ),
        migrations.RemoveField(
            model_name='order',
            name='user',
        ),
        migrations.RenameField(
            model_name='book',
            old_name='Author',
            new_name='author',
        ),
        migrations.RemoveField(
            model_name='book',
            name='Edition',
        ),
        migrations.RemoveField(
            model_name='book',
            name='Price',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='cart',
        ),
        migrations.AddField(
            model_name='book',
            name='copies_in_stock',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='book',
            name='total_copies',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='cart',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='cart',
            name='user',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Author',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.AddField(
            model_name='invoice_detail',
            name='Book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book_store_arboleda.book'),
        ),
        migrations.AddField(
            model_name='invoice_detail',
            name='invoice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book_store_arboleda.invoice'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='payment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book_store_arboleda.payment'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='book',
            name='price',
            field=models.DecimalField(decimal_places=2, default=book_store_arboleda.models.default_price, max_digits=10),
        ),
    ]