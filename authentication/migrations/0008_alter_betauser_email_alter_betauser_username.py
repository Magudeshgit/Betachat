# Generated by Django 4.2.1 on 2023-06-08 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0007_alter_betauser_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='betauser',
            name='email',
            field=models.EmailField(max_length=255, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='betauser',
            name='username',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
