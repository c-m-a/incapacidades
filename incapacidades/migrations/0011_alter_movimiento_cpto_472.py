# Generated by Django 4.2.11 on 2024-05-16 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('incapacidades', '0010_alter_movimiento_mayor_valor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movimiento',
            name='cpto_472',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
