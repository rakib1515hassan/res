# Generated by Django 4.2 on 2023-05-25 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coreapp', '0019_remove_shop_login_from'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='login_from',
            field=models.CharField(choices=[('shop', 'shop'), ('Account', 'Account')], default='Account', max_length=20),
        ),
    ]
