# Generated by Django 5.1.6 on 2025-02-21 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0007_tag_order_tag"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="order",
            name="tag",
        ),
        migrations.AddField(
            model_name="product",
            name="tag",
            field=models.ManyToManyField(to="accounts.tag"),
        ),
    ]
