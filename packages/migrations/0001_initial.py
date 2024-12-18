# Generated by Django 5.1.4 on 2024-12-16 23:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TravelPackage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('destination', models.CharField(max_length=255)),
                ('package_type', models.CharField(choices=[('Beach', 'Beach'), ('Adventure', 'Adventure'), ('Cultural', 'Cultural'), ('Family', 'Family'), ('Relaxation', 'Relaxation'), ('City', 'City')], max_length=50)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('duration', models.CharField(max_length=50)),
                ('rating', models.DecimalField(decimal_places=1, max_digits=3)),
                ('description', models.TextField()),
                ('available', models.BooleanField(default=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='packages/')),
                ('tags', models.ManyToManyField(blank=True, related_name='travel_packages', to='packages.tag')),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('datetime', models.DateTimeField()),
                ('destination', models.CharField(max_length=255)),
                ('persons', models.PositiveIntegerField()),
                ('category', models.CharField(max_length=50)),
                ('payment_method', models.CharField(max_length=50)),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='packages.travelpackage')),
            ],
        ),
    ]