# Generated by Django 5.2.1 on 2025-05-28 04:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='disc',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='payment.discount'),
        ),
    ]
