# Generated by Django 4.1 on 2023-12-20 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('virtualExpert', '0002_create_ads_ad_created_time_create_ads_coin'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad_distributor',
            name='otp1',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='ad_distributor',
            name='user_otp1',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='ad_provider',
            name='otp1',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='ad_provider',
            name='user_otp1',
            field=models.IntegerField(null=True),
        ),
    ]
