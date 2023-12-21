# Generated by Django 4.2.5 on 2023-10-07 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiapp', '0022_private_investigator'),
    ]

    operations = [
        migrations.AddField(
            model_name='private_investigator',
            name='first_name',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='private_investigator',
            name='hiring_manager',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='private_investigator',
            name='id_card',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='private_investigator',
            name='last_name',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='private_investigator',
            name='office_address',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='private_investigator',
            name='office_city',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='private_investigator',
            name='office_country',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='private_investigator',
            name='office_name',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='private_investigator',
            name='personal_address',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='private_investigator',
            name='personal_city',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='private_investigator',
            name='personal_country',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='private_investigator',
            name='tagline',
            field=models.TextField(null=True),
        ),
    ]
