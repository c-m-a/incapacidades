# Generated by Django 4.2.11 on 2024-05-12 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('incapacidades', '0003_alter_diagnostico_codigo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movimiento',
            name='genera_pago',
            field=models.BooleanField(default=False),
        ),
    ]