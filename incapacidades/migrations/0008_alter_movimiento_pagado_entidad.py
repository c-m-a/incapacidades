# Generated by Django 4.2.11 on 2024-05-16 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('incapacidades', '0007_claseincapacidad_dias_empresa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movimiento',
            name='pagado_entidad',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]