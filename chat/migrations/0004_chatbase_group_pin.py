# Generated by Django 4.2.1 on 2023-06-23 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_chatbase_group_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatbase',
            name='group_PIN',
            field=models.CharField(default='1234', max_length=8),
            preserve_default=False,
        ),
    ]
