
from rest_framework import serializers
from virtualExpert.models import Profilemanager,users

class ProfilemanagerSerializer(serializers.Serializer):
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
    notary = serializers.CharField()
    id_card = serializers.CharField()
    
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
        return Profilemanager.objects.create(
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
    notary = serializers.CharField()
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
        instance.notary = data['notary']
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
    notary = serializers.CharField()
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
        instance.notary = data['notary']
        instance.profile_picture = data['profile_picture']
        instance.save()
        return instance

class my_client_serializer(serializers.Serializer):
    # my_client = serializers.CharField(source=ProfileFinder, read_only=True)
    my_client = serializers.CharField()
    def update(self, instance, data):
        instance.my_client = data['my_client']
        instance.save()
        return instance


class add_used_Serializer(serializers.Serializer):
    uid =  serializers.CharField()
    aid = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    mobile = serializers.CharField()
    access_Privileges = serializers.CharField()
    password = serializers.CharField()
    work = serializers.CharField()
    # creator = serializers.CharField()
    my_client = serializers.CharField()
    # location = serializers.CharField()

    
    def create(self, data):
        return users.objects.create(
            uid = data['uid'],
            aid = data['aid'],
            first_name = data['first_name'],
            last_name = data['last_name'],
            email = data['email'],
            mobile = data['mobile'],
            access_Privileges = data['access_Privileges'],
            password = data['password'],
            work = data['work'],
            # creator = data['creator'],
            my_client = data['my_client'],
            # location = data['location'],
        )
class eedit_user_Serializer(serializers.Serializer):
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