# Generated by Django 4.1 on 2023-12-19 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('virtualExpert', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='create_ads',
            name='ad_created_time',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='create_ads',
            name='coin',
            field=models.TextField(null=True),
        ),
    ]