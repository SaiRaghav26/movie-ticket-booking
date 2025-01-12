# Generated by Django 4.2.17 on 2025-01-10 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookmyticket', '0002_screen_remove_movie_image_movie_banners_and_more'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='showtimings',
            constraint=models.UniqueConstraint(fields=('theatre', 'screen', 'show_time'), name='unique_show_time_per_screen'),
        ),
    ]
