# Generated by Django 4.2.3 on 2023-09-04 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiapp', '0012_block_who_blocked_me'),
    ]

    operations = [
        migrations.AddField(
            model_name='profilefinder',
            name='registered_date',
            field=models.DateField(null=True),
        ),
    ]
