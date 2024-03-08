
from rest_framework import serializers
from virtualExpert.models import hiringmanager,users

class hiringmanagerSerializer(serializers.Serializer):
    # User ID
    uid = serializers.CharField()

    # Signup
    email = serializers.EmailField()
    mobile = serializers.CharField()
    password = serializers.CharField()
    otp = serializers.IntegerField()
    user_otp = serializers.IntegerField()

    profile_picture = serializers.CharField()


     #Edit Account
    office_name = serializers.CharField()
    office_country = serializers.CharField()
    office_city = serializers.CharField()
    office_address = serializers.CharField()

    first_name = serializers.CharField()
    last_name = serializers.CharField()
    personal_country = serializers.CharField()
    personal_city = serializers.CharField()
    personal_dob = serializers.CharField()
    personal_age = serializers.CharField()
    house_number= serializers.CharField()
    street_name = serializers.CharField()
    pin_code = serializers.CharField()
    # notary = serializers.CharField()
    id_card = serializers.CharField()
    my_profile_manager = serializers.CharField()
    ad_provider = serializers.CharField() 
    ad_distributor = serializers.CharField() 
    sales_manager = serializers.CharField() 
    hiring_manager = serializers.CharField()
    affiliate_marketing = serializers.CharField()
    private_investigator = serializers.CharField()
    created_date = serializers.CharField()
    otp1 = serializers.IntegerField()
    user_otp1 = serializers.IntegerField()
    
    level_education = serializers.CharField()
    field_study = serializers.CharField()
    school_colege = serializers.CharField()
    completed_year = serializers.CharField()
    sch_colg_location = serializers.CharField()
    degree_cer = serializers.CharField()
    skills = serializers.CharField()

    work_job_title = serializers.CharField()
    work_company_name = serializers.CharField()
    work_start_date = serializers.CharField()
    starting_salary = serializers.CharField()
    work_end_date = serializers.CharField()
    reason_leaving = serializers.CharField()
    work_review_y = serializers.CharField()
    expr_certi = serializers.CharField()
    # work_job_location = serializers.CharField()
    curent_busines = serializers.CharField()
    past_business = serializers.CharField()
    
    mariyo_work_type = serializers.CharField()
    company_name = serializers.CharField()
    company_address = serializers.CharField()
    company_phone = serializers.CharField()
    company_email = serializers.CharField()

    gst_number = serializers.CharField()
    gst_certificate = serializers.CharField()


class SignupSerializer(serializers.Serializer):
    uid = serializers.CharField()
    email = serializers.EmailField()
    mobile = serializers.CharField()
    password = serializers.CharField()
    otp = serializers.IntegerField()
    created_date = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    
    def create(self, data):
        return hiringmanager.objects.create(
            uid = data['uid'],
            email = data['email'],
            mobile = data['mobile'],
            first_name = data['first_name'],       
            last_name = data['last_name'],
            password = data['password'],
            otp = data['otp'],
            created_date = data['created_date'],
        )
    
class OTPSerializer(serializers.Serializer):
    user_otp = serializers.IntegerField()
    

    def update(self, instance, data):
        instance.user_otp = data['user_otp']
        instance.save()
        return instance
    
class profile_picture_Serializer(serializers.Serializer):
    profile_picture = serializers.CharField()
    
    def update(self, instance, data):
        instance.profile_picture = data['profile_picture']
        instance.save()
        return instance


class upload_acc_Serializer(serializers.Serializer):
    office_name = serializers.CharField()
    office_country = serializers.CharField()
    office_city = serializers.CharField()
    office_address = serializers.CharField()

    personal_country = serializers.CharField()
    personal_city = serializers.CharField()
    personal_dob = serializers.CharField()
    personal_age = serializers.CharField()
    house_number= serializers.CharField()
    street_name = serializers.CharField()
    pin_code = serializers.CharField()
    my_hiring_manager = serializers.CharField()
    # id_card = serializers.CharField()
    aadhaar_no = serializers.CharField()
    aadhaar_card = serializers.CharField()
    pan_no = serializers.CharField()
    pan_card = serializers.CharField()
    drive_licence_no = serializers.CharField()
    drive_licence = serializers.CharField()
    drive_licence_date = serializers.CharField()
    licence_state = serializers.CharField()
    
    past_applied_date = serializers.CharField()
    past_applied_position = serializers.CharField()
    # citizen_country = serializers.CharField()
    govtjob_start_date = serializers.CharField()
    govtjob_end_date = serializers.CharField()
    judgment_felony = serializers.CharField()
    notary_lic_no =  serializers.CharField()
    notary_issued = serializers.CharField()
    notary_state = serializers.CharField()
    level_education = serializers.CharField()
    field_study = serializers.CharField()
    school_colege = serializers.CharField()
    completed_year = serializers.CharField()
    study_location = serializers.CharField()
    degree_cer = serializers.CharField()
    skills = serializers.CharField()

    work_job_title = serializers.CharField()
    work_company_name = serializers.CharField()
    work_start_date = serializers.CharField()
    starting_salary = serializers.CharField()
    work_end_date = serializers.CharField()
    final_salary = serializers.CharField()
    reason_leaving = serializers.CharField()
    work_review_y = serializers.CharField()
    expr_certi = serializers.CharField()
    # work_job_location = serializers.CharField()
    curent_busines = serializers.CharField()
    past_business = serializers.CharField()
    
    mariyo_work_type = serializers.CharField()
    company_name = serializers.CharField()
    company_address = serializers.CharField()
    company_phone = serializers.CharField()
    company_email = serializers.CharField()

    gst_number = serializers.CharField()
    gst_certificate = serializers.CharField()

    def update(self, instance, data):
        instance.office_name = data['office_name']
        instance.office_country = data['office_country']
        instance.office_city = data['office_city']
        instance.office_address = data['office_address']
    
        
        instance.personal_country = data['personal_country']
        instance.personal_city = data['personal_city']
        instance.personal_dob = data['personal_dob']
        instance.personal_age = data['personal_age']
        instance.house_numbe = data['house_numbe']
        instance.street_name = data['street_name']
        instance.pin_code = data['pin_code']
        # instance.personal_address = data['personal_address']
        instance.aadhaar_no = data['aadhaar_no']
        instance.aadhaar_card = data['aadhaar_card']
        instance.pan_no = data['pan_no']
        instance.pan_card = data['pan_card']
        instance.drive_licence_no = data['drive_licence_no']
        instance.drive_licence = data['drive_licence']
        instance.drive_licence_date = data['drive_licence_date']
        instance.licence_state = data['licence_state']
        instance.past_applied_date = data['past_applied_date']
        instance.past_applied_position = data['past_applied_position']
        # citizen_country = serializers.CharField()
        instance.govtjob_start_date = data['govtjob_start_date']
        instance.govtjob_end_date = data['govtjob_end_date']
        instance.judgment_felony = data['judgment_felony']
        instance.notary_lic_no =  data['notary_lic_no']
        instance.notary_issued = data['notary_issued']
        instance.notary_state = data['notary_state']
        instance.my_hiring_manager = data['my_hiring_manager']
        # instance.id_card = data['id_card']
        instance.level_education = data['level_education']
        instance.field_study = data['field_study']
        instance.school_colege = data['school_colege']
        instance.completed_year = data['completed_year']
        instance.study_location = data['study_location']
        instance.degree_cer = data['degree_cer']
        instance.skills = data['skills']
        instance.work_job_title = data['work_job_title']
        instance.work_company_name = data['work_company_name']
        instance.work_start_date = data['work_start_date']
        instance.starting_salary = data['starting_salary']
        instance.work_end_date = data['work_end_date']
        instance.final_salary = data['final_salary']
        instance.reason_leaving = data['reason_leaving']

        instance.work_review_y = data['work_review_yr']
        instance.expr_certi = data['expr_certi']
        instance.curent_busines = data['curent_busines']
        instance.past_business = data['past_business']
        instance.mariyo_work_type = data['mariyo_work_typee']
        instance.company_name = data['company_name']
        instance.company_address = data['company_address']
        instance.company_phone = data['company_phone']
        instance.company_email = data['company_email']
        instance.gst_number =data['gst_number']
        instance.gst_certificate =data['gst_certificate']
        instance.save()
        return instance
    
class edit_acc_Serializer(serializers.Serializer):
    office_name = serializers.CharField()
    office_country = serializers.CharField()
    office_city = serializers.CharField()
    office_address = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    personal_country = serializers.CharField()
    personal_city = serializers.CharField()
    personal_dob = serializers.CharField()
    personal_age = serializers.CharField()
    house_number= serializers.CharField()
    street_name = serializers.CharField()
    pin_code = serializers.CharField()
    profile_picture = serializers.CharField()
   

    def update(self, instance, data):
        instance.office_name = data['office_name']
        instance.office_country = data['office_country']
        instance.office_city = data['office_city']
        instance.office_address = data['office_address']
    
        instance.first_name = data['first_name']       
        instance.last_name = data['last_name']
        instance.personal_country = data['personal_country']
        instance.personal_city = data['personal_city']
        instance.personal_dob = data['personal_dob']
        instance.personal_age = data['personal_age']
        instance.house_numbe = data['house_numbe']
        instance.street_name = data['street_name']
        instance.pin_code = data['pin_code']
        instance.profile_picture = data['profile_picture']
        instance.save()
        return instance

#profile manager upload doc
class profile_manager_acc_Serializer(serializers.Serializer):
    office_name = serializers.CharField()
    office_country = serializers.CharField()
    office_city = serializers.CharField()
    office_address = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    personal_country = serializers.CharField()
    personal_city = serializers.CharField()
    personal_address = serializers.CharField()
    # notary = serializers.CharField()
    level_education = serializers.CharField()
    field_study = serializers.CharField()
    work_job_title = serializers.CharField()
    work_company_name = serializers.CharField()
    work_job_location = serializers.CharField()
    ex_job_title = serializers.CharField()
    ex_company_name = serializers.CharField()
    year_experience = serializers.CharField()
    ex_location = serializers.CharField()
    degree_cer = serializers.CharField()
    ex_cer = serializers.CharField()
    work_type = serializers.CharField()
    gst_number = serializers.CharField()
    gst_certificate = serializers.CharField()
    company_pan_no = serializers.CharField()
    arn_no =serializers.CharField()
    pan_card =serializers.CharField()

    id_card = serializers.CharField()
    sign_document = serializers.CharField()
    verification_img = serializers.CharField()

    def update(self, instance, data):
        instance.office_name = data['office_name']
        instance.office_country = data['office_country']
        instance.office_city = data['office_city']
        instance.office_address = data['office_address']
        instance.first_name = data['first_name']       
        instance.last_name = data['last_name']
        instance.personal_country = data['personal_country']
        instance.personal_city = data['personal_city']
        instance.personal_address = data['personal_address']
        # instance.notary = data['notary']
        instance.level_education = data['level_education']
        instance.field_study = data['field_study']
        instance.work_job_title = data['work_job_title']
        instance.work_company_name = data['work_company_name']
        instance.work_job_location = data['work_job_location']
        instance.ex_job_title = data['ex_job_title']
        instance.ex_company_name = data['ex_company_name']
        instance.year_experience = data['year_experience']
        instance.ex_location = data['ex_location']
        instance.degree_cer = data['degree_cer']
        instance.ex_cer = data['ex_cer']
        instance.work_type = data['work_type']
        instance.gst_number = data['gst_number']
        instance.gst_certificate = data['gst_certificate']
        instance.company_pan_no = data['company_pan_no']
        instance.arn_no =data['arn_no']
        instance.pan_card =data['pan_card']

        instance.id_card = data['id_card']
        instance.sign_document = data['sign_document']
        instance.verification_img =data['verification_img']

        instance.save()
        return instance
    
#ad provider upload doc
class ad_provider_acc_Serializer(serializers.Serializer):
    office_name = serializers.CharField()
    office_country = serializers.CharField()
    office_city = serializers.CharField()
    office_address = serializers.CharField()

    first_name = serializers.CharField()
    last_name = serializers.CharField()
    personal_country = serializers.CharField()
    personal_city = serializers.CharField()
    personal_address = serializers.CharField()
    # notary = serializers.CharField()
    level_education = serializers.CharField()
    field_study = serializers.CharField()
    work_job_title = serializers.CharField()
    work_company_name = serializers.CharField()
    work_job_location = serializers.CharField()
    ex_job_title = serializers.CharField()
    ex_company_name = serializers.CharField()
    year_experience = serializers.CharField()
    ex_location = serializers.CharField()
    degree_cer = serializers.CharField()
    ex_cer = serializers.CharField()
    work_type = serializers.CharField()
    gst_number = serializers.CharField()
    gst_certificate = serializers.CharField()
    company_pan_no = serializers.CharField()
    arn_no =serializers.CharField()
    pan_card =serializers.CharField()

    id_card = serializers.CharField()
    sign_document = serializers.CharField()
    verification_img = serializers.CharField()
    def update(self, instance, data):
        instance.office_name = data['office_name']
        instance.office_country = data['office_country']
        instance.office_city = data['office_city']
        instance.office_address = data['office_address']
        instance.first_name = data['first_name']       
        instance.last_name = data['last_name']
        instance.personal_country = data['personal_country']
        instance.personal_city = data['personal_city']
        instance.personal_address = data['personal_address']
        # instance.notary = data['notary']
        instance.level_education = data['level_education']
        instance.field_study = data['field_study']
        instance.work_job_title = data['work_job_title']
        instance.work_company_name = data['work_company_name']
        instance.work_job_location = data['work_job_location']
        instance.ex_job_title = data['ex_job_title']
        instance.ex_company_name = data['ex_company_name']
        instance.year_experience = data['year_experience']
        instance.ex_location = data['ex_location']
        instance.degree_cer = data['degree_cer']
        instance.ex_cer = data['ex_cer']
        instance.work_type = data['work_type']
        instance.gst_number = data['gst_number']
        instance.gst_certificate = data['gst_certificate']
        instance.company_pan_no = data['company_pan_no']
        instance.arn_no =data['arn_no']
        instance.pan_card =data['pan_card']

        instance.id_card = data['id_card']
        instance.sign_document = data['sign_document']
        instance.verification_img =data['verification_img']
        instance.save()
        return instance

#ad distributor upload doc
class ad_distributor_acc_Serializer(serializers.Serializer):
    office_name = serializers.CharField()
    office_country = serializers.CharField()
    office_city = serializers.CharField()
    office_address = serializers.CharField()

    first_name = serializers.CharField()
    last_name = serializers.CharField()
    personal_country = serializers.CharField()
    personal_city = serializers.CharField()
    personal_address = serializers.CharField()
    # notary = serializers.CharField()
    level_education = serializers.CharField()
    field_study = serializers.CharField()
    work_job_title = serializers.CharField()
    work_company_name = serializers.CharField()
    work_job_location = serializers.CharField()
    ex_job_title = serializers.CharField()
    ex_company_name = serializers.CharField()
    year_experience = serializers.CharField()
    ex_location = serializers.CharField()
    degree_cer = serializers.CharField()
    ex_cer = serializers.CharField()
    work_type = serializers.CharField()
    gst_number = serializers.CharField()
    gst_certificate = serializers.CharField()
    company_pan_no = serializers.CharField()
    arn_no =serializers.CharField()
    pan_card =serializers.CharField()

    id_card = serializers.CharField()
    sign_document = serializers.CharField()
    verification_img = serializers.CharField()

    def update(self, instance, data):
        instance.office_name = data['office_name']
        instance.office_country = data['office_country']
        instance.office_city = data['office_city']
        instance.office_address = data['office_address']
        instance.first_name = data['first_name']       
        instance.last_name = data['last_name']
        instance.personal_country = data['personal_country']
        instance.personal_city = data['personal_city']
        instance.personal_address = data['personal_address']
        # instance.notary = data['notary']
        instance.level_education = data['level_education']
        instance.field_study = data['field_study']
        instance.work_job_title = data['work_job_title']
        instance.work_company_name = data['work_company_name']
        instance.work_job_location = data['work_job_location']
        instance.ex_job_title = data['ex_job_title']
        instance.ex_company_name = data['ex_company_name']
        instance.year_experience = data['year_experience']
        instance.ex_location = data['ex_location']
        instance.degree_cer = data['degree_cer']
        instance.ex_cer = data['ex_cer']
        instance.work_type = data['work_type']
        instance.gst_number = data['gst_number']
        instance.gst_certificate = data['gst_certificate']
        instance.company_pan_no = data['company_pan_no']
        instance.arn_no =data['arn_no']
        instance.pan_card =data['pan_card']

        instance.id_card = data['id_card']
        instance.sign_document = data['sign_document']
        instance.verification_img =data['verification_img']
        instance.save()
        return instance

#sales upload doc
class sales_acc_Serializer(serializers.Serializer):
    full_name = serializers.CharField()
    personal_country = serializers.CharField()
    personal_city = serializers.CharField()
    personal_address = serializers.CharField()

    level_education = serializers.CharField()
    field_study = serializers.CharField()
    work_job_title = serializers.CharField()
    work_company_name = serializers.CharField()
    work_job_location = serializers.CharField()
    ex_job_title = serializers.CharField()
    ex_company_name = serializers.CharField()
    year_experience = serializers.CharField()
    ex_location = serializers.CharField()
    degree_cer = serializers.CharField()
    ex_cer = serializers.CharField()
    work_type = serializers.CharField()
    gst_number = serializers.CharField()
    gst_certificate = serializers.CharField()
    company_pan_no = serializers.CharField()
    arn_no =serializers.CharField()
    pan_card =serializers.CharField()

    id_card = serializers.CharField()
    sign_document = serializers.CharField()
    verification_img = serializers.CharField()

    def update(self, instance, data):
        instance.full_name = data['full_name']
        instance.personal_country = data['personal_country']
        instance.personal_city = data['personal_city']
        instance.personal_address = data['personal_address']
        instance.level_education = data['level_education']
        instance.field_study = data['field_study']
        instance.work_job_title = data['work_job_title']
        instance.work_company_name = data['work_company_name']
        instance.work_job_location = data['work_job_location']
        instance.ex_job_title = data['ex_job_title']
        instance.ex_company_name = data['ex_company_name']
        instance.year_experience = data['year_experience']
        instance.ex_location = data['ex_location']
        instance.degree_cer = data['degree_cer']
        instance.ex_cer = data['ex_cer']
        instance.work_type = data['work_type']
        instance.gst_number = data['gst_number']
        instance.gst_certificate = data['gst_certificate']
        instance.company_pan_no = data['company_pan_no']
        instance.arn_no =data['arn_no']
        instance.pan_card =data['pan_card']

        instance.id_card = data['id_card']
        instance.sign_document = data['sign_document']
        instance.verification_img =data['verification_img']
    
        instance.save()
        return instance

#hiring manager upload doc
class hiring_acc_Serializer(serializers.Serializer):
    office_name = serializers.CharField()
    office_country = serializers.CharField()
    office_city = serializers.CharField()
    office_address = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    personal_country = serializers.CharField()
    personal_city = serializers.CharField()
    personal_address = serializers.CharField()
    level_education = serializers.CharField()
    field_study = serializers.CharField()
    work_job_title = serializers.CharField()
    work_company_name = serializers.CharField()
    work_job_location = serializers.CharField()
    ex_job_title = serializers.CharField()
    ex_company_name = serializers.CharField()
    year_experience = serializers.CharField()
    ex_location = serializers.CharField()
    degree_cer = serializers.CharField()
    ex_cer = serializers.CharField()
    work_type = serializers.CharField()
    gst_number = serializers.CharField()
    gst_certificate = serializers.CharField()
    company_pan_no = serializers.CharField()
    arn_no =serializers.CharField()
    pan_card =serializers.CharField()

    id_card = serializers.CharField()
    sign_document = serializers.CharField()
    verification_img = serializers.CharField()
    def update(self, instance, data):
        instance.office_name = data['office_name']
        instance.office_country = data['office_country']
        instance.office_city = data['office_city']
        instance.office_address = data['office_address']
    

        instance.first_name = data['first_name']       
        instance.last_name = data['last_name']
        instance.personal_country = data['personal_country']
        instance.personal_city = data['personal_city']
        instance.personal_address = data['personal_address']
        # instance.notary = data['notary']
        instance.level_education = data['level_education']
        instance.field_study = data['field_study']
        instance.work_job_title = data['work_job_title']
        instance.work_company_name = data['work_company_name']
        instance.work_job_location = data['work_job_location']
        instance.ex_job_title = data['ex_job_title']
        instance.ex_company_name = data['ex_company_name']
        instance.year_experience = data['year_experience']
        instance.ex_location = data['ex_location']
        instance.degree_cer = data['degree_cer']
        instance.ex_cer = data['ex_cer']
        instance.work_type = data['work_type']
        instance.gst_number = data['gst_number']
        instance.gst_certificate = data['gst_certificate']
        instance.company_pan_no = data['company_pan_no']
        instance.arn_no =data['arn_no']
        instance.pan_card =data['pan_card']

        instance.id_card = data['id_card']
        instance.sign_document = data['sign_document']
        instance.verification_img =data['verification_img']
        instance.save()
        return instance

#ad provider upload doc
class affiliate_marketing_acc_Serializer(serializers.Serializer):
    full_name = serializers.CharField()
    personal_country = serializers.CharField()
    personal_city = serializers.CharField()
    personal_address = serializers.CharField()

    level_education = serializers.CharField()
    field_study = serializers.CharField()
    work_job_title = serializers.CharField()
    work_company_name = serializers.CharField()
    work_job_location = serializers.CharField()
    ex_job_title = serializers.CharField()
    ex_company_name = serializers.CharField()
    year_experience = serializers.CharField()
    ex_location = serializers.CharField()
    degree_cer = serializers.CharField()
    ex_cer = serializers.CharField()
    work_type = serializers.CharField()
    gst_number = serializers.CharField()
    gst_certificate = serializers.CharField()
    company_pan_no = serializers.CharField()
    arn_no =serializers.CharField()
    pan_card =serializers.CharField()

    id_card = serializers.CharField()
    sign_document = serializers.CharField()
    verification_img = serializers.CharField()

    def update(self, instance, data):
        instance.full_name = data['full_name']
        instance.personal_country = data['personal_country']
        instance.personal_city = data['personal_city']
        instance.personal_address = data['personal_address']
        instance.level_education = data['level_education']
        instance.field_study = data['field_study']
        instance.work_job_title = data['work_job_title']
        instance.work_company_name = data['work_company_name']
        instance.work_job_location = data['work_job_location']
        instance.ex_job_title = data['ex_job_title']
        instance.ex_company_name = data['ex_company_name']
        instance.year_experience = data['year_experience']
        instance.ex_location = data['ex_location']
        instance.degree_cer = data['degree_cer']
        instance.ex_cer = data['ex_cer']
        instance.work_type = data['work_type']
        instance.gst_number = data['gst_number']
        instance.gst_certificate = data['gst_certificate']
        instance.company_pan_no = data['company_pan_no']
        instance.arn_no =data['arn_no']
        instance.pan_card =data['pan_card']

        instance.id_card = data['id_card']
        instance.sign_document = data['sign_document']
        instance.verification_img =data['verification_img']
    
        instance.save()
        return instance
#ad provider upload doc
class private_investigator_acc_Serializer(serializers.Serializer):
    office_name = serializers.CharField()
    office_country = serializers.CharField()
    office_city = serializers.CharField()
    office_address = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    personal_country = serializers.CharField()
    personal_city = serializers.CharField()
    personal_address = serializers.CharField()
    level_education = serializers.CharField()
    field_study = serializers.CharField()
    work_job_title = serializers.CharField()
    work_company_name = serializers.CharField()
    work_job_location = serializers.CharField()
    ex_job_title = serializers.CharField()
    ex_company_name = serializers.CharField()
    year_experience = serializers.CharField()
    ex_location = serializers.CharField()
    degree_cer = serializers.CharField()
    ex_cer = serializers.CharField()
    work_type = serializers.CharField()
    gst_number = serializers.CharField()
    gst_certificate = serializers.CharField()
    company_pan_no = serializers.CharField()
    arn_no =serializers.CharField()
    pan_card =serializers.CharField()

    id_card = serializers.CharField()
    sign_document = serializers.CharField()
    verification_img = serializers.CharField()

    def update(self, instance, data):
        instance.office_name = data['office_name']
        instance.office_country = data['office_country']
        instance.office_city = data['office_city']
        instance.office_address = data['office_address']
    

        instance.first_name = data['first_name']       
        instance.last_name = data['last_name']
        instance.personal_country = data['personal_country']
        instance.personal_city = data['personal_city']
        instance.personal_address = data['personal_address']
        # instance.notary = data['notary']
        instance.level_education = data['level_education']
        instance.field_study = data['field_study']
        instance.work_job_title = data['work_job_title']
        instance.work_company_name = data['work_company_name']
        instance.work_job_location = data['work_job_location']
        instance.ex_job_title = data['ex_job_title']
        instance.ex_company_name = data['ex_company_name']
        instance.year_experience = data['year_experience']
        instance.ex_location = data['ex_location']
        instance.degree_cer = data['degree_cer']
        instance.ex_cer = data['ex_cer']
        instance.work_type = data['work_type']
        instance.gst_number = data['gst_number']
        instance.gst_certificate = data['gst_certificate']
        instance.company_pan_no = data['company_pan_no']
        instance.arn_no =data['arn_no']
        instance.pan_card =data['pan_card']

        instance.id_card = data['id_card']
        instance.sign_document = data['sign_document']
        instance.verification_img =data['verification_img']
        instance.save()
        return instance

#my profile manager 
class my_profile_manager_Serializer(serializers.Serializer):
    my_profile_manager = serializers.CharField()
    
    def update(self, instance, data):
        instance.my_profile_manager = data['my_profile_manager']
        instance.save()
        return instance
#ad provider  
class ad_provider_Serializer(serializers.Serializer):
    ad_provider = serializers.CharField()
    
    def update(self, instance, data):
        instance.ad_provider = data['ad_provider']
        instance.save()
        return instance

#ad distributor  
class ad_distributor_Serializer(serializers.Serializer):
    ad_distributor = serializers.CharField()
    
    def update(self, instance, data):
        instance.ad_distributor = data['ad_distributor']
        instance.save()
        return instance


#sales manager  
class sales_manager_Serializer(serializers.Serializer):
    sales_manager = serializers.CharField()
    
    def update(self, instance, data):
        instance.sales_manager = data['sales_manager']
        instance.save()
        return instance
#hiring manager  
class hiring_manager_Serializer(serializers.Serializer):
    hiring_manager = serializers.CharField()
    
    def update(self, instance, data):
        instance.hiring_manager = data['hiring_manager']
        instance.save()
        return instance

#affiliate marketing   
class affiliate_markting_Serializer(serializers.Serializer):
    affiliate_marketing = serializers.CharField()
    
    def update(self, instance, data):
        instance.affiliate_marketing = data['affiliate_marketing']
        instance.save()
        return instance

#Private Investigator   
class private_investigator_Serializer(serializers.Serializer):
    private_investigator = serializers.CharField()
    
    def update(self, instance, data):
        instance.private_investigator = data['private_investigator']
        instance.save()
        return instance
class add_used_Serializer(serializers.Serializer):
    aid =  serializers.CharField()
    uid =  serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    mobile = serializers.CharField()
    access_Privileges = serializers.CharField()
    password = serializers.CharField()
    work = serializers.CharField()
    # creator = serializers.CharField()
    # location=serializers.CharField()
    def create(self, data):
        return users.objects.create(
            aid = data['aid'],
            uid = data['uid'],
            first_name = data['first_name'],
            last_name = data['last_name'],
            email = data['email'],
            mobile = data['mobile'],
            access_Privileges = data['access_Privileges'],
            password = data['password'],
            work = data['work'],
            # creator = data['creator'],
            # location=data['location'],

        )
    
class hiringedit_user_Serializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    mobile = serializers.CharField()
    access_Privileges = serializers.CharField()
    password = serializers.CharField()
    # location=serializers.CharField()


    def update(self, instance, data):
        instance.first_name = data['first_name']
        instance.last_name = data['last_name']
        instance.email = data['email']
        instance.mobile = data['mobile']
        instance.access_Privileges = data['access_Privileges']
        instance.password = data['password']
        # instance.location=data['location']
        instance.save()
        return instance
    

class update_email_serializer(serializers.Serializer):
    email = serializers.CharField()
    def update (self,instance,data):
        instance.email=data["email"]
        instance.save()
        return instance
    
class update_password_serializer(serializers.Serializer):
    password = serializers.CharField()
    def update (self,instance,data):
        instance.password=data["password"]
        instance.save()
        return instance
    
class update_otp_serializer(serializers.Serializer):
    otp1 = serializers.IntegerField()
    def update(self, instance, data):
        instance.otp1 = data['otp1']
        instance.save()
        return instance
    
class OTP1Serializer(serializers.Serializer):
    user_otp1 = serializers.IntegerField()
    
    def update(self, instance, data):
        instance.user_otp1 = data['user_otp1']
        instance.save()
        return instance