# Generated by Django 5.1.4 on 2025-02-19 14:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Documento',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('data_publicacao', models.DateField()),
                ('data_documento', models.DateField()),
                ('numero_documento', models.CharField(max_length=100)),
                ('assunto', models.CharField(max_length=200)),
                ('descricao', models.TextField()),
                ('assinada_por', models.CharField(max_length=100)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('arquivo', models.FileField(upload_to='documentos/')),
                ('tipo', models.CharField(choices=[('PDF', 'PDF'), ('VIDEO', 'Vídeo'), ('AUDIO', 'Áudio'), ('DOC', 'Documento'), ('SHEET', 'Planilha'), ('IMAGE', 'Imagem'), ('TEXT', 'Texto'), ('OUTRO', 'Outro')], default='OUTRO', max_length=10)),
                ('usuario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
