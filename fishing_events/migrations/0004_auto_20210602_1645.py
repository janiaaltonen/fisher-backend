# Generated by Django 3.2.3 on 2021-06-02 16:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fishing_events', '0003_auto_20210602_1639'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fishingtechnique',
            old_name='key',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='fishspecies',
            old_name='key',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='lure',
            old_name='key',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='weatheroption',
            old_name='key',
            new_name='name',
        ),
    ]