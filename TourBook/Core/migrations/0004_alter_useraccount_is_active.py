# Generated by Django 5.0.2 on 2024-03-27 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0003_alter_useraccount_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
