# Generated by Django 5.1.4 on 2025-04-02 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kpi_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kpi',
            name='amount',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='kpi',
            name='cases_received',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='kpi',
            name='cases_reported',
            field=models.IntegerField(default=0),
        ),
    ]
