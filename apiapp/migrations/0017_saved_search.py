# Generated by Django 4.2.5 on 2023-09-14 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiapp', '0016_happy_couples'),
    ]

    operations = [
        migrations.CreateModel(
            name='saved_search',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.TextField(null=True)),
                ('country', models.TextField(null=True)),
                ('city', models.TextField(null=True)),
                ('age', models.IntegerField(null=True)),
                ('complexion', models.TextField(null=True)),
                ('gender', models.TextField(null=True)),
                ('denomination', models.TextField(null=True)),
            ],
        ),
    ]
