# Generated by Django 4.2.7 on 2023-11-30 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiapp', '0038_private_investigator_created_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profilefinder',
            name='my_manager',
            field=models.TextField(null=True),
        ),
    ]