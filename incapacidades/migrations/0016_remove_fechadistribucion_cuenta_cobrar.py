# Generated by Django 4.2.11 on 2024-05-21 19:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incapacidades', '0015_alter_fechadistribucion_empresa_valor_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fechadistribucion',
            name='cuenta_cobrar',
        ),
    ]
