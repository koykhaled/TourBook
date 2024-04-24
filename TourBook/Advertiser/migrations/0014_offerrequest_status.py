# Generated by Django 5.0.2 on 2024-04-24 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Advertiser', '0013_alter_offer_num_of_seat'),
    ]

    operations = [
        migrations.AddField(
            model_name='offerrequest',
            name='status',
            field=models.CharField(choices=[('W', 'Waiting'), ('A', 'Accepted'), ('R', 'Rejected')], default='W', max_length=10),
        ),
    ]
