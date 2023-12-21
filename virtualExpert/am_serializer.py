
from rest_framework import serializers
from virtualExpert.models import affliate_marketing

class affliatemarketingSerializer(serializers.Serializer):
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

class SignupSerializer(serializers.Serializer):
    uid = serializers.CharField()
    email = serializers.EmailField()
    mobile = serializers.CharField()
    password = serializers.CharField()
    otp = serializers.IntegerField()
    created_date = serializers.CharField()
    
    def create(self, data):
        return affliate_marketing.objects.create(
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

    # profile_picture = serializers.CharField()

    # id_card = serializers.CharField()

   

    def update(self, instance, data):
        instance.full_name = data['full_name']
        instance.personal_country = data['personal_country']
        instance.personal_city = data['personal_city']
        instance.personal_address = data['personal_address']
        instance.hiring_manager = data['hiring_manager']

        # instance.profile_picture = data['profile_picture']
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
    
class update_password_serializer(serializers.Serializer):
    password = serializers.CharField()
    
    def update (self,instance,data):
        instance.password=data["password"]

        # instance.id_card = data['id_card']

        instance.save()
        return instance