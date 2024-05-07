# Generated by Django 5.0.2 on 2024-05-07 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tour_Organizer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tourpoint',
            name='title',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tourpoint',
            name='arrival_time',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='tourpoint',
            name='leaving_time',
            field=models.DateTimeField(),
        ),
    ]
