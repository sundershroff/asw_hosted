# Generated by Django 4.2.3 on 2023-07-22 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProfileFinder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.TextField()),
                ('email', models.EmailField(max_length=254)),
                ('mobile', models.TextField()),
                ('password', models.TextField()),
                ('referral_code', models.TextField()),
                ('otp', models.IntegerField()),
                ('user_otp', models.IntegerField(null=True)),
                ('id_card_1', models.TextField(null=True)),
                ('name', models.TextField(null=True)),
                ('address', models.TextField(null=True)),
                ('height', models.IntegerField(null=True)),
                ('weight', models.IntegerField(null=True)),
                ('marital', models.TextField(null=True)),
                ('physical', models.TextField(null=True)),
                ('religion', models.TextField(null=True)),
                ('age', models.IntegerField(null=True)),
                ('birth_place', models.TextField(null=True)),
                ('birth_country', models.TextField(null=True)),
                ('birth_time', models.TimeField(null=True)),
                ('birth_city', models.TextField(null=True)),
                ('origin', models.TextField(null=True)),
                ('r_country', models.TextField(null=True)),
                ('r_state', models.TextField(null=True)),
                ('r_status', models.TextField(null=True)),
                ('denomination', models.TextField(null=True)),
                ('blood_group', models.TextField(null=True)),
                ('id_card_2', models.TextField(null=True)),
                ('temple_name', models.TextField(null=True)),
                ('temple_street', models.TextField(null=True)),
                ('temple_post_code', models.TextField(null=True)),
                ('temple_country', models.TextField(null=True)),
                ('temple_city', models.TextField(null=True)),
                ('temple_phone_number', models.TextField(null=True)),
                ('temple_diocese', models.TextField(null=True)),
                ('temple_local_admin', models.TextField(null=True)),
                ('emergency_name', models.TextField(null=True)),
                ('emergency_relation', models.TextField(null=True)),
                ('emergency_phone_number', models.TextField(null=True)),
                ('emergency_email', models.TextField(null=True)),
                ('emergency_marital_status', models.TextField(null=True)),
                ('emergency_occupations', models.TextField(null=True)),
                ('profile_picture', models.TextField(null=True)),
                ('marital_status', models.TextField(null=True)),
                ('physical_mental_status', models.TextField(null=True)),
                ('primary_email', models.EmailField(max_length=254, null=True)),
                ('primary_phone_number', models.TextField(null=True)),
                ('dob', models.DateField(null=True)),
                ('why_marry', models.TextField(null=True)),
                ('behind_decision', models.TextField(null=True)),
                ('education_school', models.TextField(null=True)),
                ('education_year', models.TextField(null=True)),
                ('education_course', models.TextField(null=True)),
                ('education_major', models.TextField(null=True)),
                ('are_you_working_now', models.TextField(null=True)),
                ('company_name', models.TextField(null=True)),
                ('position', models.TextField(null=True)),
                ('profession', models.TextField(null=True)),
                ('salary_range', models.TextField(null=True)),
                ('your_intrest', models.TextField(null=True)),
                ('non_intrest', models.TextField(null=True)),
                ('complexion', models.TextField(null=True)),
                ('food_taste', models.TextField(null=True)),
                ('daily_diet_plan', models.TextField(null=True)),
                ('carriying_after_marriage', models.TextField(null=True)),
                ('tobacco', models.TextField(null=True)),
                ('alcohol', models.TextField(null=True)),
                ('drugs', models.TextField(null=True)),
                ('criminal_offence', models.TextField(null=True)),
                ('primary_country', models.TextField(null=True)),
                ('selfie', models.TextField(null=True)),
                ('full_size_image', models.TextField(null=True)),
                ('family_image', models.TextField(null=True)),
                ('gallery', models.TextField(null=True)),
                ('horoscope', models.TextField(null=True)),
                ('profile_tag', models.TextField(null=True)),
                ('treet_mypartner', models.TextField(null=True)),
                ('treet_their_side', models.TextField(null=True)),
                ('orphan', models.TextField(null=True)),
                ('disable', models.TextField(null=True)),
                ('whichorgan', models.TextField(null=True)),
                ('family_status', models.TextField(null=True)),
                ('father_name', models.TextField(null=True)),
                ('father_country', models.TextField(null=True)),
                ('father_city', models.TextField(null=True)),
                ('father_job', models.TextField(null=True)),
                ('father_family_name', models.TextField(null=True)),
                ('mother_name', models.TextField(null=True)),
                ('mother_country', models.TextField(null=True)),
                ('mother_city', models.TextField(null=True)),
                ('mother_job', models.TextField(null=True)),
                ('mother_family_name', models.TextField(null=True)),
                ('sibling_name', models.TextField(null=True)),
                ('sibling_relation', models.TextField(null=True)),
                ('sibling_young_or_old', models.TextField(null=True)),
                ('sibling_occupation', models.TextField(null=True)),
                ('sibling_marital', models.TextField(null=True)),
                ('sibling_email', models.TextField(null=True)),
                ('sibling_dob', models.TextField(null=True)),
                ('sibling_job', models.TextField(null=True)),
                ('about_candidate', models.TextField(null=True)),
                ('current_status', models.TextField(null=True)),
                ('contact_father_name', models.TextField(null=True)),
                ('contact_father_street', models.TextField(null=True)),
                ('contact_father_zipcode', models.TextField(null=True)),
                ('contact_father_country', models.TextField(null=True)),
                ('contact_father_city', models.TextField(null=True)),
                ('contact_father_housename', models.TextField(null=True)),
                ('contact_mother_housename', models.TextField(null=True)),
                ('contact_email', models.TextField(null=True)),
                ('contact_phone', models.TextField(null=True)),
                ('whatsapp', models.TextField(null=True)),
                ('facebook', models.TextField(null=True)),
                ('linkedin', models.TextField(null=True)),
                ('instagram', models.TextField(null=True)),
                ('youtube', models.TextField(null=True)),
                ('twitter', models.TextField(null=True)),
                ('website', models.TextField(null=True)),
            ],
        ),
    ]
