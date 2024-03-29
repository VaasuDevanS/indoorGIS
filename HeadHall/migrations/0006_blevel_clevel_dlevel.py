# Generated by Django 2.1 on 2019-07-03 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HeadHall', '0005_auto_20190703_1813'),
    ]

    operations = [
        migrations.CreateModel(
            name='BLevel',
            fields=[
                ('OBJECTID', models.IntegerField(editable=False, primary_key=True, serialize=False)),
                ('PlaceNode', models.IntegerField()),
                ('PlaceName', models.CharField(blank=True, max_length=50, null=True)),
                ('PersonName', models.CharField(blank=True, max_length=50, null=True)),
                ('Contact', models.CharField(blank=True, max_length=20, null=True)),
                ('Email', models.CharField(blank=True, max_length=50, null=True)),
                ('Details', models.CharField(blank=True, max_length=200, null=True)),
                ('geometry', models.TextField(editable=False)),
            ],
            options={
                'verbose_name_plural': 'BLevel',
            },
        ),
        migrations.CreateModel(
            name='CLevel',
            fields=[
                ('OBJECTID', models.IntegerField(editable=False, primary_key=True, serialize=False)),
                ('PlaceNode', models.IntegerField()),
                ('PlaceName', models.CharField(blank=True, max_length=50, null=True)),
                ('PersonName', models.CharField(blank=True, max_length=50, null=True)),
                ('Contact', models.CharField(blank=True, max_length=20, null=True)),
                ('Email', models.CharField(blank=True, max_length=50, null=True)),
                ('Details', models.CharField(blank=True, max_length=200, null=True)),
                ('geometry', models.TextField(editable=False)),
            ],
            options={
                'verbose_name_plural': 'CLevel',
            },
        ),
        migrations.CreateModel(
            name='DLevel',
            fields=[
                ('OBJECTID', models.IntegerField(editable=False, primary_key=True, serialize=False)),
                ('PlaceNode', models.IntegerField()),
                ('PlaceName', models.CharField(blank=True, max_length=50, null=True)),
                ('PersonName', models.CharField(blank=True, max_length=50, null=True)),
                ('Contact', models.CharField(blank=True, max_length=20, null=True)),
                ('Email', models.CharField(blank=True, max_length=50, null=True)),
                ('Details', models.CharField(blank=True, max_length=200, null=True)),
                ('geometry', models.TextField(editable=False)),
            ],
            options={
                'verbose_name_plural': 'DLevel',
            },
        ),
    ]
