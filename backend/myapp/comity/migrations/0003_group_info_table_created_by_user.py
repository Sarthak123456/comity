# Generated by Django 2.2.2 on 2020-09-06 21:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('comity', '0002_group_info_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='group_info_table',
            name='created_by_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
