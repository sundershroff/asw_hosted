
from rest_framework import serializers
from virtualExpert.models import salesmanager,ad_client,users

class salesmanagerSerializer(serializers.Serializer):
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
    full_name = serializers.CharField()
    personal_country = serializers.CharField()
    personal_city = serializers.CharField()
    personal_address = serializers.CharField()
    hiring_manager = serializers.CharField()
    id_card = serializers.CharField()
    created_date = serializers.CharField()
    otp1 = serializers.IntegerField()
    user_otp1 = serializers.IntegerField()

    ad_provider=serializers.CharField()
    ad_distributor=serializers.CharField()
    my_profile_manager=serializers.CharField()
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



class SignupSerializer(serializers.Serializer):
    uid = serializers.CharField()
    email = serializers.EmailField()
    mobile = serializers.CharField()
    password = serializers.CharField()
    otp = serializers.IntegerField()
    created_date = serializers.CharField()
    
    def create(self, data):
        return salesmanager.objects.create(
            uid = data['uid'],
            email = data['email'],
            mobile = data['mobile'],
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
    full_name = serializers.CharField()
    personal_country = serializers.CharField()
    personal_city = serializers.CharField()
    personal_address = serializers.CharField()
    hiring_manager = serializers.CharField()
    # id_card = serializers.CharField()
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
   

    def update(self, instance, data):
        instance.full_name = data['full_name']
        instance.personal_country = data['personal_country']
        instance.personal_city = data['personal_city']
        instance.personal_address = data['personal_address']
        instance.hiring_manager = data['hiring_manager']
        # instance.profile_picture= data['profile_picture']
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
        instance.save()
        return instance

class update_acc_serializer(serializers.Serializer):
    full_name = serializers.CharField()
    personal_country = serializers.CharField()
    personal_city = serializers.CharField()
    personal_address = serializers.CharField()
    profile_picture=serializers.CharField()
    def update(self,instance,data):
        instance.full_name=data["full_name"]
        instance.personal_country = data['personal_country']
        instance.personal_city = data['personal_city']
        instance.personal_address = data['personal_address']
        instance.profile_picture=data["profile_picture"]
        instance.save()
        return instance
    
class sm_add_client_serializer(serializers.Serializer):
    
    uid=serializers.CharField()
    sales_id=serializers.CharField(read_only=True)
    client_type=serializers.CharField()
    client_name=serializers.CharField()
    client_location=serializers.CharField()
    category=serializers.CharField()
    google_map=serializers.CharField()
    phone_number=serializers.CharField()
    email=serializers.EmailField()
    picture=serializers.CharField()
    status=serializers.BooleanField()
    types_of_activities=serializers.CharField()
    date=serializers.CharField()
    time=serializers.CharField()
    notes=serializers.CharField()
    otp = serializers.IntegerField()
    user_otp = serializers.IntegerField()
    active_status=serializers.BooleanField()


class add_client_serializer(serializers.Serializer):
    uid=serializers.CharField()
    sales_id=serializers.CharField()
    client_type=serializers.CharField()
    client_name=serializers.CharField()
    client_location=serializers.CharField()
    category=serializers.CharField()
    google_map=serializers.CharField()
    phone_number=serializers.CharField()
    email=serializers.EmailField()
    picture=serializers.CharField()
    # status=serializers.BooleanField()

    # otp = serializers.IntegerField()
    def create(self,data):
        return ad_client.objects.create(
            uid = data['uid'],
            sales_id=data['sales_id'],
            client_type=data['client_type'],
            client_name=data['client_name'],
            client_location=data['client_location'],
            category=data["category"],
            google_map=data['google_map'],
            phone_number = data['phone_number'],
            email = data['email'],
            picture=data['picture'],
            # status=data['status'],
            # otp = data['otp'],
        )
    
class update_clientotp_serializer(serializers.Serializer):
    otp = serializers.IntegerField()
   
    def update(self, instance, data):
        instance.otp = data['otp']
        instance.save()
        return instance

class OTPclientSerializer(serializers.Serializer):

    user_otp = serializers.IntegerField()
    
    def update(self, instance, data):
        instance.user_otp = data['user_otp']
        instance.save()
        return instance

class client_activities_serializer(serializers.Serializer):
    # sales_id=serializers.CharField()
    types_of_activities=serializers.CharField()
    date=serializers.CharField()
    time=serializers.CharField()
    notes=serializers.CharField()
    # status=serializers.BooleanField()


    def update(self,instance,data):
            
        instance.types_of_activities=data["types_of_activities"]
        instance.date=data["date"]
        instance.time=data["time"]
        instance.notes=data["notes"]
        # instance.status=data["status"]
        instance.save()
        return instance

class all_activities_serializer(serializers.Serializer):
    # sales_id=serializers.CharField(read_only=True)

    client_name=serializers.CharField()
    types_of_activities=serializers.CharField()
    date=serializers.CharField()
    time=serializers.CharField()
    notes=serializers.CharField()
    status=serializers.BooleanField()

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
    
class salesedit_user_Serializer(serializers.Serializer):
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