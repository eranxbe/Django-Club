# Generated by Django 4.2.7 on 2023-12-07 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_venue_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='venue',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='Image'),
        ),
    ]