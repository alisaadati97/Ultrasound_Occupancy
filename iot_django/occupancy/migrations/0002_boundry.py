# Generated by Django 3.1.3 on 2021-09-26 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('occupancy', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Boundry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
            ],
        ),
    ]
