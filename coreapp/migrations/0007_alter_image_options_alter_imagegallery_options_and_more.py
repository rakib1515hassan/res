# Generated by Django 4.2 on 2023-05-11 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coreapp', '0006_image_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='image',
            options={'ordering': ['-id']},
        ),
        migrations.AlterModelOptions(
            name='imagegallery',
            options={'ordering': ['-id']},
        ),
        migrations.AlterModelOptions(
            name='shop',
            options={'ordering': ['-id']},
        ),
        migrations.AddField(
            model_name='customuser',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]