
from rest_framework import serializers
from apiapp.models import ProfileFinder,sender_list,received_list,block,favorite,happy_couples,saved_search


class ProfileFinderSerializer(serializers.Serializer):
    # User ID
    uid = serializers.CharField()

    # Signup
    email = serializers.EmailField()
    mobile = serializers.CharField()
    password = serializers.CharField()
    referral_code = serializers.CharField()
    otp = serializers.IntegerField()
    user_otp = serializers.IntegerField()
    
    created_date = serializers.CharField()


    # ID Card 1
    id_card_1 = serializers.CharField()

    # Basic Details
    name = serializers.CharField()
    address = serializers.CharField()
    height = serializers.IntegerField()
    weight = serializers.IntegerField()
    gender = serializers.CharField()
    marital = serializers.CharField()
    religion = serializers.CharField()
    physical = serializers.CharField()
    age = serializers.IntegerField()
    birth_place = serializers.CharField()
    birth_country = serializers.CharField()
    birth_time = serializers.TimeField()
    birth_city = serializers.CharField()
    origin = serializers.CharField()
    r_country = serializers.CharField()
    r_state = serializers.CharField()
    r_status = serializers.CharField()
    denomination = serializers.CharField()
    blood_group = serializers.CharField()

    # ID Card 2
    id_card_2 = serializers.CharField()

    # Parish / Temple / Mosque Details
    temple_name = serializers.CharField()
    temple_street = serializers.CharField()
    temple_post_code = serializers.CharField()
    temple_country = serializers.CharField()
    temple_city = serializers.CharField()
    temple_phone_number = serializers.CharField()
    temple_diocese = serializers.CharField()
    temple_local_admin = serializers.CharField()

    # Emergency Contact
    emergency_name = serializers.CharField()
    emergency_relation = serializers.CharField()
    emergency_phone_number = serializers.CharField()
    emergency_email = serializers.CharField()
    emergency_marital_status = serializers.CharField()
    emergency_occupations = serializers.CharField()

    # Profile Picture
    profile_picture = serializers.CharField()

    # Primary Details
    marital_status = serializers.CharField()
    physical_mental_status = serializers.CharField()
    primary_email = serializers.EmailField()
    primary_phone_number = serializers.CharField()
    dob = serializers.DateField()
    why_marry = serializers.CharField()
    behind_decision = serializers.CharField()

    # Education
    education_school = serializers.CharField()
    education_year = serializers.CharField()
    education_course = serializers.CharField()
    education_major = serializers.CharField()

    # Working
    are_you_working_now = serializers.CharField()
    company_name = serializers.CharField()
    position = serializers.CharField()
    profession = serializers.CharField()
    salary_range = serializers.CharField()

    # Intrest and Non Intrest
    your_intrest = serializers.CharField()
    non_intrest = serializers.CharField()

    # Complexion
    complexion = serializers.CharField()

    # Food Taste
    food_taste = serializers.CharField()

    # After Marriage
    daily_diet_plan = serializers.CharField()
    carriying_after_marriage = serializers.CharField()
    tobacco = serializers.CharField()
    alcohol = serializers.CharField()
    drugs = serializers.CharField()
    criminal_offence = serializers.CharField()

    # Primary Country
    primary_country = serializers.CharField()

    # Gallery
    selfie = serializers.CharField()
    full_size_image = serializers.CharField()
    family_image = serializers.CharField()
    gallery = serializers.CharField()
    horoscope = serializers.CharField()
    profile_tag = serializers.CharField()
    treet_mypartner = serializers.CharField()
    treet_their_side = serializers.CharField()

    # More Specific
    orphan = serializers.CharField()
    disable = serializers.CharField()
    whichorgan = serializers.CharField()

    # Family Details
    family_status = serializers.CharField()

    # Father Details
    father_name = serializers.CharField()
    father_country = serializers.CharField()
    father_city = serializers.CharField()
    father_job = serializers.CharField()
    father_family_name = serializers.CharField()

    # Mother Details
    mother_name = serializers.CharField()
    mother_country = serializers.CharField()
    mother_city = serializers.CharField()
    mother_job = serializers.CharField()
    mother_family_name = serializers.CharField()

    # Sibling 1 Details
    sibling_name = serializers.CharField()
    sibling_relation = serializers.CharField()
    sibling_young_or_old = serializers.CharField()
    sibling_occupation = serializers.CharField()
    sibling_marital = serializers.CharField()
    sibling_email = serializers.CharField()
    sibling_dob = serializers.CharField()
    sibling_job = serializers.CharField()

    # About Candidates
    about_candidate = serializers.CharField()
    current_status = serializers.CharField()

    # Contact Details
    contact_father_name = serializers.CharField()
    contact_father_street = serializers.CharField()
    contact_father_zipcode = serializers.CharField()
    contact_father_country = serializers.CharField()
    contact_father_city = serializers.CharField()
    contact_father_housename = serializers.CharField()
    contact_mother_housename = serializers.CharField()
    contact_email = serializers.CharField()
    contact_phone = serializers.CharField()

    # Social Media
    whatsapp = serializers.CharField()
    facebook = serializers.CharField()
    linkedin = serializers.CharField()
    instagram = serializers.CharField()
    youtube = serializers.CharField()
    twitter = serializers.CharField()
    website = serializers.CharField()

    #registered_date
    registered_date = serializers.DateField()
    
    #question and answer
    Questin = serializers.CharField()
    answer = serializers.CharField()
    
    #feedback and rating
    feedback = serializers.CharField()
    rating = serializers.CharField()



class SignupSerializer(serializers.Serializer):
    uid = serializers.CharField()
    email = serializers.EmailField()
    mobile = serializers.CharField()
    password = serializers.CharField()
    referral_code = serializers.CharField()
    otp = serializers.IntegerField()
    created_date = serializers.CharField()

    
    def create(self, data):
        return ProfileFinder.objects.create(
            uid = data['uid'],
            email = data['email'],
            mobile = data['mobile'],
            password = data['password'],
            referral_code = data['referral_code'],
            otp = data['otp'],
            created_date = data['created_date'],
        )


class OTPSerializer(serializers.Serializer):
    user_otp = serializers.IntegerField()

    def update(self, instance, data):
        instance.user_otp = data['user_otp']
        instance.save()
        return instance


class IDSerializer(serializers.Serializer):
    id_card_1 = serializers.CharField()

    def update(self, instance, data):
        instance.id_card_1 = data['id_card_1']
        instance.save()
        return instance


class BasicDetailsSerializer(serializers.Serializer):
    name = serializers.CharField()
    address = serializers.CharField()
    height = serializers.IntegerField()
    weight = serializers.IntegerField()
    gender = serializers.CharField()
    marital = serializers.CharField()
    age = serializers.IntegerField()
    physical = serializers.CharField()
    religion = serializers.CharField()
    birth_place = serializers.CharField()
    birth_country = serializers.CharField()
    birth_time = serializers.TimeField()
    birth_city = serializers.CharField()
    origin = serializers.CharField()
    r_country = serializers.CharField()
    r_state = serializers.CharField()
    r_status = serializers.CharField()
    denomination = serializers.CharField()
    blood_group = serializers.CharField()

    id_card_2 = serializers.CharField()

    temple_name = serializers.CharField()
    temple_street = serializers.CharField()
    temple_post_code = serializers.CharField()
    temple_country = serializers.CharField()
    temple_city = serializers.CharField()
    temple_phone_number = serializers.CharField()
    temple_diocese = serializers.CharField()
    temple_local_admin = serializers.CharField()

    emergency_name = serializers.CharField()
    emergency_relation = serializers.CharField()
    emergency_phone_number = serializers.CharField()
    emergency_email = serializers.CharField()
    emergency_marital_status = serializers.CharField()
    emergency_occupations = serializers.CharField()

    def update(self, instance, data):
        instance.name = data['name']
        instance.address = data['address']
        instance.height = data['height']
        instance.weight = data['weight']
        instance.gender = data['gender']
        instance.marital = data['marital']
        instance.physical = data['physical']
        instance.age = data['age']
        instance.religion = data['religion']
        instance.birth_place = data['birth_place']
        instance.birth_country = data['birth_country']
        instance.birth_time = data['birth_time']
        instance.birth_city = data['birth_city']
        instance.origin = data['origin']
        instance.r_country = data['r_country']
        instance.r_state = data['r_state']
        instance.r_status = data['r_status']
        instance.denomination = data['denomination']
        instance.blood_group = data['blood_group']
        instance.id_card_2 = data['id_card_2']
        instance.temple_name = data['temple_name']
        instance.temple_street = data['temple_street']
        instance.temple_post_code = data['temple_post_code']
        instance.temple_country = data['temple_country']
        instance.temple_city = data['temple_city']
        instance.temple_phone_number = data['temple_phone_number']
        instance.temple_diocese = data['temple_diocese']
        instance.temple_local_admin = data['temple_local_admin']
        instance.emergency_name = data['emergency_name']
        instance.emergency_relation = data['emergency_relation']
        instance.emergency_phone_number = data['emergency_phone_number']
        instance.emergency_email = data['emergency_email']
        instance.emergency_marital_status = data['emergency_marital_status']
        instance.emergency_occupations = data['emergency_occupations']
        instance.save()
        return instance


class ProfilePictureSerializer(serializers.Serializer):
    profile_picture = serializers.CharField()

    def update(self, instance, data):
        instance.profile_picture = data['profile_picture']
        instance.save()
        return instance


class PrimaryDetailsSerializer(serializers.Serializer):
    marital_status = serializers.CharField()
    physical_mental_status = serializers.CharField()
    primary_email = serializers.EmailField()
    primary_phone_number = serializers.CharField()
    dob = serializers.DateField()
    why_marry = serializers.CharField()
    behind_decision = serializers.CharField()
    education_school = serializers.CharField()
    education_year = serializers.CharField()
    education_course = serializers.CharField()
    education_major = serializers.CharField()
    are_you_working_now = serializers.CharField()
    company_name = serializers.CharField()
    position = serializers.CharField()
    profession = serializers.CharField()
    salary_range = serializers.CharField()
    your_intrest = serializers.CharField()
    non_intrest = serializers.CharField()
    complexion = serializers.CharField()
    food_taste = serializers.CharField()
    daily_diet_plan = serializers.CharField()
    carriying_after_marriage = serializers.CharField()
    tobacco = serializers.CharField()
    alcohol = serializers.CharField()
    drugs = serializers.CharField()
    criminal_offence = serializers.CharField()
    primary_country = serializers.CharField()
    selfie = serializers.CharField()
    full_size_image = serializers.CharField()
    family_image = serializers.CharField()
    gallery = serializers.CharField()
    horoscope = serializers.CharField()
    profile_tag = serializers.CharField()
    treet_mypartner = serializers.CharField()
    treet_their_side = serializers.CharField()
    orphan = serializers.CharField()
    disable = serializers.CharField()
    whichorgan = serializers.CharField()

    def update(self, instance, data):
        instance.marital_status = data['marital_status']
        instance.physical_mental_status = data['physical_mental_status']
        instance.primary_email = data['primary_email']
        instance.primary_phone_number = data['primary_phone_number']
        instance.dob = data['dob']
        instance.why_marry = data['why_marry']
        instance.behind_decision = data['behind_decision']
        instance.education_school = data['education_school']
        instance.education_year = data['education_year']
        instance.education_course = data['education_course']
        instance.education_major = data['education_major']
        instance.are_you_working_now = data['are_you_working_now']
        instance.company_name = data['company_name']
        instance.position = data['position']
        instance.profession = data['profession']
        instance.salary_range = data['salary_range']
        instance.your_intrest = data['your_intrest']
        instance.non_intrest = data['non_intrest']
        instance.complexion = data['complexion']
        instance.food_taste = data['food_taste']
        instance.daily_diet_plan = data['daily_diet_plan']
        instance.carriying_after_marriage = data['carriying_after_marriage']
        instance.tobacco = data['tobacco']
        instance.alcohol = data['alcohol']
        instance.drugs = data['drugs']
        instance.criminal_offence = data['criminal_offence']
        instance.primary_country = data['primary_country']
        instance.selfie = data['selfie']
        instance.full_size_image = data['full_size_image']
        instance.family_image = data['family_image']
        instance.gallery = data['gallery']
        instance.horoscope = data['horoscope']
        instance.profile_tag = data['profile_tag']
        instance.treet_mypartner = data['treet_mypartner']
        instance.treet_their_side = data['treet_their_side']
        instance.orphan = data['orphan']
        instance.disable = data['disable']
        instance.whichorgan = data['whichorgan']
        instance.save()
        return instance


class FamilyDetailsSerializer(serializers.Serializer):
    family_status = serializers.CharField()
    father_name = serializers.CharField()
    father_country = serializers.CharField()
    father_city = serializers.CharField()
    father_job = serializers.CharField()
    father_family_name = serializers.CharField()
    mother_name = serializers.CharField()
    mother_country = serializers.CharField()
    mother_city = serializers.CharField()
    mother_job = serializers.CharField()
    mother_family_name = serializers.CharField()
    sibling_name = serializers.CharField()
    sibling_relation = serializers.CharField()
    sibling_young_or_old = serializers.CharField()
    sibling_occupation = serializers.CharField()
    sibling_marital = serializers.CharField()
    sibling_email = serializers.CharField()
    sibling_dob = serializers.CharField()
    sibling_job = serializers.CharField()
    about_candidate = serializers.CharField()
    current_status = serializers.CharField()

    def update(self, instance, data):
        instance.family_status = data['family_status']
        instance.father_name = data['father_name']
        instance.father_country = data['father_country']
        instance.father_city = data['father_city']
        instance.father_job = data['father_job']
        instance.father_family_name = data['father_family_name']
        instance.mother_name = data['mother_name']
        instance.mother_country = data['mother_country']
        instance.mother_city = data['mother_city']
        instance.mother_job = data['mother_job']
        instance.mother_family_name = data['mother_family_name']
        instance.sibling_name = data['sibling_name']
        instance.sibling_relation = data['sibling_relation']
        instance.sibling_young_or_old = data['sibling_young_or_old']
        instance.sibling_occupation = data['sibling_occupation']
        instance.sibling_marital = data['sibling_marital']
        instance.sibling_email = data['sibling_email']
        instance.sibling_dob = data['sibling_dob']
        instance.sibling_job = data['sibling_job']
        instance.about_candidate = data['about_candidate']
        instance.current_status = data['current_status']
        instance.save()
        return instance


class ContactDetailsSerializer(serializers.Serializer):
    contact_father_name = serializers.CharField()
    contact_father_street = serializers.CharField()
    contact_father_zipcode = serializers.CharField()
    contact_father_country = serializers.CharField()
    contact_father_city = serializers.CharField()
    contact_father_housename = serializers.CharField()
    contact_mother_housename = serializers.CharField()
    contact_email = serializers.CharField()
    contact_phone = serializers.CharField()
    whatsapp = serializers.CharField()
    facebook = serializers.CharField()
    linkedin = serializers.CharField()
    instagram = serializers.CharField()
    youtube = serializers.CharField()
    twitter = serializers.CharField()
    website = serializers.CharField()

    def update(self, instance, data):
        instance.contact_father_name = data['contact_father_name']
        instance.contact_father_street = data['contact_father_street']
        instance.contact_father_zipcode = data['contact_father_zipcode']
        instance.contact_father_country = data['contact_father_country']
        instance.contact_father_city = data['contact_father_city']
        instance.contact_father_housename = data['contact_father_housename']
        instance.contact_mother_housename = data['contact_mother_housename']
        instance.contact_email = data['contact_email']
        instance.contact_phone = data['contact_phone']
        instance.whatsapp = data['whatsapp']
        instance.facebook = data['facebook']
        instance.linkedin = data['linkedin']
        instance.instagram = data['instagram']
        instance.youtube = data['youtube']
        instance.twitter = data['twitter']
        instance.website = data['website']
        instance.save()
        return instance

class profileupdateSerializer(serializers.Serializer):
    selfie = serializers.CharField()
    def update(self, instance, data):
        instance.selfie = data['selfie']
        return instance

class SenderSerializer(serializers.Serializer):
    sender_uid = serializers.CharField()
    received_uid = serializers.CharField()
    request_phone_number = serializers.CharField()
    request_whatsapp_number = serializers.CharField()
    request_address = serializers.CharField()
    request_horoscope = serializers.CharField()
    request_social_media_link = serializers.CharField()
    action = serializers.CharField()

class sender_list_Serializer(serializers.Serializer):
    sender_uid = serializers.CharField()
   

    def create(self, data):
        return sender_list.objects.create(
        sender_uid = data['sender_uid'],
        
        )

class sender_request_Serializer(serializers.Serializer):
    received_uid = serializers.CharField()
    request_phone_number = serializers.CharField()
    request_whatsapp_number = serializers.CharField()
    request_address = serializers.CharField()
    request_horoscope = serializers.CharField()
    request_social_media_link = serializers.CharField()
    action = serializers.CharField()
    def update(self, instance, data):
        instance.received_uid = data['received_uid']
        instance.request_phone_number = data['request_phone_number']
        instance.request_whatsapp_number = data['request_whatsapp_number']
        instance.request_address = data['request_address']
        instance.request_horoscope = data['request_horoscope']
        instance.request_social_media_link = data['request_social_media_link']  
        instance.action = data['action']  
        instance.save()    
        return instance
    
class ReceivedSerializer(serializers.Serializer):
    received_uid = serializers.CharField()
    sender_uid = serializers.CharField()
    request_phone_number = serializers.CharField()
    request_whatsapp_number = serializers.CharField()
    request_address = serializers.CharField()
    request_horoscope = serializers.CharField()
    request_social_media_link = serializers.CharField()
    action = serializers.CharField()
    
class received_list_Serializer(serializers.Serializer):
    received_uid = serializers.CharField()


    def create(self, data):
        return received_list.objects.create(
        received_uid = data['received_uid'],
        )

class received_request_Serializer(serializers.Serializer):
    sender_uid = serializers.CharField()
    request_phone_number = serializers.CharField()
    request_whatsapp_number = serializers.CharField()
    request_address = serializers.CharField()
    request_horoscope = serializers.CharField()
    request_social_media_link = serializers.CharField()
    action = serializers.CharField()
    def update(self, instance, data):
        instance.sender_uid = data['sender_uid']
        instance.request_phone_number = data['request_phone_number']
        instance.request_whatsapp_number = data['request_whatsapp_number']
        instance.request_address = data['request_address']
        instance.request_horoscope = data['request_horoscope']
        instance.request_social_media_link = data['request_social_media_link']
        instance.action = data['action']
        instance.save()    
        return instance

class BlockSerializer(serializers.Serializer):
    who_blocked_id = serializers.CharField()
    blocked_id = serializers.CharField()
    reason = serializers.CharField()

class blocked_list_Serializer(serializers.Serializer):
    who_blocked_id = serializers.CharField()
   

    def create(self, data):
        return block.objects.create(
        who_blocked_id = data['who_blocked_id'],
        
        )
    
class blocked_Serializer(serializers.Serializer):
    who_blocked_id = serializers.CharField()
    blocked_id = serializers.CharField()
    reason = serializers.CharField()
    def update(self, instance, data):
        instance.who_blocked_id = data['who_blocked_id']
        instance.blocked_id = data['blocked_id']
        instance.reason = data['reason']
        instance.save()    
        return instance

class blocked_me_Serializer(serializers.Serializer):
    who_blocked_id = serializers.CharField()
    who_blocked_me = serializers.CharField()
    def update(self, instance, data):
        instance.who_blocked_id = data['who_blocked_id']
        instance.who_blocked_me = data['who_blocked_me']
        instance.save()    
        return instance
    
#favorite
class favoriteSerializer(serializers.Serializer):
    my_id = serializers.CharField()
    myfavorite_id = serializers.CharField()
    who_favorite_me_id = serializers.CharField()

class favorite_list_Serializer(serializers.Serializer):
    my_id = serializers.CharField()
   

    def create(self, data):
        return favorite.objects.create(
        my_id = data['my_id'],
        
        )
    
class favorite_Serializer(serializers.Serializer):
    my_id = serializers.CharField()
    myfavorite_id = serializers.CharField()
    def update(self, instance, data):
        instance.my_id = data['my_id']
        instance.myfavorite_id = data['myfavorite_id']
        instance.save()    
        return instance

class favorite_me_Serializer(serializers.Serializer):
    my_id = serializers.CharField()
    who_favorite_me_id = serializers.CharField()
    def update(self, instance, data):
        instance.my_id = data['my_id']
        instance.who_favorite_me_id = data['who_favorite_me_id']
        instance.save()    
        return instance
    
#Happy couples
class happy_couple_Serializer(serializers.Serializer):
    groom_name = serializers.CharField()
    groom_id = serializers.CharField()
    bride_name = serializers.CharField()
    bride_id = serializers.CharField()
    date_of_marriage = serializers.CharField()
    worde_about_marriyo = serializers.CharField()
    image_videous = serializers.CharField()

class happy_list_Serializer(serializers.Serializer):
    groom_name = serializers.CharField()
    groom_id = serializers.CharField()
    bride_name = serializers.CharField()
    bride_id = serializers.CharField()
    date_of_marriage = serializers.CharField()
    worde_about_marriyo = serializers.CharField()
    image_videous = serializers.CharField()   

    def create(self, data):
        return happy_couples.objects.create(
    groom_name = data['groom_name'],
    groom_id = data['groom_id'],
    bride_name = data['bride_name'],
    bride_id = data['bride_id'],
    date_of_marriage = data['date_of_marriage'],
    worde_about_marriyo = data['worde_about_marriyo'],
    image_videous = data['image_videous'],  
        
        )
#saved search
class saved_list_Serializer(serializers.Serializer):
    my_id = serializers.CharField()
    tag = serializers.CharField()
    country = serializers.CharField()
    city = serializers.CharField()
    age = serializers.IntegerField()
    complexion =serializers.CharField()
    gender = serializers.CharField()
    denomination = serializers.CharField()   
    filterd_data = serializers.CharField()  

    def create(self, data):
        return saved_search.objects.create(
        my_id = data['my_id'],
         tag = data['tag'],
          country = data['country'],
           city = data['city'],
            age = data['age'],
             complexion = data['complexion'],
              gender = data['gender'],
               denomination = data['denomination'],
               filterd_data = data['filterd_data'],
        
        )
    
class saved_Serializer(serializers.Serializer):
    my_id = serializers.CharField()
    tag = serializers.CharField()
    country = serializers.CharField()
    city = serializers.CharField()
    age = serializers.IntegerField()
    complexion =serializers.CharField()
    gender = serializers.CharField()
    denomination = serializers.CharField()
    filterd_data = serializers.CharField()  

    def update(self, instance, data):
        instance.my_id = data['my_id']
        instance.tag = data['tag']
        instance.country = data['country']
        instance.city = data['city']
        instance.age = data['age']
        instance.complexion = data['complexion']
        instance.gender = data['gender']
        instance.denomination = data['denomination']
        filterd_data = data['filterd_data'],
        instance.save()    
        return instance
    
class my_investigator_serializer(serializers.Serializer):
    # my_client = serializers.CharField(source=ProfileFinder, read_only=True)
    my_investigator = serializers.CharField()
    rating = serializers.CharField()
    feedback = serializers.CharField()
    Questin = serializers.CharField()
    answer =serializers.CharField()

    def update(self, instance, data):
        instance.my_investigator = data['my_investigator']
        instance.rating = data['rating']
        instance.feedback = data['feedback']
        instance.Questin = data['Questin']
        instance.answer = data['answer']
        instance.save()
        return instance

class my_question_and_answer(serializers.Serializer):
    # my_client = serializers.CharField(source=ProfileFinder, read_only=True)
    Questin = serializers.CharField()
    answer =serializers.CharField()
    def update(self, instance, data):
        instance.Questin = data['Questin']
        instance.answer = data['answer']
        instance.save()
        return instance
    
class feedback_and_rating(serializers.Serializer):
    # my_client = serializers.CharField(source=ProfileFinder, read_only=True)
    feedback = serializers.CharField()
    rating =serializers.CharField()
    def update(self, instance, data):
        instance.feedback = data['feedback']
        instance.rating = data['rating']
        instance.save()
        return instance
    
class my_manager_serializer(serializers.Serializer):
    my_manager = serializers.CharField()
    complaints = serializers.CharField()
    complaints_replay = serializers.CharField()

    def update(self, instance, data):
        instance.my_manager = data['my_manager']
        instance.complaints = data['complaints']
        instance.complaints_replay = data['complaints_replay']
        instance.save()
        return instance

class complaints_and_complaints_replay(serializers.Serializer):
    # my_client = serializers.CharField(source=ProfileFinder, read_only=True)
    complaints = serializers.CharField()
    complaints_replay =serializers.CharField()
    def update(self, instance, data):
        instance.complaints = data['complaints']
        instance.complaints_replay = data['complaints_replay']
        instance.save()
        return instance
