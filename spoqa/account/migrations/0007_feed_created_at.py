# Generated by Django 2.2.1 on 2019-05-18 23:30

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_auto_20190519_0819'),
    ]

    operations = [
        migrations.AddField(
            model_name='feed',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
