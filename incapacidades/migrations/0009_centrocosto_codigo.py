# Generated by Django 4.2.11 on 2024-05-03 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('incapacidades', '0008_alter_concepto_codigo_alter_diagnostico_codigo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='centrocosto',
            name='codigo',
            field=models.CharField(help_text='Escribe el codigo de centro de costos...', max_length=16, null=True, verbose_name='Codigo del centro de costos'),
        ),
    ]