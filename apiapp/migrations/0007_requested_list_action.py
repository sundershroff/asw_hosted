# Generated by Django 4.2.3 on 2023-08-15 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiapp', '0006_requested_list_requested_uid'),
    ]

    operations = [
        migrations.AddField(
            model_name='requested_list',
            name='action',
            field=models.TextField(null=True),
        ),
    ]