# Generated by Django 4.2 on 2023-05-22 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coreapp', '0015_remove_image_gallery_image_gallery'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='bank_account_number',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='company_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='kvk',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='street_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='zip_code',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
