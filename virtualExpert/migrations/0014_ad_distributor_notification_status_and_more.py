# Generated by Django 4.1 on 2024-03-21 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('virtualExpert', '0013_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad_distributor',
            name='notification_status',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='ad_provider',
            name='notification_status',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='affliate_marketing',
            name='notification_status',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='hiringmanager',
            name='notification_status',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='profilemanager',
            name='notification_status',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='salesmanager',
            name='notification_status',
            field=models.BooleanField(default=False, null=True),
        ),
    ]