# Generated by Django 2.2.2 on 2020-09-06 22:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comity', '0004_group_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group_table',
            name='u_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
