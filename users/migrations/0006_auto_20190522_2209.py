# Generated by Django 2.2 on 2019-05-22 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20190517_1949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profileImg',
            field=models.ImageField(default='users/not-user.jpg', upload_to='users/'),
        ),
    ]
