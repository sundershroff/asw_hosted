# Generated by Django 4.2.5 on 2023-10-10 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiapp', '0023_private_investigator_first_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='private_investigator',
            name='my_client',
            field=models.TextField(null=True),
        ),
    ]
