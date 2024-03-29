# Generated by Django 2.2 on 2019-05-15 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='country',
            field=models.CharField(default='Europe', max_length=35),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='profileImg',
            field=models.ImageField(default='/static/imgs/not-user.jpg', upload_to=''),
        ),
    ]
