# Generated by Django 5.1.4 on 2025-01-08 15:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('efetivo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cadastro_adicional',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_adicional', models.IntegerField(choices=[(1, '01'), (2, '02'), (3, '03'), (4, '04'), (5, '05'), (6, '06'), (7, '07'), (8, '08')])),
                ('data_ultimo_adicional', models.DateField()),
                ('numero_lp', models.IntegerField(choices=[(1, '01'), (2, '02'), (3, '03'), (4, '04'), (5, '05'), (6, '06'), (7, '07'), (8, '08')])),
                ('data_ultimo_lp', models.DateField()),
                ('proximo_adicional', models.DateField(blank=True, null=True)),
                ('mes_proximo_adicional', models.IntegerField(blank=True, null=True)),
                ('ano_proximo_adicional', models.IntegerField(blank=True, null=True)),
                ('dias_desconto_adicional', models.IntegerField(default=0)),
                ('proximo_lp', models.DateField()),
                ('mes_proximo_lp', models.IntegerField()),
                ('ano_proximo_lp', models.IntegerField()),
                ('dias_desconto_lp', models.IntegerField(default=0)),
                ('status_adicional', models.CharField(max_length=20)),
                ('status_lp', models.CharField(max_length=20)),
                ('cadastro', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='efetivo.cadastro')),
            ],
        ),
    ]
