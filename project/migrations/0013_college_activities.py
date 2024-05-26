# Generated by Django 5.0.3 on 2024-05-25 16:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0012_remove_accstatusmain_accreditation_criteria_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='College_activities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('year', models.IntegerField()),
                ('seasson', models.CharField(max_length=15)),
                ('acc_status_main', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.accstatusmain')),
            ],
        ),
    ]