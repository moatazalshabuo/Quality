# Generated by Django 5.0.3 on 2024-06-07 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accuont', '0003_user_type_enterprise'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='staff',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='students',
            field=models.IntegerField(default=0),
        ),
    ]