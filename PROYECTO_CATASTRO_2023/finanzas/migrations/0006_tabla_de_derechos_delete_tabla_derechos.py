# Generated by Django 4.2.4 on 2023-12-14 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finanzas', '0005_tabla_derechos_delete_tabla_info_derechos'),
    ]

    operations = [
        migrations.CreateModel(
            name='tabla_de_derechos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_derecho', models.PositiveSmallIntegerField()),
                ('serial', models.PositiveSmallIntegerField()),
                ('categoria', models.CharField(max_length=200)),
                ('nombre_derecho', models.CharField(max_length=200)),
                ('precio', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ],
            options={
                'unique_together': {('id', 'serial')},
            },
        ),
        migrations.DeleteModel(
            name='tabla_derechos',
        ),
    ]