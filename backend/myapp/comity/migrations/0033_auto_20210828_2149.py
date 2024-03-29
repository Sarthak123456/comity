# Generated by Django 3.2.4 on 2021-08-28 21:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('comity', '0032_alter_userinfo_gpay_qr_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='gpay_qr_code',
            field=models.FileField(blank=True, default='', upload_to='static/img/'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='u_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_info', to=settings.AUTH_USER_MODEL),
        ),
    ]
