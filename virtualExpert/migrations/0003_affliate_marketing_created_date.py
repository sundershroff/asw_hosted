# Generated by Django 4.2.5 on 2024-01-16 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('virtualExpert', '0002_remove_affliate_marketing_created_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='affliate_marketing',
            name='created_date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
