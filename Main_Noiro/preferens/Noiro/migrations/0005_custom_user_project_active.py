# Generated by Django 5.1.2 on 2024-11-11 12:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Noiro', '0004_alter_project_db_user_created_alter_status_db_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='custom_user',
            name='project_active',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Noiro.project_db'),
        ),
    ]
