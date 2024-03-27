from django.db import models

class ProfileFinder(models.Model):
    # User ID
    uid = models.TextField()

    # Signup
    email = models.EmailField()
    mobile = models.TextField()
    password = models.TextField()
    referral_code = models.TextField()
    coin = models.TextField(null=True)
    created_time= models.TextField(null=True)
    otp = models.IntegerField()
    user_otp = models.IntegerField(null=True)
    
        #created on 
    created_date = models.TextField(null=True)

    # ID Card 1
    id_card_1  = models.TextField(null=True)

    # Basic Details
    name = models.TextField(null=True)
    address = models.TextField(null=True)
    height = models.IntegerField(null=True)
    weight = models.IntegerField(null=True)
    gender = models.TextField(null=True)
    marital = models.TextField(null=True)
    physical = models.TextField(null=True)
    religion = models.TextField(null=True)
    age = models.IntegerField(null=True)
    birth_place = models.TextField(null=True)  
    birth_country = models.TextField(null=True) 
    birth_time = models.TimeField(null=True)
    birth_city = models.TextField(null=True)
    origin = models.TextField(null=True)    
    r_country = models.TextField(null=True) 
    r_state = models.TextField(null=True)   
    r_status = models.TextField(null=True)  
    denomination = models.TextField(null=True)  
    blood_group = models.TextField(null=True)

    # ID Card 2
    id_card_2 = models.TextField(null=True)

    # profileforwho
    profileforwho = models.TextField(null=True)

    # Parish / Temple / Mosque Details
    temple_name = models.TextField(null=True)
    temple_street = models.TextField(null=True)
    temple_post_code = models.TextField(null=True)
    temple_country= models.TextField(null=True)
    temple_city = models.TextField(null=True)
    temple_phone_number = models.TextField(null=True)
    temple_diocese = models.TextField(null=True)
    temple_local_admin = models.TextField(null=True)

    # Emergency Contact
    emergency_name = models.TextField(null=True)    
    emergency_relation = models.TextField(null=True)
    emergency_phone_number = models.TextField(null=True)
    emergency_email = models.TextField(null=True)
    emergency_marital_status = models.TextField(null=True)
    emergency_occupations = models.TextField(null=True) 

    # Profile Picture
    profile_picture = models.TextField(null=True)

    # Primary Details
    marital_status = models.TextField(null=True)
    physical_mental_status = models.TextField(null=True)
    primary_email = models.EmailField(null=True)
    primary_phone_number = models.TextField(null=True)
    dob = models.DateField(null=True)
    why_marry = models.TextField(null=True)
    behind_decision = models.TextField(null=True)

    # Education
    education_school = models.TextField(null=True)
    education_year = models.TextField(null=True)
    education_course = models.TextField(null=True)
    education_major = models.TextField(null=True)

    # Working
    are_you_working_now = models.TextField(null=True)
    company_name = models.TextField(null=True)
    position = models.TextField(null=True)
    profession = models.TextField(null=True)
    salary_range = models.TextField(null=True)

    # Intrest and Non Intrest
    your_intrest = models.TextField(null=True)
    non_intrest = models.TextField(null=True)

    # Complexion
    complexion = models.TextField(null=True)

    # Food Taste
    food_taste = models.TextField(null=True) 

    # After Marriage
    daily_diet_plan = models.TextField(null=True)
    carriying_after_marriage = models.TextField(null=True)
    tobacco = models.TextField(null=True)
    alcohol =models.TextField(null=True)
    drugs = models.TextField(null=True)
    criminal_offence = models.TextField(null=True)

    # Primary Country
    primary_country = models.TextField(null=True)

    # Gallery
    selfie = models.TextField(null=True)
    full_size_image = models.TextField(null=True)
    family_image = models.TextField(null=True)
    gallery = models.TextField(null=True)
    horoscope = models.TextField(null=True)
    profile_tag = models.TextField(null=True)
    treet_mypartner = models.TextField(null=True)
    treet_their_side = models.TextField(null=True)

    # More Specific
    orphan = models.TextField(null=True)
    disable = models.TextField(null=True)
    whichorgan = models.TextField(null=True)

    # Family Details
    family_status = models.TextField(null=True)

    # Father Details
    father_name = models.TextField(null=True)
    father_country = models.TextField(null=True)
    father_city = models.TextField(null=True)
    father_job = models.TextField(null=True)
    father_family_name = models.TextField(null=True)

    # Mother Details
    mother_name = models.TextField(null=True)
    mother_country = models.TextField(null=True)
    mother_city = models.TextField(null=True)
    mother_job = models.TextField(null=True)
    mother_family_name= models.TextField(null=True)

    # Sibling 1 Details
    sibling_name = models.TextField(null=True)
    sibling_relation = models.TextField(null=True)
    sibling_young_or_old = models.TextField(null=True)
    sibling_occupation = models.TextField(null=True)
    sibling_marital = models.TextField(null=True)
    sibling_email = models.TextField(null=True)
    sibling_dob = models.TextField(null=True)
    sibling_job = models.TextField(null=True)

    # About Candidates
    about_candidate = models.TextField(null=True)
    current_status = models.TextField(null=True)  

    # Contact Details
    contact_father_name = models.TextField(null=True)
    contact_father_street = models.TextField(null=True)
    contact_father_zipcode = models.TextField(null=True)
    contact_father_country = models.TextField(null=True)
    contact_father_city = models.TextField(null=True)
    contact_father_housename = models.TextField(null=True)
    contact_mother_housename = models.TextField(null=True)
    contact_email = models.TextField(null=True)
    contact_phone = models.TextField(null=True)

    # Social Media
    whatsapp = models.TextField(null=True)
    facebook = models.TextField(null=True)
    linkedin = models.TextField(null=True)
    instagram = models.TextField(null=True)
    youtube = models.TextField(null=True)
    twitter = models.TextField(null=True)
    website = models.TextField(null=True)
    
    #registered date and time
    registered_date = models.DateField(null=True)

    #my investigator
    my_investigator = models.TextField(null=True)
    
    #question and answer
    Questin = models.TextField(null=True)
    answer = models.TextField(null=True)
    
    #ratings and feedback
    rating = models.TextField(null=True)
    feedback = models.TextField(null=True)

    #my_manager
    my_manager = models.TextField(null=True)
    complaints = models.TextField(null=True)
    complaints_replay = models.TextField(null=True)

    #status
    status = models.TextField(null=True)
    reason = models.TextField(null=True)
    # forget password
    otp1 = models.IntegerField(null=True)
    user_otp1 = models.IntegerField(null=True)

class sender_list(models.Model):
    sender_uid = models.TextField(null=True)
    received_uid = models.TextField(null=True)
    request_phone_number = models.TextField(null=True)
    request_whatsapp_number = models.TextField(null=True)
    request_address = models.TextField(null=True)
    request_horoscope = models.TextField(null=True)
    request_social_media_link = models.TextField(null=True)
    action = models.TextField(null=True)

class received_list(models.Model):
    received_uid = models.TextField(null=True)
    sender_uid = models.TextField(null=True)
    request_phone_number = models.TextField(null=True)
    request_whatsapp_number = models.TextField(null=True)
    request_address = models.TextField(null=True)
    request_horoscope = models.TextField(null=True)
    request_social_media_link = models.TextField(null=True)
    action = models.TextField(null=True)

class block(models.Model):
    who_blocked_id = models.TextField(null=True)
    blocked_id = models.TextField(null=True)
    reason = models.TextField(null=True)
    who_blocked_me=models.TextField(null=True)

class favorite(models.Model):
    my_id = models.TextField(null=True)
    myfavorite_id = models.TextField(null=True)
    who_favorite_me_id = models.TextField(null=True)

class happy_couples(models.Model):
    groom_name = models.TextField(null=True)
    groom_id = models.TextField(null=True)
    bride_name = models.TextField(null=True)
    bride_id = models.TextField(null=True)
    date_of_marriage = models.TextField(null=True)
    worde_about_marriyo = models.TextField(null=True)
    image_videous = models.TextField(null=True)

class saved_search(models.Model):
    my_id = models.TextField(null=True)
    tag = models.TextField(null=True)
    country = models.TextField(null=True)
    city = models.TextField(null=True)
    age = models.IntegerField(null=True)
    complexion = models.TextField(null=True)
    gender = models.TextField(null=True)
    denomination = models.TextField(null=True)
    filterd_data = models.TextField(null=True)

    
class AdsViewedUser(models.Model):
   
    PF_id =models.TextField(null=True)
    Ads_id = models.TextField(null=True)
    no_views = models.TextField(null=True)


class profilefinder_ads_highlights(models.Model):
    uid=models.TextField(null=True)
    pf_data=models.TextField(null=True)
    ads_languages=models.TextField(null=True)
    ads_country=models.TextField(null=True)
    ads_state=models.TextField(null=True)
    ads_district=models.TextField(null=True)
    ads_gender=models.TextField(null=True)
    age_range=models.IntegerField(null=True)
    age_to=models.IntegerField(null=True) 
    Total_views=models.TextField(null=True)
    ads_days_required=models.TextField(null=True)
    ads_times_repeat=models.TextField(null=True)


#///////////////private investigator/////////////
class private_investigator(models.Model):
    # User ID
    uid = models.TextField()

    # Signup
    email = models.EmailField()
    mobile = models.TextField()
    password = models.TextField()
    # referral_code = models.TextField()
    otp = models.IntegerField()
    user_otp = models.IntegerField(null=True)
    
        #created on 
    created_date = models.TextField(null=True)

    # ID Card 1
    profile_picture  = models.TextField(null=True)

    #Edit Account
    office_name = models.TextField(null=True)
    office_country = models.TextField(null=True)
    office_city = models.TextField(null=True)
    office_address = models.TextField(null=True)

    first_name = models.TextField(null=True)
    last_name = models.TextField(null=True)
    personal_country = models.TextField(null=True)
    personal_city = models.TextField(null=True)
    personal_address = models.TextField(null=True)
    hiring_manager = models.TextField(null=True)
    id_card = models.TextField(null=True)
    tagline = models.TextField(null=True)
    hiring_manager = models.TextField(null=True)
    
    #signed document
    sign_document = models.TextField(null=True)
    verification_img = models.TextField(null=True)
 #new qualification
    level_education = models.TextField(null=True)
    field_study = models.TextField(null=True)
    work_job_title = models.TextField(null=True)
    work_company_name = models.TextField(null=True)
    work_job_location = models.TextField(null=True)
    ex_job_title = models.TextField(null=True)
    ex_company_name = models.TextField(null=True)
    year_experience = models.TextField(null=True)
    ex_location = models.TextField(null=True)
    degree_cer = models.TextField(null=True)
    ex_cer = models.TextField(null=True)
    work_type = models.TextField(null=True)
    gst_number = models.TextField(null=True)
    gst_certificate = models.TextField(null=True)
    company_pan_no = models.TextField(null=True)
    arn_no =models.TextField(null=True)
    pan_card =models.TextField(null=True)
    notification_status=models.BooleanField(default=False,null=True)
    #my client
    # my_client= models.ForeignKey(ProfileFinder,null=True,on_delete=models.CASCADE)
    my_client = models.TextField(null=True)
    
    #allratings
    all_ratings =  models.TextField(null=True)
    #total ratings
    total_ratings = models.IntegerField(null=True)
        # forget password
    otp1 = models.IntegerField(null=True)
    user_otp1 = models.IntegerField(null=True)

