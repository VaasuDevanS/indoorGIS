# Generated by Django 2.1 on 2019-06-28 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HeadHall', '0003_elevel_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='elevel',
            name='Details',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]