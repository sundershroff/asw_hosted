# Generated by Django 4.2.5 on 2023-10-11 05:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apiapp', '0027_remove_private_investigator_my_client'),
    ]

    operations = [
        migrations.AddField(
            model_name='private_investigator',
            name='my_client',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='apiapp.profilefinder'),
            preserve_default=False,
        ),
    ]
