# Generated by Django 5.0.2 on 2024-03-09 15:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='TourOrganizer',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Tour_Organizer.basemodel')),
                ('address', models.CharField(max_length=255)),
                ('evaluation', models.IntegerField(default=0)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='logos/')),
                ('joined_at', models.DateTimeField(auto_now_add=True)),
                ('situation', models.CharField(choices=[('SUB', 'Subscriper'), ('UNSUB', 'UnSubscriper'), ('B', 'Blocked')], default='UNSUB', max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='organizer', to=settings.AUTH_USER_MODEL)),
            ],
            bases=('Tour_Organizer.basemodel',),
        ),
        migrations.CreateModel(
            name='Tour',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Tour_Organizer.basemodel')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, max_length=1000, null=True)),
                ('starting_place', models.CharField(max_length=100)),
                ('like_counter', models.IntegerField(default=0)),
                ('dislike_counter', models.IntegerField(default=0)),
                ('seat_num', models.IntegerField(default=0)),
                ('seat_cost', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('transportation_cost', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('extra_cost', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('total_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('x_starting_place', models.IntegerField(default=0)),
                ('y_starting_place', models.IntegerField(default=0)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('note', models.TextField(blank=True, null=True)),
                ('tour_organizer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Tour_Organizer.tourorganizer')),
            ],
            bases=('Tour_Organizer.basemodel',),
        ),
    ]
