# Generated by Django 5.1.4 on 2025-02-19 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documentos', '0002_remove_documento_arquivo_alter_documento_tipo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documento',
            name='data_documento',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='documento',
            name='data_publicacao',
            field=models.DateTimeField(),
        ),
    ]
