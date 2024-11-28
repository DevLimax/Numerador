# Generated by Django 5.1.3 on 2024-11-15 06:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('numerador', '0004_rename_categoria_crime_id_tipocrimes_categoria_crime'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='registros',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registros', to=settings.AUTH_USER_MODEL),
        ),
    ]
