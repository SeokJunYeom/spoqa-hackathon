# Generated by Django 2.2.1 on 2019-05-18 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_feed_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feed',
            name='img',
            field=models.FileField(upload_to='image/'),
        ),
    ]
