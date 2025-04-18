# Generated by Django 5.1.7 on 2025-04-10 02:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0002_room_dirty_since'),
    ]

    operations = [
        migrations.CreateModel(
            name='Amenity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='RoomType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField(blank=True)),
                ('capacity', models.IntegerField()),
                ('size', models.IntegerField(help_text='Size in square feet')),
                ('default_price', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
        migrations.RemoveField(
            model_name='room',
            name='dirty_since',
        ),
        migrations.AddField(
            model_name='room',
            name='capacity',
            field=models.IntegerField(default=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='room',
            name='floor',
            field=models.IntegerField(default=15),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='room',
            name='size',
            field=models.IntegerField(default=25),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='room',
            name='amenities',
            field=models.ManyToManyField(blank=True, to='rooms.amenity'),
        ),
        migrations.AlterField(
            model_name='room',
            name='room_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rooms.roomtype'),
        ),
    ]
