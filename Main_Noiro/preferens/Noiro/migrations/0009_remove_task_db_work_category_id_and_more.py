# Generated by Django 5.1.2 on 2024-11-28 14:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Noiro', '0008_user_work_category_db_board_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task_db',
            name='work_category_id',
        ),
        migrations.AlterField(
            model_name='task_db',
            name='board_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Noiro.board_db'),
        ),
        migrations.AlterField(
            model_name='task_db',
            name='comment',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
