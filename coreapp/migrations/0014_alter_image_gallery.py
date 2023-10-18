# Generated by Django 4.2 on 2023-05-22 10:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coreapp', '0013_remove_imagegallery_image_image_gallery'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='gallery',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='gallery_image', to='coreapp.imagegallery'),
        ),
    ]
