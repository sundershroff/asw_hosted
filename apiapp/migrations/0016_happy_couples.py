# Generated by Django 4.2.3 on 2023-09-06 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiapp', '0015_favorite_my_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='happy_couples',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('groom_name', models.TextField(null=True)),
                ('groom_id', models.TextField(null=True)),
                ('bride_name', models.TextField(null=True)),
                ('bride_id', models.TextField(null=True)),
                ('date_of_marriage', models.TextField(null=True)),
                ('worde_about_marriyo', models.TextField(null=True)),
                ('image_videous', models.TextField(null=True)),
            ],
        ),
    ]