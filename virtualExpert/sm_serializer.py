
from rest_framework import serializers
from virtualExpert.models import salesmanager,ad_client

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
    my_profile_manager = serializers.CharField()
    ad_provider = serializers.CharField() 
    ad_distributor = serializers.CharField()
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
   

    def update(self, instance, data):
        instance.full_name = data['full_name']
        instance.personal_country = data['personal_country']
        instance.personal_city = data['personal_city']
        instance.personal_address = data['personal_address']
        instance.hiring_manager = data['hiring_manager']
        # instance.profile_picture= data['profile_picture']
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

    otp = serializers.IntegerField()
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
            otp = data['otp'],
        )
    


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
    status=serializers.BooleanField()


    def update(self,instance,data):
            
        instance.types_of_activities=data["types_of_activities"]
        instance.date=data["date"]
        instance.time=data["time"]
        instance.notes=data["notes"]
        instance.status=data["status"]
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