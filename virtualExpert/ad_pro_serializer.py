
from rest_framework import serializers
from virtualExpert.models import ad_provider,ad_pro_ads,users
from datetime import date,datetime


class adproviderSerializer(serializers.Serializer):
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
    id_card = serializers.CharField()
    hiring_manager = serializers.CharField()
    sales_manager = serializers.CharField()
    created_date = serializers.CharField()
    otp1 = serializers.IntegerField()
    user_otp1 = serializers.IntegerField()
    type=serializers.CharField()

class SignupSerializer(serializers.Serializer):
    uid = serializers.CharField()
    email = serializers.EmailField()
    mobile = serializers.CharField()
    password = serializers.CharField()
    otp = serializers.IntegerField()
    created_date = serializers.CharField()
    
    def create(self, data):
        return ad_provider.objects.create(
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

# //// Complete profile or Ad_provider Account updation/////

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
    # id_card = serializers.CharField()
    hiring_manager = serializers.CharField()
    sales_manager = serializers.CharField()
    type=serializers.CharField()
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
        # instance.id_card = data['id_card']
        instance.hiring_manager = data['hiring_manager']
        instance.sales_manager = data['sales_manager']
        instance.type=data['type']
        instance.save()
        return instance
    
# ///// Editing Ad_Provider Account//////   
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
    # notary = serializers.CharField()
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
        # instance.notary = data['notary']
        instance.profile_picture = data['profile_picture']
        instance.save()
        return instance


#//// create new Ads ///// 
class create_ads_Serializer(serializers.Serializer):
    ad_id = serializers.CharField()
    ad_name=serializers.CharField()
    ad_pro=serializers.CharField()
    category=serializers.CharField()
    ad_type=serializers.CharField()
    languages=serializers.CharField()
    office_country=serializers.CharField()
    office_state=serializers.CharField()
    office_district=serializers.CharField()
    gender=serializers.CharField()
    age_range=serializers.CharField()
    age_to=serializers.CharField()
    id_card = serializers.CharField()
    no_views=serializers.CharField()
    days_required=serializers.CharField()
    times_repeat=serializers.CharField()
    ad_details=serializers.CharField()
    other_ads=serializers.CharField()
    action_name=serializers.CharField()
    action_url=serializers.CharField()
    status=serializers.CharField()
    ad_created_date=serializers.CharField()
    ad_created_time=serializers.CharField()
    # coin=serializers.CharField()
    # commission=serializers.CharField()

    def create(self, data):
        return ad_pro_ads.objects.create(
            ad_id = data['ad_id'],
            ad_name = data['ad_name'],
            ad_pro=data['ad_pro'],
            category=data['category'],
            ad_type=data['ad_type'],
            languages=data['languages'],
            office_country=data['office_country'],
            office_state=data['office_state'],
            office_district=data['office_district'],
            gender=data['gender'],
            age_range=data['age_range'],
            age_to=data['age_to'],
            id_card=data['id_card'],
            no_views=data['no_views'],
            days_required=data['days_required'],
            times_repeat=data['times_repeat'],
            ad_details=data['ad_details'],
            other_ads=data['other_ads'],
            action_name=data['action_name'],
            action_url=data['action_url'],
            status=data['status'],
            ad_created_date=data['ad_created_date'],
            ad_created_time=data['ad_created_time'],
            # coin=data['coin'],
            # commission=data['commission'],
            )
    

# def update_status_to_deactive(self, instance):
#         last_date= datetime.strptime(instance.days_required, "%Y-%m-%d")
#         if last_date == date.today():
#             instance.status = "Deactive"
#             instance.save()
#         return instance    

#/// Get Ads Details//// 
class list_ads_Serializer(serializers.Serializer):
    ad_id=serializers.CharField()
    ad_name=serializers.CharField()
    ad_pro=serializers.CharField()
    category=serializers.CharField()
    ad_type=serializers.CharField()
    languages=serializers.CharField()
    office_country=serializers.CharField()
    office_state=serializers.CharField()
    office_district=serializers.CharField()
    gender=serializers.CharField()
    age_range=serializers.CharField()
    age_to=serializers.CharField()
    id_card = serializers.CharField()
    no_views=serializers.CharField()
    days_required=serializers.CharField()
    times_repeat=serializers.CharField()
    ad_details=serializers.CharField()
    other_ads=serializers.CharField()
    action_name=serializers.CharField()
    action_url=serializers.CharField()
    reason=serializers.CharField()
    status=serializers.CharField()
    ad_created_date=serializers.CharField()
    ad_created_time=serializers.CharField()
    coin=serializers.CharField()
    commission=serializers.CharField()

# /// Edit Ads Details//////
class edit_ads_Serializer(serializers.Serializer):
    # ad_id=serializers.CharField()
    ad_name=serializers.CharField()
    # ad_dis=serializers.CharField()
    category=serializers.CharField()
    ad_type=serializers.CharField()
    languages=serializers.CharField()
    office_country=serializers.CharField()
    office_state=serializers.CharField()
    office_district=serializers.CharField()
    gender=serializers.CharField()
    age_range=serializers.CharField()
    age_to=serializers.CharField()
    id_card = serializers.CharField()
    # no_views=serializers.CharField()
    days_required=serializers.CharField()
    times_repeat=serializers.CharField()
    ad_details=serializers.CharField()
    other_ads=serializers.CharField()
    action_name=serializers.CharField()
    action_url=serializers.CharField()
    # reason=serializers.CharField()
    status=serializers.CharField()

    def update(self,instance,data):
        instance.ad_name=data['ad_name']
        # instance.ad_pro=data['ad_pro']
        instance.category=data['category']
        instance.ad_type=data['ad_type']
        instance.languages=data['languages']
        instance.office_country=data['office_country']
        instance.office_state=data['office_state']
        instance.office_district=data['office_district']
        instance.gender=data['gender']
        instance.age_range=data['age_range']
        instance.age_to=data['age_to']
        instance.id_card=data['id_card']
        # instance.no_views=data['no_views']
        instance.days_required=data['days_required']
        instance.times_repeat=data['times_repeat']
        instance.ad_details=data['ad_details']
        instance.other_ads=data['other_ads']
        instance.action_name=data['action_name']
        instance.action_url=data['action_url']
        # instance.reason=data['reason']
        instance.status=data['status']
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

class update_status_serializer(serializers.Serializer):
    status = serializers.CharField()
    def update (self,instance,data):
        instance.status=data["status"]
        instance.save()
        return instance 
    
class status_active_serializer(serializers.Serializer):
    days_required = serializers.CharField()
    status = serializers.CharField()
    def update (self,instance,data):
        instance.days_required=data["days_required"]
        instance.status=data["status"]
        instance.save()
        return instance

class add_user_Serializer(serializers.Serializer):
    uid =  serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    mobile = serializers.CharField()
    access_Privileges = serializers.CharField()
    password = serializers.CharField()
    work = serializers.CharField()
    creator = serializers.CharField()
    # location = serializers.CharField()

    
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
            # location = data['location'],
        )
    
class edit_user_Serializer(serializers.Serializer):
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
    
class update_views_serializer(serializers.Serializer):
    no_views = serializers.CharField()
    def update (self,instance,data):
        instance.no_views = data['no_views']
        instance.save()
        return instance
    
class update_coin_serializer(serializers.Serializer):
    coin = serializers.CharField()
    commission = serializers.CharField()
    def update (self,instance,data):
        instance.coin = data['coin']
        instance.commission =  data['commission']
        instance.save()
        return instance