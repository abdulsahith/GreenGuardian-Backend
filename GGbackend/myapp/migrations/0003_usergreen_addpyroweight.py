# Generated by Django 5.1.3 on 2024-12-15 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_usergreen_bsmachineid_usergreen_bsflweight_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='usergreen',
            name='addpyroweight',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
