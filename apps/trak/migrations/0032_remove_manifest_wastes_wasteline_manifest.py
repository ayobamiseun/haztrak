# Generated by Django 4.0.4 on 2022-05-20 20:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trak', '0031_alter_wasteline_discrepancy_info'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='manifest',
            name='wastes',
        ),
        migrations.AddField(
            model_name='wasteline',
            name='manifest',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='trak.manifest'),
            preserve_default=False,
        ),
    ]
