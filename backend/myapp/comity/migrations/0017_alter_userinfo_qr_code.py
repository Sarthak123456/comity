# Generated by Django 3.2.4 on 2021-06-23 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comity', '0016_auto_20201220_0722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='qr_code',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]