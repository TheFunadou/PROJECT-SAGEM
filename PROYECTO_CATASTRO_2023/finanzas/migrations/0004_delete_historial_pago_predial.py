# Generated by Django 4.2.4 on 2023-10-12 02:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finanzas', '0003_alter_historial_pago_predial_cajero_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='historial_pago_predial',
        ),
    ]
