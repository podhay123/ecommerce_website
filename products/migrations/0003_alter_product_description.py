# Generated by Django 4.2.5 on 2023-11-14 18:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0002_product_description_product_price_alter_product_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="description",
            field=models.TextField(default=None, max_length=100),
        ),
    ]
