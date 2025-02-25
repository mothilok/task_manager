# Generated by Django 5.1.2 on 2024-11-10 14:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Noiro', '0003_rename_status_name_status_db_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project_db',
            name='user_created',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='status_db',
            name='status',
            field=models.IntegerField(),
        ),
    ]
