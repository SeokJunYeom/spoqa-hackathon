# Generated by Django 2.2.1 on 2019-05-18 19:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20190519_0325'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='to_do',
        ),
    ]