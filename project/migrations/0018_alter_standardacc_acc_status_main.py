# Generated by Django 5.0.3 on 2024-05-28 23:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0017_alter_accstatusmain_accreditation_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='standardacc',
            name='acc_status_main',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stan_acc', to='project.accstatusmain'),
        ),
    ]