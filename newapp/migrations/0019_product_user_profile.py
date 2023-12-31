# Generated by Django 4.2.3 on 2023-07-19 05:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("newapp", "0018_remove_product_user_profile"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="user_profile",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to="newapp.userprofile",
            ),
        ),
    ]
