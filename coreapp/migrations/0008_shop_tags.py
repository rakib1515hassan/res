# Generated by Django 4.2 on 2023-05-11 18:53

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0005_auto_20220424_2025'),
        ('coreapp', '0007_alter_image_options_alter_imagegallery_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
