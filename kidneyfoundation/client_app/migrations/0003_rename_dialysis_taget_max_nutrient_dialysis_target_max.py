# Generated by Django 4.1.2 on 2022-11-30 22:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client_app', '0002_patient_sex'),
    ]

    operations = [
        migrations.RenameField(
            model_name='nutrient',
            old_name='dialysis_taget_max',
            new_name='dialysis_target_max',
        ),
    ]
