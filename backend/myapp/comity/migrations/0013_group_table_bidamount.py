# Generated by Django 2.2.2 on 2020-10-24 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comity', '0012_auto_20201017_1148'),
    ]

    operations = [
        migrations.AddField(
            model_name='group_table',
            name='bidAmount',
            field=models.IntegerField(default=0),
        ),
    ]