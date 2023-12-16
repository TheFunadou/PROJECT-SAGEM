# Generated by Django 4.2.4 on 2023-12-14 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finanzas', '0004_tabla_info_derechos_delete_tabla_derechos'),
    ]

    operations = [
        migrations.CreateModel(
            name='tabla_derechos',
            fields=[
                ('id', models.PositiveSmallIntegerField(primary_key=True, serialize=False)),
                ('categoria', models.CharField(max_length=200)),
                ('nombre_derecho', models.CharField(max_length=200)),
                ('precio', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ],
            options={
                'unique_together': {('id', 'categoria', 'nombre_derecho')},
            },
        ),
        migrations.DeleteModel(
            name='tabla_info_derechos',
        ),
    ]