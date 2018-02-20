# Generated by Django 2.0.2 on 2018-02-19 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cBase', '0003_auto_20180219_1352'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('surname', models.CharField(max_length=32)),
                ('age', models.SmallIntegerField()),
                ('birthday', models.DateField()),
                ('photo', models.FileField(upload_to='photo')),
            ],
        ),
    ]
