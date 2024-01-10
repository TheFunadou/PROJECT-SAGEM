# Generated by Django 4.2.4 on 2023-12-16 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ReportDefinition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_definition', models.TextField()),
                ('report_type', models.CharField(max_length=100, unique=True)),
                ('remark', models.TextField(blank=True, null=True)),
                ('last_modified_at', models.DateTimeField()),
            ],
            options={
                'db_table': 'report_definition',
            },
        ),
        migrations.CreateModel(
            name='ReportRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=36)),
                ('report_definition', models.TextField()),
                ('data', models.TextField()),
                ('is_test_data', models.BooleanField()),
                ('pdf_file', models.BinaryField(null=True)),
                ('pdf_file_size', models.IntegerField(null=True)),
                ('created_on', models.DateTimeField()),
            ],
            options={
                'db_table': 'report_request',
            },
        ),
    ]
