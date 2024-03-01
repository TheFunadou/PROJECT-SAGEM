# Generated by Django 4.2.4 on 2024-02-28 10:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catastro', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='fc_datos_const',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('etiqueta', models.CharField(max_length=1)),
                ('tipo_c', models.PositiveSmallIntegerField()),
                ('estado', models.PositiveSmallIntegerField()),
                ('terreno', models.PositiveSmallIntegerField()),
                ('antiguedad', models.PositiveSmallIntegerField()),
                ('area_d_m2', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='fc_datos_construccion_valores',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor_terreno', models.BigIntegerField()),
                ('valor_construccion', models.BigIntegerField()),
                ('valor_catastral', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='fc_datos_documento_predio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lugar_expedicion', models.CharField(max_length=35)),
                ('td', models.PositiveSmallIntegerField()),
                ('no_documento', models.PositiveSmallIntegerField()),
                ('dia', models.PositiveSmallIntegerField()),
                ('mes', models.PositiveSmallIntegerField()),
                ('año', models.PositiveSmallIntegerField()),
                ('no_notaria', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='fc_datos_generales',
            fields=[
                ('folio', models.BigAutoField(primary_key=True, serialize=False)),
                ('tipo_mov', models.CharField(max_length=2)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('clave_catastral', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catastro.datos_contribuyentes')),
            ],
        ),
        migrations.CreateModel(
            name='fc_datos_inscripcion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=15)),
                ('bajo_numero', models.PositiveSmallIntegerField()),
                ('tomo', models.PositiveSmallIntegerField()),
                ('dia', models.PositiveSmallIntegerField()),
                ('mes', models.PositiveSmallIntegerField()),
                ('year', models.PositiveSmallIntegerField()),
                ('zona', models.PositiveSmallIntegerField()),
                ('folio_fc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catastro.fc_datos_generales')),
            ],
        ),
        migrations.CreateModel(
            name='fc_datos_predio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_avaluo', models.PositiveSmallIntegerField()),
                ('fraccionamiento', models.PositiveSmallIntegerField()),
                ('traslado_dominio', models.PositiveSmallIntegerField()),
                ('regimen', models.PositiveSmallIntegerField()),
                ('tenencia', models.PositiveSmallIntegerField()),
                ('estado_fisico', models.PositiveSmallIntegerField()),
                ('codigo_uso', models.PositiveSmallIntegerField()),
                ('tipo_posecion', models.PositiveSmallIntegerField()),
                ('num_emision', models.PositiveSmallIntegerField()),
                ('tipo_predio', models.PositiveSmallIntegerField()),
                ('uso_predio', models.PositiveSmallIntegerField()),
                ('folio_fc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catastro.fc_datos_generales')),
            ],
        ),
        migrations.CreateModel(
            name='fc_datos_terrenos_rurales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_suelo', models.PositiveSmallIntegerField()),
                ('valor_has', models.PositiveSmallIntegerField()),
                ('a', models.PositiveSmallIntegerField()),
                ('c', models.PositiveSmallIntegerField()),
                ('sup_has', models.PositiveSmallIntegerField()),
                ('top', models.CharField(max_length=2)),
                ('vias_c', models.CharField(max_length=2)),
                ('folio_fc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catastro.fc_datos_generales')),
            ],
        ),
        migrations.CreateModel(
            name='fc_datos_terrenos_rurales_sup_total',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sup_t_has', models.PositiveSmallIntegerField()),
                ('a', models.PositiveSmallIntegerField()),
                ('c', models.PositiveSmallIntegerField()),
                ('folio_fc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catastro.fc_datos_generales')),
            ],
        ),
        migrations.CreateModel(
            name='fc_datos_terrenos_urbanos_suburbanos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor_m2_1', models.PositiveSmallIntegerField()),
                ('area', models.PositiveSmallIntegerField()),
                ('c', models.PositiveSmallIntegerField()),
                ('valor_m2_2', models.PositiveSmallIntegerField()),
                ('frente', models.PositiveSmallIntegerField()),
                ('profundidad', models.PositiveSmallIntegerField()),
                ('folio_fc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catastro.fc_datos_generales')),
            ],
        ),
        migrations.CreateModel(
            name='fc_dtus_demeritos_predios_urbanos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=35)),
                ('valor', models.PositiveSmallIntegerField()),
                ('folio_fc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catastro.fc_datos_generales')),
            ],
        ),
        migrations.CreateModel(
            name='fc_dtus_incremento_por_esquina',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=1)),
                ('valor', models.PositiveSmallIntegerField()),
                ('folio_fc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catastro.fc_datos_generales')),
            ],
        ),
        migrations.DeleteModel(
            name='datos_documento_predio',
        ),
        migrations.DeleteModel(
            name='datos_inscripcion',
        ),
        migrations.DeleteModel(
            name='datos_predio_ficha',
        ),
        migrations.DeleteModel(
            name='demeritos_predios_urbanos',
        ),
        migrations.RemoveField(
            model_name='ficha_datos_construcciones',
            name='fk_clave_catastral',
        ),
        migrations.DeleteModel(
            name='incrementos_esquina_urbanos',
        ),
        migrations.DeleteModel(
            name='terrenos_rurales',
        ),
        migrations.DeleteModel(
            name='terrenos_rurales_superficietotal',
        ),
        migrations.DeleteModel(
            name='terrenos_urbanos_suburbanos',
        ),
        migrations.DeleteModel(
            name='valores_catastro',
        ),
        migrations.DeleteModel(
            name='ficha_datos_construcciones',
        ),
        migrations.AddField(
            model_name='fc_datos_documento_predio',
            name='folio_fc',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catastro.fc_datos_generales'),
        ),
        migrations.AddField(
            model_name='fc_datos_construccion_valores',
            name='folio_fc',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catastro.fc_datos_generales'),
        ),
        migrations.AddField(
            model_name='fc_datos_const',
            name='folio_fc',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catastro.fc_datos_generales'),
        ),
        migrations.AlterUniqueTogether(
            name='fc_datos_const',
            unique_together={('folio_fc', 'etiqueta')},
        ),
    ]
