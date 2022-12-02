# Generated by Django 4.1.2 on 2022-12-02 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client_app', '0018_report_drink_phosphorus_report_drink_potassium_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='food_item',
            name='water',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='report_food',
            name='water',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='food_item',
            name='phosphorus',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='food_item',
            name='potassium',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='food_item',
            name='protein',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='food_item',
            name='sodium',
            field=models.FloatField(default=0),
        ),
    ]
