# Generated by Django 3.2.3 on 2021-06-08 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fishing_events', '0007_alter_fishingevent_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fishingevent',
            name='air_temp',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='fishingevent',
            name='end_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='fishingevent',
            name='persons',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='fishingevent',
            name='start_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='fishingevent',
            name='water_temp',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='fishingevent',
            name='wind',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
