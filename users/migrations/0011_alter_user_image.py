# Generated by Django 5.0.1 on 2024-02-07 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_alter_user_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='user_image/'),
        ),
    ]
