# Generated by Django 2.1 on 2019-07-03 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HeadHall', '0004_elevel_details'),
    ]

    operations = [
        migrations.AlterField(
            model_name='elevel',
            name='Email',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
