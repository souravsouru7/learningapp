# Generated by Django 4.2.3 on 2023-07-19 04:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("newapp", "0015_product_user"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="user",
        ),
    ]
