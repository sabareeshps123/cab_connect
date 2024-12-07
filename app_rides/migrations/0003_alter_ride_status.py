# Generated by Django 5.1.4 on 2024-12-07 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_rides', '0002_remove_ride_dropoff_location_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ride',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('completed', 'Completed'), ('cancelled', 'Cancelled'), ('started', 'Started')], default='pending', max_length=10),
        ),
    ]
