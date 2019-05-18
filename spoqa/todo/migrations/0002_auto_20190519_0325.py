# Generated by Django 2.2.1 on 2019-05-18 18:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20190519_0325'),
        ('todo', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='todotext',
            options={'ordering': ['-created_at'], 'verbose_name': 'to do text', 'verbose_name_plural': 'to do text'},
        ),
        migrations.AddField(
            model_name='todotext',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='생성 날짜'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='History',
        ),
    ]