# Generated by Django 3.2.9 on 2021-11-18 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boxes', '0002_alter_box_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='BoxLimits',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('A1', models.FloatField()),
                ('V1', models.FloatField()),
                ('L1', models.FloatField()),
                ('L2', models.FloatField()),
            ],
            options={
                'db_table': 'limits',
            },
        ),
    ]
