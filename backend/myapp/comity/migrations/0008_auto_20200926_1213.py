# Generated by Django 2.2.2 on 2020-09-26 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comity', '0007_user_info_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='group_table',
            name='winner',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='user_info_table',
        ),
    ]
