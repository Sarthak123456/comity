# Generated by Django 3.2.4 on 2021-07-27 23:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('comity', '0019_auto_20210727_2311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group_table',
            name='u_id',
            field=models.ForeignKey(default=9, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]