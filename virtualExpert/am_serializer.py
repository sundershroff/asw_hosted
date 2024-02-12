
from rest_framework import serializers
from virtualExpert.models import affliate_marketing,users

class affliatemarketingSerializer(serializers.Serializer):
    # User ID
    uid = serializers.CharField()

    # Signup
    email = serializers.EmailField()
    mobile = serializers.CharField()
    password = serializers.CharField()
    otp = serializers.IntegerField()
    user_otp = serializers.IntegerField()
    referral_code=serializers.CharField()
    profile_picture = serializers.CharField()


     #Edit Account
    full_name = serializers.CharField()
    personal_country = serializers.CharField()
    personal_city = serializers.CharField()
    personal_address = serializers.CharField()
    hiring_manager = serializers.CharField()
    id_card = serializers.CharField()
    created_date = serializers.DateField()
    created_time =serializers.CharField()
    coin=serializers.CharField()
    otp1 = serializers.IntegerField()
    user_otp1 = serializers.IntegerField()

class SignupSerializer(serializers.Serializer):
    uid = serializers.CharField()
    email = serializers.EmailField()
    mobile = serializers.CharField()
    password = serializers.CharField()
    otp = serializers.IntegerField()
    # created_date = serializers.CharField()
    created_time=serializers.CharField()
    referral_code=serializers.CharField()
  

    def create(self, data):
        return affliate_marketing.objects.create(
            uid = data['uid'],
            email = data['email'],
            mobile = data['mobile'],
            password = data['password'],
            otp = data['otp'],
            # created_date = data['created_date'],
            created_time = data['created_time'],
            referral_code = data['referral_code'],   
        )

class aff_coin_serializer(serializers.Serializer):
    coin=serializers.CharField()
    
    def update(self, instance,data):
        instance.coin=data["coin"]
        instance.save()
        return instance
    



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
    # profile_picture = serializers.CharField()

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






class am_all_serializer(serializers.Serializer):
    full_name = serializers.CharField()
    personal_country = serializers.CharField()
    personal_city = serializers.CharField()
    personal_address = serializers.CharField()
    hiring_manager = serializers.CharField()
    profile_picture = serializers.CharField()

class update_email_serializer(serializers.Serializer):
    email = serializers.CharField()
    def update (self,instance,data):
        instance.email=data["email"]
        instance.save()
        return instance
    
class update_pass_aff_serializer(serializers.Serializer):
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

        )
    
class affedit_user_Serializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    mobile = serializers.CharField()
    access_Privileges = serializers.CharField()
    password = serializers.CharField()


    def update(self, instance, data):
        instance.first_name = data['first_name']
        instance.last_name = data['last_name']
        instance.email = data['email']
        instance.mobile = data['mobile']
        instance.access_Privileges = data['access_Privileges']
        instance.password = data['password']
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
    