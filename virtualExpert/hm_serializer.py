
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
    personal_address = serializers.CharField()
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


class SignupSerializer(serializers.Serializer):
    uid = serializers.CharField()
    email = serializers.EmailField()
    mobile = serializers.CharField()
    password = serializers.CharField()
    otp = serializers.IntegerField()
    created_date = serializers.CharField()
    
    def create(self, data):
        return hiringmanager.objects.create(
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
    # office_name = serializers.CharField()
    # office_country = serializers.CharField()
    # office_city = serializers.CharField()
    # office_address = serializers.CharField()

    first_name = serializers.CharField()
    last_name = serializers.CharField()
    personal_country = serializers.CharField()
    personal_city = serializers.CharField()
    personal_address = serializers.CharField()
    my_hiring_manager = serializers.CharField()
    # id_card = serializers.CharField()

    def update(self, instance, data):
        # instance.office_name = data['office_name']
        # instance.office_country = data['office_country']
        # instance.office_city = data['office_city']
        # instance.office_address = data['office_address']
    
        instance.first_name = data['first_name']       
        instance.last_name = data['last_name']
        instance.personal_country = data['personal_country']
        instance.personal_city = data['personal_city']
        instance.personal_address = data['personal_address']
        instance.my_hiring_manager = data['my_hiring_manager']
        # instance.id_card = data['id_card']
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
    personal_address = serializers.CharField()
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
        instance.personal_address = data['personal_address']
        instance.profile_picture = data['profile_picture']
        instance.save()
        return instance

#profile manager upload doc
class profile_manager_acc_Serializer(serializers.Serializer):
    office_name = serializers.CharField()
    office_country = serializers.CharField()
    office_city = serializers.CharField()
    office_address = serializers.CharField()

    id_card = serializers.CharField()
    sign_document = serializers.CharField()

    def update(self, instance, data):
        instance.office_name = data['office_name']
        instance.office_country = data['office_country']
        instance.office_city = data['office_city']
        instance.office_address = data['office_address']
    

        instance.id_card = data['id_card']
        instance.sign_document = data['sign_document']
        instance.save()
        return instance
    
#ad provider upload doc
class ad_provider_acc_Serializer(serializers.Serializer):
    office_name = serializers.CharField()
    office_country = serializers.CharField()
    office_city = serializers.CharField()
    office_address = serializers.CharField()

    id_card = serializers.CharField()
    sign_document = serializers.CharField()

    def update(self, instance, data):
        instance.office_name = data['office_name']
        instance.office_country = data['office_country']
        instance.office_city = data['office_city']
        instance.office_address = data['office_address']
    

        instance.id_card = data['id_card']
        instance.sign_document = data['sign_document']
        instance.save()
        return instance

#ad distributor upload doc
class ad_distributor_acc_Serializer(serializers.Serializer):
    office_name = serializers.CharField()
    office_country = serializers.CharField()
    office_city = serializers.CharField()
    office_address = serializers.CharField()

    id_card = serializers.CharField()
    sign_document = serializers.CharField()

    def update(self, instance, data):
        instance.office_name = data['office_name']
        instance.office_country = data['office_country']
        instance.office_city = data['office_city']
        instance.office_address = data['office_address']
    

        instance.id_card = data['id_card']
        instance.sign_document = data['sign_document']
        instance.save()
        return instance

#sales upload doc
class sales_acc_Serializer(serializers.Serializer):
    full_name = serializers.CharField()
    personal_country = serializers.CharField()
    personal_city = serializers.CharField()
    personal_address = serializers.CharField()

    id_card = serializers.CharField()
    sign_document = serializers.CharField()

    def update(self, instance, data):
        instance.full_name = data['full_name']
        instance.personal_country = data['personal_country']
        instance.personal_city = data['personal_city']
        instance.personal_address = data['personal_address']
    

        instance.id_card = data['id_card']
        instance.sign_document = data['sign_document']
        instance.save()
        return instance

#hiring manager upload doc
class hiring_acc_Serializer(serializers.Serializer):
    office_name = serializers.CharField()
    office_country = serializers.CharField()
    office_city = serializers.CharField()
    office_address = serializers.CharField()

    id_card = serializers.CharField()
    sign_document = serializers.CharField()

    def update(self, instance, data):
        instance.office_name = data['office_name']
        instance.office_country = data['office_country']
        instance.office_city = data['office_city']
        instance.office_address = data['office_address']
    

        instance.id_card = data['id_card']
        instance.sign_document = data['sign_document']
        instance.save()
        return instance

#ad provider upload doc
class affiliate_marketing_acc_Serializer(serializers.Serializer):
    full_name = serializers.CharField()
    personal_country = serializers.CharField()
    personal_city = serializers.CharField()
    personal_address = serializers.CharField()

    id_card = serializers.CharField()
    sign_document = serializers.CharField()

    def update(self, instance, data):
        instance.full_name = data['full_name']
        instance.personal_country = data['personal_country']
        instance.personal_city = data['personal_city']
        instance.personal_address = data['personal_address']
    

        instance.id_card = data['id_card']
        instance.sign_document = data['sign_document']
        instance.save()
        return instance
#ad provider upload doc
class private_investigator_acc_Serializer(serializers.Serializer):
    office_name = serializers.CharField()
    office_country = serializers.CharField()
    office_city = serializers.CharField()
    office_address = serializers.CharField()
    id_card = serializers.CharField()
    sign_document = serializers.CharField()

    def update(self, instance, data):
        instance.office_name = data['office_name']
        instance.office_country = data['office_country']
        instance.office_city = data['office_city']
        instance.office_address = data['office_address']
    

        instance.id_card = data['id_card']
        instance.sign_document = data['sign_document']
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
    uid =  serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    mobile = serializers.CharField()
    access_Privileges = serializers.CharField()
    password = serializers.CharField()
    work = serializers.CharField()
    creator = serializers.CharField()
    # location=serializers.CharField()
    def create(self, data):
        return users.objects.create(
            uid = data['uid'],
            first_name = data['first_name'],
            last_name = data['last_name'],
            email = data['email'],
            mobile = data['mobile'],
            access_Privileges = data['access_Privileges'],
            password = data['password'],
            work = data['work'],
            creator = data['creator'],
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