# Generated by Django 5.0.3 on 2024-05-26 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accuont', '0002_depatment'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='type_enterprise',
            field=models.CharField(blank=True, choices=[('علوم طبية', 'علوم طبية'), ('علوم تطبيقية', 'علوم تطبيقية'), ('علوم انسانية', 'علوم انسانية')], max_length=50, null=True),
        ),
    ]