# Generated by Django 4.2.6 on 2023-10-25 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiapp', '0030_alter_private_investigator_my_client'),
    ]

    operations = [
        migrations.AddField(
            model_name='profilefinder',
            name='Questin_and_answer',
            field=models.TextField(null=True),
        ),
    ]