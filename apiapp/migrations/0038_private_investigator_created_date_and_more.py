# Generated by Django 4.2.7 on 2023-11-09 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiapp', '0037_alter_private_investigator_total_ratings'),
    ]

    operations = [
        migrations.AddField(
            model_name='private_investigator',
            name='created_date',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='profilefinder',
            name='created_date',
            field=models.TextField(null=True),
        ),
    ]