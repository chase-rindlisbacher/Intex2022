# Generated by Django 4.1.2 on 2022-12-02 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client_app', '0017_report_food_phosphorus_report_food_potassium_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='report_drink',
            name='phosphorus',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='report_drink',
            name='potassium',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='report_drink',
            name='protein',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='report_drink',
            name='sodium',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='report_drink',
            name='water',
            field=models.FloatField(default=0),
        ),
    ]