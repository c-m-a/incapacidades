# Generated by Django 4.2.11 on 2024-05-16 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('incapacidades', '0008_alter_movimiento_pagado_entidad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movimiento',
            name='llevada_gasto',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
