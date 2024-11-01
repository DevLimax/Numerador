# Generated by Django 5.1.2 on 2024-10-29 21:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('numerador', '0003_rename_ano_registros_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tipomodelo',
            name='ocorrencias',
        ),
        migrations.CreateModel(
            name='Numerador',
            fields=[
                ('id_numerador', models.AutoField(primary_key=True, serialize=False)),
                ('contagem', models.IntegerField(default=0)),
                ('modelo_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contador', to='numerador.tipomodelo')),
                ('unidade_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contador', to='numerador.unidades')),
            ],
        ),
    ]
