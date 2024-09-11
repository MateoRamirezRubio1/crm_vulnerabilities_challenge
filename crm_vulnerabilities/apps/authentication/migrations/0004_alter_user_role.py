# Generated by Django 5.1.1 on 2024-09-11 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_alter_user_groups_alter_user_user_permissions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('permi1', 'Permi1'), ('permi2', 'Permi2'), ('permi3', 'Permi3')], default='basic', max_length=20),
        ),
    ]
