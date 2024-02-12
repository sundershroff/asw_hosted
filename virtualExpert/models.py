from django.db import models

# Create your models here.
class Profilemanager(models.Model):
    # User ID
    uid = models.TextField()

    # Signup
    email = models.EmailField()
    mobile = models.TextField()
    password = models.TextField()
    otp = models.IntegerField()
    user_otp = models.IntegerField(null=True)
    
    #profile picture
    profile_picture = models.TextField(null=True)

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
    notary = models.TextField(null=True)
    id_card = models.TextField(null=True)
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
    
    #signed document
    sign_document = models.TextField(null=True)
    
    #created on 
    created_date = models.TextField(null=True)

    #my_client
    my_client = models.TextField(null=True)
    
     # forget Password otps
    otp1 = models.IntegerField(null=True)
    user_otp1 = models.IntegerField(null=True)

#/////Hiring manager/////
class hiringmanager(models.Model):
    # User ID
    uid = models.TextField()

    # Signup
    email = models.EmailField()
    mobile = models.TextField()
    password = models.TextField()
    otp = models.IntegerField()
    user_otp = models.IntegerField(null=True)

    #profile picture
    profile_picture = models.TextField(null=True)

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
    
    #my hiring manager
    my_hiring_manager = models.TextField(null=True)
    #signed document
    sign_document = models.TextField(null=True)

    #my profile manager
    my_profile_manager = models.TextField(null=True)
    
    #ad_provider
    ad_provider = models.TextField(null=True)
    
    #sales_manager
    sales_manager = models.TextField(null=True)
    #ad_distributor
    ad_distributor = models.TextField(null=True)

    #affiliate_marketing
    affiliate_marketing = models.TextField(null=True)

    #private_investigator
    private_investigator = models.TextField(null=True)

    #created on 
    created_date = models.TextField(null=True)

    # forget Password otps
    otp1 = models.IntegerField(null=True)
    user_otp1 = models.IntegerField(null=True)
   #deioces

#/////sales manager/////
class salesmanager(models.Model):
    # User ID
    uid = models.TextField()

    # Signup
    email = models.EmailField()
    mobile = models.TextField()
    password = models.TextField()
    otp = models.IntegerField()
    user_otp = models.IntegerField(null=True)

    #profile picture
    profile_picture = models.TextField(null=True)


    #Edit Account
    full_name = models.TextField(null=True)
    personal_country = models.TextField(null=True)
    personal_city = models.TextField(null=True)
    personal_address = models.TextField(null=True)
    hiring_manager = models.TextField(null=True)
    id_card = models.TextField(null=True)
    otp1 = models.IntegerField(null=True)
    user_otp1 = models.IntegerField(null=True)
    #signed document
    sign_document = models.TextField(null=True)
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
    
    #created on 
    created_date = models.TextField(null=True)

    #ads list
    ad_provider=models.TextField(null=True)
    ad_distributor=models.TextField(null=True)
    my_profile_manager=models.TextField(null=True)
    

#/////add client////#
class ad_client(models.Model):

    uid=models.TextField()

    options=(
        ("Profile Manager","Profile Manager"),
        ("AD Provider","AD Provider"),
        ("AD Distributor","AD Distributor"),

    )
    client_type=models.CharField(max_length=200,choices=options)
    client_name=models.TextField()
    client_location=models.TextField()
    category=models.TextField()
    google_map=models.TextField()
    phone_number=models.TextField()
    email=models.TextField()
    picture = models.TextField(null=True)
    status=models.BooleanField(null=True,default=False)
    sales_id=models.TextField(null=True)
    otp = models.IntegerField(null=True)
    user_otp = models.IntegerField(null=True)
    active_status=models.BooleanField(null=True,default=False)
    
    
    #///add activities///#

    # client=models.TextField(null=True)
    types_of_activities=models.TextField(null=True)
    date=models.TextField(null=True)
    time=models.TextField(null=True)
    notes=models.TextField(null=True)
 



#/////ad provider//////
class ad_provider(models.Model):
    # User ID
    uid = models.TextField()

    # Signup
    email = models.EmailField()
    mobile = models.TextField()
    password = models.TextField()
    otp = models.IntegerField(null=True)
    user_otp = models.IntegerField(null=True)
    
    #profile picture
    profile_picture = models.TextField(null=True)

    #Edit Account
    office_name = models.TextField(null=True)
    office_country = models.TextField(null=True)
    office_city = models.TextField(null=True)
    office_address = models.TextField(null=True)
    
    type=models.TextField(null=True)
    first_name = models.TextField(null=True)
    last_name = models.TextField(null=True)
    personal_country = models.TextField(null=True)
    personal_city = models.TextField(null=True)
    personal_address = models.TextField(null=True)
    id_card = models.TextField(null=True)
    hiring_manager = models.TextField(null=True)
    sales_manager = models.TextField(null=True)
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
    
    #signed document
    sign_document = models.TextField(null=True)
    
        #created on 
    created_date = models.TextField(null=True)
    # forget password otp
    otp1 = models.IntegerField(null=True)
    user_otp1 = models.IntegerField(null=True)

#/////ad distributor//////
class ad_distributor(models.Model):
    # User ID
    uid = models.TextField()

    # Signup
    email = models.EmailField()
    mobile = models.TextField()
    password = models.TextField()
    otp = models.IntegerField(null=True)
    user_otp = models.IntegerField(null=True)

    #profile picture
    profile_picture = models.TextField(null=True)

    type=models.TextField(null=True)
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
    id_card = models.TextField(null=True)
    hiring_manager = models.TextField(null=True)
    sales_manager = models.TextField(null=True)
    #signed document
    sign_document = models.TextField(null=True)
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
    
    #created on 
    created_date = models.TextField(null=True)

    # forget password otp
    otp1 = models.IntegerField(null=True)
    user_otp1 = models.IntegerField(null=True)

#/////affiliate marketing//////
class affliate_marketing(models.Model):
# User ID
    uid = models.TextField()

    # Signup
    email = models.EmailField()
    mobile = models.TextField()
    password = models.TextField()
    otp = models.IntegerField()
    user_otp = models.IntegerField(null=True)

    #profile picture
    profile_picture = models.TextField(null=True)


    #Edit Account

    full_name = models.TextField(null=True)
    personal_country = models.TextField(null=True)
    personal_city = models.TextField(null=True)
    personal_address = models.TextField(null=True)
    id_card = models.TextField(null=True)
    hiring_manager = models.TextField(null=True)
    referral_code = models.TextField(null=True)
    coin = models.TextField(null=True)
    #signed document
    sign_document = models.TextField(null=True)
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
    
    otp1 = models.IntegerField(null=True)
    user_otp1 = models.IntegerField(null=True)
    #created on 
    created_date = models.DateField(null=True, auto_now_add=True)
    created_time = models.TextField(null=True)


# ///ad_distributor AD Creation Model////
class Create_ads(models.Model):
    ad_id = models.TextField(null=True)
    ad_name=models.TextField()
    category=models.TextField()
    ad_type=models.TextField()
    languages=models.TextField()
    office_country=models.TextField()
    office_state=models.TextField(null=True)
    office_district=models.TextField()
    gender=models.TextField()
    age_range=models.IntegerField()
    age_to=models.IntegerField(null=True)
    id_card = models.TextField(null=True)
    no_views=models.TextField()
    days_required=models.TextField()
    times_repeat=models.TextField()
    ad_details=models.TextField()
    other_ads=models.TextField()
    action_name=models.TextField()
    action_url=models.TextField()
    status=models.TextField(null=True)
    ad_dis=models.TextField(null=True)
     #created on 
    ad_created_date = models.TextField(null=True)
    reason = models.TextField(null=True)
    coin=models.TextField(null=True)
    ad_created_time = models.TextField(null=True)

    


# ///// Ad-Provider Ad Creation/////
class ad_pro_ads(models.Model):
    ad_id = models.TextField()
    ad_name=models.TextField()
    category=models.TextField()
    ad_type=models.TextField()
    languages=models.TextField()
    office_country=models.TextField()
    office_state=models.TextField(null=True)
    office_district=models.TextField()
    gender=models.TextField()
    age_range=models.IntegerField()
    age_to=models.IntegerField()
    id_card = models.TextField()
    no_views=models.TextField()
    days_required=models.TextField()
    times_repeat=models.TextField()
    ad_details=models.TextField()
    other_ads=models.TextField()
    action_name=models.TextField()
    action_url=models.TextField()
    status=models.TextField(null=True)
    ad_pro=models.TextField(null=True)
     #created on 
    ad_created_date = models.TextField(null=True)
    ad_created_time = models.TextField(null=True)
    reason = models.TextField(null=True)
    coin=models.TextField(null=True)
    commission=models.TextField(null=True)

#/////Users //////
class users(models.Model):
    uid = models.TextField(null=True)
    aid = models.TextField(null=True)
    first_name = models.TextField(null=True)
    last_name = models.TextField(null=True)
    email = models.EmailField(null=True)
    mobile = models.TextField(null=True)
    password = models.TextField(null=True)
    access_Privileges = models.TextField(null=True)
    work = models.TextField(null=True)
    creator =  models.TextField(null=True)
    location = models.TextField(null=True)
    my_client = models.TextField(null=True)
