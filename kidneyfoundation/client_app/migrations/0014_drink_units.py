# Generated by Django 4.1.2 on 2022-12-01 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client_app', '0013_remove_report_drink_phosphorus_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Drink_Units',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('abbreviation', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'drink_units',
            },
        ),
    ]
