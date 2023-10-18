# Generated by Django 4.2 on 2023-05-18 12:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coreapp', '0010_remove_image_shop_remove_imagegallery_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='category',
        ),
        migrations.RemoveField(
            model_name='imagegallery',
            name='image_url',
        ),
        migrations.AddField(
            model_name='imagegallery',
            name='image',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='coreapp.image'),
            preserve_default=False,
        ),
    ]