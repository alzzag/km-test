# Generated by Django 2.0.2 on 2018-02-19 10:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cBase', '0004_client'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Client_old',
        ),
        migrations.RemoveField(
            model_name='client',
            name='age',
        ),
    ]
