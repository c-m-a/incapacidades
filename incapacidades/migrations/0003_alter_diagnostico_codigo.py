# Generated by Django 4.2.11 on 2024-05-08 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('incapacidades', '0002_alter_eps_codigo_alter_eps_nit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diagnostico',
            name='codigo',
            field=models.CharField(help_text='Escribe el codigo del diagnostico...', max_length=16, unique=True, verbose_name='Codigo del diagnostico'),
        ),
    ]