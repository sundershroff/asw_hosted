from django.shortcuts import render
from django.http import HttpResponse,JsonResponse

from apiapp import serializer,pi_serializer
from apiapp import models
from apiapp.models import ProfileFinder,sender_list,received_list,saved_search,private_investigator
# Create your views here.

from rest_framework.decorators import api_view,renderer_classes,permission_classes
from rest_framework.response import Response
from rest_framework import status,generics
from apiapp import extension


from django.core.files.storage import FileSystemStorage
from django.db.models import Q
import requests
import json
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated,AllowAny

import datetime


all_image_url = "http://127.0.0.1:3000/"
@api_view(['POST'])
def signup(request):
    try:
        try:
            if extension.validate_email(request.data['email']):
                return Response("User Already Exists", status=status.HTTP_302_FOUND)
            else:
                x = datetime.datetime.now()
                code = ""
                if str(request.data['referral_code']) == "":
                    code = "Empty"
                else:
                    code = request.data['referral_code']
                datas = {
                    'email': request.data["email"],
                    'mobile': request.data["mobile"],
                    'password': request.data["password"],
                    'referral_code': code,
                    'uid': extension.id_generate(),
                    'otp': extension.otp_generate(),
                    'created_date':str(x.strftime("%d"))+" "+str(x.strftime("%B"))+","+str(x.year)
                }
                dataserializer = serializer.SignupSerializer(data=datas)
                print(datas['uid'])
                received ={'received_uid':datas['uid']}
                sender ={'sender_uid':datas['uid']}
                blocked ={'who_blocked_id':datas['uid']}
                favorite ={'my_id':datas['uid']}
                saved ={'my_id':datas['uid']}
                received_list= serializer.received_list_Serializer(data=received)
                sender_list= serializer.sender_list_Serializer(data=sender)
                blocked_list= serializer.blocked_list_Serializer(data=blocked)
                favorite_list= serializer.favorite_list_Serializer(data=favorite)
                saved_list= serializer.saved_list_Serializer(data=saved)
                if dataserializer.is_valid() and received_list.is_valid() and sender_list.is_valid() and blocked_list.is_valid() and favorite_list.is_valid():
                    dataserializer.save()
                    received_list.save()
                    sender_list.save()
                    blocked_list.save()
                    favorite_list.save()
                    print("Valid Data")
                    extension.send_mail(datas['email'], datas['otp'])
                    print("Email send")
                    return Response(datas['uid'], status=status.HTTP_200_OK)
                else:
                    return Response({"Bad Request"}, status=status.HTTP_403_FORBIDDEN)
        except:
            return Response({"Invalid Json Format (OR) Invalid Key"}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({"Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def otp(request, id):
    try:
        try:
            if extension.validate_otp(id, int(request.data['user_otp'])):
                try:
                    userSpecificData = models.ProfileFinder.objects.get(uid=id)
                    serializer_validate = serializer.OTPSerializer(
                        instance=userSpecificData, data=request.POST, partial=True)
                    if serializer_validate.is_valid():
                        serializer_validate.save()
                        print("Valid OTP")
                        return Response(id, status=status.HTTP_200_OK)
                    else:
                        return Response({"Cannot Verify OTP"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                except:
                    return Response({"serializer Issue"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response({"Wrong OTP"}, status=status.HTTP_403_FORBIDDEN)
        except:
            return Response({"Invalid Json Format (OR) Invalid Key"}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({"Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def signin(request):
    try:
        try:
            if extension.validate_email(request.data['email']):
                if extension.verify_user(request.data['email'], request.data['password']):
                    if extension.verify_user_otp(request.data['email']):
                        return Response(extension.get_user_id(request.data['email']), status=status.HTTP_200_OK)
                    else:
                        return Response({"Didn't Completed OTP Verification"}, status=status.HTTP_401_UNAUTHORIZED)
                else:
                    return Response({"Password Is Incorrect"}, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({"User Dosn't Exits"}, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response({"Invalid Json Format (OR) Invalid Key"}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({"Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def profileIdCard(request, uid):
    try:
        try:
            userdata = models.ProfileFinder.objects.get(uid=uid)
        except:
            return Response({"Accound Not Found"}, statusu=status.HTTP_404_NOT_FOUND)
        print(request.FILES)
        id_card = str(request.FILES['id_card_1']).replace(" ", "_")
        fs = FileSystemStorage()
        path = fs.save(f"{uid}/id_card/"+id_card, request.FILES['id_card_1'])
        # full_path = "http://54.159.186.219:8000"+fs.url(path)
        full_path = all_image_url+fs.url(path)
        data = {
            "id_card_1": full_path
        }
        print(data)
        idserializer = serializer.IDSerializer(
            instance=userdata, data=data, partial=True)
        if idserializer.is_valid():
            idserializer.save()
            print(data['id_card_1'])
            return Response(uid, status=status.HTTP_200_OK)
        else:
            return Response({})
    except:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# def profileForwho(request, id):
#     return render(request, 'profileforwho.html', context={"uid": id})


@api_view(['POST'])
def profileForm(request, id):
    try:
        fs = FileSystemStorage()
        userdata = serializer.ProfileFinder.objects.get(uid=id)
        id_card = str(request.FILES['id_card_2']).replace(" ", "_")
        path = fs.save(f"{id}/id_card/"+id_card, request.FILES['id_card_2'])

        # full_path = "http://54.159.186.219:8000"+fs.url(path)
        full_path = all_image_url+fs.url(path)

        data = {
            'name': request.POST['name'],
            'address': request.POST['address'],
            'height': request.POST['height'],
            'weight': request.POST['weight'],
            'gender': request.POST['gender'],
            'marital': request.POST['marital'],
            'physical': request.POST['physical'],
            'religion': request.POST['religion'],
            'age': request.POST['age'],
            'birth_place': request.POST['birth_place'],
            'birth_country': request.POST['birth_country'],
            'birth_time': request.POST['birth_time'],
            'birth_city': request.POST['birth_city'],
            'origin': request.POST['origin'],
            'r_country': request.POST['r_country'],
            'r_state': request.POST['r_state'],
            'r_status': request.POST['r_status'],
            'denomination': request.POST['denomination'],
            'blood_group': request.POST['blood_group'],
            'id_card_2': full_path,
            'temple_name': request.POST['temple_name'],
            'temple_street': request.POST['temple_street'],
            'temple_post_code': request.POST['temple_post_code'],
            'temple_country': request.POST['temple_country'],
            'temple_city': request.POST['temple_city'],
            'temple_phone_number': request.POST['temple_phone_number'],
            'temple_diocese': request.POST['temple_diocese'],
            'temple_local_admin': request.POST['temple_local_admin'],
            'emergency_name': str(request.POST.getlist('emergency_name')),
            'emergency_relation': str(request.POST.getlist('emergency_relation')),
            'emergency_phone_number': str(request.POST.getlist('emergency_phone_number')),
            'emergency_email': str(request.POST.getlist('emergency_email')),
            'emergency_marital_status': str(request.POST.getlist('emergency_marital_status')),
            'emergency_occupations': str(request.POST.getlist('emergency_occupations')),
        }

        print(data)
        basicdetailsserializer = serializer.BasicDetailsSerializer(
            instance=userdata, data=data, partial=True)
        if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
        else:
            return Response({"sserializer issue"}, status=status.HTTP_403_FORBIDDEN)
    except:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def profilePicture(request, id):
    try:
        userdata = serializer.ProfileFinder.objects.get(uid=id)

        id_card = str(request.FILES['profile_picture']).replace(" ", "_")

        fs = FileSystemStorage()
        path = fs.save(f"{id}/id_card/"+id_card,
        request.FILES['profile_picture'])
        # full_path = "http://54.159.186.219:8000"+fs.url(path)
        full_path = all_image_url+fs.url(path)
        data = {
            "profile_picture": full_path
        }
        profilepictureserializer = serializer.ProfilePictureSerializer(
            instance=userdata, data=data, partial=True)
        if profilepictureserializer.is_valid():
            profilepictureserializer.save()
            # print(full_path)
            return Response(id, status=status.HTTP_200_OK)
    except:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def primaryDetails(request, id):
    try:
        image_names = []
        image_list = []
        gallery_web = []
        web_multi_image = request.FILES
        web_multi_imagekey = str(web_multi_image.keys())
        # web_multi_image.pop("selfie")
        print(web_multi_image)
        for x in web_multi_image.keys():
            gallery_web.append(web_multi_image[x])
        print(gallery_web)
        a = gallery_web[4:]
        for y in a:
            print((y))
       
        # request.FILES.getlist('gallery')
        # print(request.FILES.getlist('gallery'))
        userdata = serializer.ProfileFinder.objects.get(uid=id)
        fs = FileSystemStorage()
        
        if "file_0" in web_multi_imagekey:
            for i in a:
                image_names.append(str(i).replace(" ","_"))
            print(image_names)
            for qq in range(0,1):
               for iname in range(0,len(image_names)):
                   gallery_path = fs.save(
                   f"{id}/images/gallery/"+image_names[iname], request.FILES[f'file_{iname}'])
                #    image_list.append("http://54.159.186.219:8000"+fs.url(gallery_path))
                   image_list.append(all_image_url+fs.url(gallery_path))
        
        else:   
            for sav in request.FILES.getlist('gallery'):
                sa = fs.save(
                    f"{id}/images/gallery/"+sav.name, sav)
                image_names.append(str(sa).replace(" ","_"))
            # for i in request.FILES.getlist('gallery'):
            #     image_names.append(str(i).replace(" ","_"))
            print(image_names)
            for iname in image_names:
                # gallery_path = fs.save(
                #     f"{id}/images/gallery/"+iname, request.FILES['gallery'])
                gallery_path = iname
                # image_list.append("http://54.159.186.219:8000"+fs.url(gallery_path))
                image_list.append(all_image_url+fs.url(gallery_path))
            
    


        selfie = str(request.FILES['selfie']).replace(" ", "_")
        full_size_image = str(
            request.FILES['full_size_image']).replace(" ", "_")
        family_image = str(request.FILES['family_image']).replace(" ", "_")
        # gallery = str(request.FILES['gallery']).replace(" ", "_")
        # for i in request.FILES.getlist('gallery'):
        #     image_names.append(str(i).replace(" ","_"))
        # print(image_names)
        horoscope = str(request.FILES['horoscope']).replace(" ", "_")
        selfie_path = fs.save(f"{id}/images/selfie/" +
        selfie, request.FILES['selfie'])
        full_size_image_path = fs.save(
            f"{id}/images/full_size_image/"+full_size_image, request.FILES['full_size_image'])
        family_image_path = fs.save(
            f"{id}/images/family_image/"+family_image, request.FILES['family_image'])
        
        
        horoscope_path = fs.save(
            f"{id}/images/horoscope/"+horoscope, request.FILES['horoscope'])

        # selfie = "http://54.159.186.219:8000"+fs.url(selfie_path)
        selfie = all_image_url+fs.url(selfie_path)
        # full_size_image = "http://54.159.186.219:8000" + \
        #     fs.url(full_size_image_path)
        full_size_image = all_image_url + \
            fs.url(full_size_image_path)
        # family_image = "http://54.159.186.219:8000"+fs.url(family_image_path)
        family_image = all_image_url+fs.url(family_image_path)

        # horoscope = "http://54.159.186.219:8000"+fs.url(horoscope_path)
        horoscope = all_image_url+fs.url(horoscope_path)
       
        gallery = str(image_list)
        data = {
            'marital_status': request.POST['marital_status'],
            'physical_mental_status': request.POST['physical_mental_status'],
            'primary_email': request.POST['primary_email'],
            'primary_phone_number': str(request.POST['primary_phone_number']),
            'dob': request.POST['dob'],
            'why_marry': request.POST['why_marry'],
            'behind_decision': request.POST['behind_decision'],
            'education_school': str(request.POST.getlist('education_school')),
            'education_year': str(request.POST.getlist('education_year')),
            'education_course': str(request.POST.getlist('education_course')),
            'education_major': str(request.POST.getlist('education_major')),
            'are_you_working_now': str(request.POST.getlist('are_you_working_now')),
            'company_name': str(request.POST.getlist('company_name')),
            'position': str(request.POST.getlist('position')),
            'profession': str(request.POST.getlist('profession')),
            'salary_range': str(request.POST.getlist('salary_range')),
            'your_intrest': str(request.POST.getlist('your_intrest')),
            'non_intrest': str(request.POST.getlist('non_intrest')),
            'complexion': str(request.POST.getlist('complexion')),
            'food_taste': str(request.POST.getlist('food_taste')),
            'daily_diet_plan': str(request.POST.getlist('daily_diet_plan')),
            'carriying_after_marriage': request.POST['carriying_after_marriage'],
            'tobacco': request.POST['tobacco'],
            'alcohol': request.POST['alcohol'],
            'drugs': request.POST['drugs'],
            'criminal_offence': request.POST['criminal_offence'],
            'primary_country': request.POST['primary_country'],
            'selfie': selfie,
            'full_size_image': full_size_image,
            'family_image': family_image,
            'gallery': gallery, 
            'horoscope': horoscope,
            'profile_tag': request.POST['profile_tag'],
            'treet_mypartner': request.POST['treet_mypartner'],
            'treet_their_side': request.POST['treet_their_side'],
            'orphan': request.POST['orphan'],
            'disable': request.POST['disable'],
            'whichorgan': request.POST['whichorgan'],
        }
        print(data["gallery"])
        # print(data)
        primarydetailsserializer = serializer.PrimaryDetailsSerializer(
            instance=userdata, data=data, partial=True)
        # print(primarydetailsserializer)
        if primarydetailsserializer.is_valid():
            primarydetailsserializer.save()
            print("valid data")
            return Response(id, status=status.HTTP_200_OK)
            
        else:
            return Response({"Something Went Wrong"}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def familyDetails(request, id):
    try:
        userdata = serializer.ProfileFinder.objects.get(uid=id)
        data = {
            'family_status': request.POST['family_status'],
            'father_name': request.POST['father_name'],
            'father_country': request.POST['father_country'],
            'father_city': request.POST['father_city'],
            'father_job': request.POST['father_job'],
            'father_family_name' : request.POST['father_family_name'],
            'mother_name': request.POST['mother_name'],
            'mother_country': request.POST['mother_country'],
            'mother_city': request.POST['mother_city'],
            'mother_job': request.POST['mother_job'],
            'mother_family_name': request.POST['mother_family_name'],
            'sibling_name': str(request.POST.getlist('sibling_name')),
            'sibling_relation': str(request.POST.getlist('sibling_relation')),
            'sibling_young_or_old': str(request.POST.getlist('sibling_young_or_old')),
            'sibling_occupation': str(request.POST.getlist('sibling_occupation')),
            'sibling_marital': str(request.POST.getlist('sibling_marital')),
            'sibling_email': str(request.POST.getlist('sibling_email')),
            'sibling_job': str(request.POST.getlist('sibling_job')),
            'sibling_dob': str(request.POST.getlist('sibling_dob')),
            'about_candidate': request.POST['about_candidate'],
            'current_status': request.POST['current_status'],
        }
        print(data)
        familydetailsserializer = serializer.FamilyDetailsSerializer(
            instance=userdata, data=data, partial=True)
        if familydetailsserializer.is_valid():
            familydetailsserializer.save()
            print("valid data")
            return Response(id, status=status.HTTP_200_OK)
        return Response({"somthing wrong"}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def contactDetails(request, id):
    try:
        print(request.POST)
        userdata = serializer.ProfileFinder.objects.get(uid=id)
        # print("Stop")
        data = {
            'contact_father_name': request.POST['contact_father_name'],
            'contact_father_street': request.POST['contact_father_street'],
            'contact_father_zipcode': request.POST['contact_father_zipcode'],
            'contact_father_country': request.POST['contact_father_country'],
            'contact_father_city': request.POST['contact_father_city'],
            'contact_father_housename': request.POST['contact_father_housename'],
            'contact_mother_housename': request.POST['contact_mother_housename'],
            'contact_email': request.POST['contact_email'],
            'contact_phone': request.POST['contact_phone'],
            'whatsapp': request.POST['whatsapp'],
            'facebook': request.POST['facebook'],
            'linkedin': request.POST['linkedin'],
            'instagram': request.POST['instagram'],
            'youtube': request.POST['youtube'],
            'twitter': request.POST['twitter'],
            'website': request.POST['website'],
        }
        # print(data)
        contactdetailsserializer = serializer.ContactDetailsSerializer(
            instance=userdata, data=data, partial=True)
        if contactdetailsserializer.is_valid():
        
            contactdetailsserializer.save()
            print(data)
            return Response(id, status=status.HTTP_200_OK)
    except:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def getAllUserData(request, id):
    try:
        allData = serializer.ProfileFinder.objects.get(uid=id)
        alldataserializer = serializer.ProfileFinderSerializer(allData)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)
    except:
        return Response({"Invalid User"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def about_candidate(request, id):
    try:
        userdata = serializer.ProfileFinder.objects.get(uid=id)
        mydata = ProfileFinder.objects.filter(uid = id).values()
        for my in mydata:
            print(my['uid'])
#sibling details
        sibling_name_value=[]
        sibling_relation_value=[]
        sibling_occupation_value=[]
        sibling_name = my['sibling_name'][1:-1].split(", ")
        sibling_relation = my['sibling_relation'][1:-1].split(", ")
        sibling_occupation = my['sibling_occupation'][1:-1].split(", ")
        for sibling_name_x in sibling_name:
            sibling_name_value.append(sibling_name_x[1:-1])
        for sibling_relation_x in sibling_relation:
            sibling_relation_value.append(sibling_relation_x[1:-1])
        for sibling_occupation_x in sibling_occupation:
            sibling_occupation_value.append(sibling_occupation_x[1:-1])
        sibling={}
        sib = [sibling]
        for i, sibling_name_data in enumerate(sibling_name_value):
                sibling[f'sibling_name_{i}'] = sibling_name_data
        for i, sibling_relation_data in enumerate(sibling_relation_value):
                sibling[f'sibling_relation_{i}'] = sibling_relation_data
        for i, sibling_occupation_data in enumerate(sibling_occupation_value):
                sibling[f'sibling_occupation_{i}'] = sibling_occupation_data
        print(sibling)

#education details
        education_school_value=[]
        education_year_value=[]
        education_course_value=[]
        education_school = my['education_school'][1:-1].split(", ")
        education_year = my['education_year'][1:-1].split(", ")
        education_course = my['education_course'][1:-1].split(", ")
        for education_school_x in education_school:
            education_school_value.append(education_school_x[1:-1])
        for education_year_x in education_year:
            education_year_value.append(education_year_x[1:-1])
        for education_course_x in education_course:
            education_course_value.append(education_course_x[1:-1])
        education={}
        edu = [education]
        for i, education_school_data in enumerate(education_school_value):
                education[f'education_school_{i}'] = education_school_data
        for i, education_year_data in enumerate(education_year_value):
                education[f'education_year_{i}'] = education_year_data
        for i, education_course_data in enumerate(education_course_value):
                education[f'education_course_{i}'] = education_course_data
        print(education)
 #working details
        company_name_value=[]
        position_value=[]
        salary_range_value=[]
        profession_value = []
        company_name = my['company_name'][1:-1].split(", ")
        position = my['position'][1:-1].split(", ")
        salary_range = my['salary_range'][1:-1].split(", ")
        profession = my['profession'][1:-1].split(", ")
        for company_name_x in company_name:
            company_name_value.append(company_name_x[1:-1])
        for position_x in position:
            position_value.append(position_x[1:-1])
        for salary_range_x in salary_range:
            salary_range_value.append(salary_range_x[1:-1])
        for profession_x in profession:
            profession_value.append(profession_x[1:-1])
        working={}
        wor = [working]
        for i, company_name_data in enumerate(company_name_value):
                working[f'company_name_{i}'] = company_name_data
        for i, position_data in enumerate(position_value):
                working[f'position_{i}'] = position_data
        for i, salary_range_data in enumerate(salary_range_value):
                working[f'salary_range_{i}'] = salary_range_data
        for i, profession_data in enumerate(profession_value):
                working[f'profession_{i}'] = profession_data
#gallery
        all = my['gallery']
        ga = all.replace("[", "").replace("]","").replace("'","").replace(" ","")
        lengthgallery= ga.split(",")

        if 'profile_tag' in request.POST:
                userdata.profile_tag =  request.POST['profile_tag']
                userdata.save()
                return Response(id, status=status.HTTP_200_OK)
        elif 'about_candidate' in request.POST:
                userdata.about_candidate =  request.POST['about_candidate']
                userdata.save()
                return Response(id, status=status.HTTP_200_OK)
        elif 'current_status' in request.POST:
                userdata.current_status =  request.POST['current_status']
                userdata.save()
                return Response(id, status=status.HTTP_200_OK)
        elif 'address' in request.POST:
                userdata.address =  request.POST['address']
                userdata.primary_phone_number =  request.POST['primary_phone_number']
                userdata.primary_email =  request.POST['primary_email']
                userdata.save()
                return Response(id, status=status.HTTP_200_OK)
        elif 'contact_email' in request.POST:
                userdata.contact_email =  request.POST['contact_email']
                userdata.contact_phone =  request.POST['contact_phone']
                userdata.whatsapp =  request.POST['whatsapp']
                userdata.save()
                return Response(id, status=status.HTTP_200_OK)
        elif 'height' in request.POST:
                userdata.height =  request.POST['height']
                userdata.weight =  request.POST['weight']
                userdata.age =  request.POST['age']
                userdata.blood_group =  request.POST['blood_group']
                userdata.marital_status =  request.POST['marital_status']
                userdata.religion =  request.POST['religion']
                userdata.primary_email =  request.POST['primary_email']
                userdata.primary_phone_number =  request.POST['primary_phone_number']
                userdata.education_school =  request.POST['education_school']
                userdata.profession =  request.POST['profession']
                userdata.orphan =  request.POST['orphan']
                userdata.save()
                return Response(id, status=status.HTTP_200_OK)
        elif 'father_name' in request.POST:
                userdata.father_name =  request.POST['father_name']
                userdata.father_country =  request.POST['father_country']
                userdata.father_job =  request.POST['father_job']
                userdata.mother_name =  request.POST['mother_name']
                userdata.mother_country =  request.POST['mother_country']
                userdata.mother_job =  request.POST['mother_job']
                userdata.father_family_name =  request.POST['father_family_name']
                userdata.mother_family_name =  request.POST['mother_family_name']
                userdata.save()
                return Response(id, status=status.HTTP_200_OK)
        elif 'sibling_nameadd' in request.POST:
                print(request.POST)
                sibling_name_addmore = []
                sibling_relation_addmore = []
                sibling_occupation_addmore = []
                sibling_name_addmore.append(sibling['sibling_name_0'])
                sibling_name_addmore.append(request.POST.getlist('sibling_nameadd')[0])
                sibling_relation_addmore.append(sibling['sibling_relation_0'])
                sibling_relation_addmore.append(request.POST.getlist('sibling_relation')[0])
                sibling_occupation_addmore.append(sibling['sibling_occupation_0'])
                sibling_occupation_addmore.append(request.POST.getlist('sibling_occupation')[0])
                userdata.sibling_name =  sibling_name_addmore
                userdata.sibling_relation =  sibling_relation_addmore
                userdata.sibling_occupation =  sibling_occupation_addmore
                print(sibling_name_addmore)
                print(sibling_relation_addmore)
                print(sibling_occupation_addmore)
                userdata.save()
                return Response(id, status=status.HTTP_200_OK)
        
        elif 'sibling_nameedit' in request.POST:
                print(request.POST)
                userdata.sibling_name = request.POST.getlist('sibling_nameedit')
                userdata.sibling_relation = request.POST.getlist('sibling_relation')
                userdata.sibling_occupation = request.POST.getlist('sibling_occupation')
                userdata.save()
                print(userdata.sibling_name)
                print(userdata.sibling_relation )
                print(userdata.sibling_occupation)
                return Response(id, status=status.HTTP_200_OK)

        elif 'education_schooladd' in request.POST:
                print(request.POST)
                education_school_addmore = []
                education_year_addmore = []
                education_course_addmore = []
                education_school_addmore.append(education['education_school_0'])
                education_school_addmore.append(request.POST.getlist('education_schooladd')[0])
                education_year_addmore.append(education['education_year_0'])
                education_year_addmore.append(request.POST.getlist('education_year')[0])
                education_course_addmore.append(education['education_course_0'])
                education_course_addmore.append(request.POST.getlist('education_course')[0])
                userdata.education_school =  education_school_addmore
                userdata.education_year =  education_year_addmore
                userdata.education_course =  education_course_addmore
                print(education_school_addmore)
                print(education_year_addmore)
                print(education_course_addmore)
                userdata.save()
                return Response(id, status=status.HTTP_200_OK)
        
        elif 'education_schooledit' in request.POST:
                print(request.POST)
                userdata.education_school = request.POST.getlist('education_schooledit')
                userdata.education_year = request.POST.getlist('education_year')
                userdata.education_course = request.POST.getlist('education_course')
                userdata.save()
                print(userdata.sibling_name)
                print(userdata.sibling_relation )
                print(userdata.sibling_occupation)
                return Response(id, status=status.HTTP_200_OK)
        
        elif 'company_nameadd' in request.POST:
                print(request.POST)
                company_name_addmore = []
                position_addmore = []
                salary_range_addmore = []
                company_name_addmore.append(working['company_name_0'])
                company_name_addmore.append(request.POST.getlist('company_nameadd')[0])
                position_addmore.append(working['position_0'])
                position_addmore.append(request.POST.getlist('position')[0])
                salary_range_addmore.append(working['salary_range_0'])
                salary_range_addmore.append(request.POST.getlist('salary_range')[0])
                userdata.company_name =  company_name_addmore
                userdata.position =  position_addmore
                userdata.salary_range =  salary_range_addmore
                print(company_name_addmore)
                print(position_addmore)
                print(salary_range_addmore)
                userdata.save()
                return Response(id, status=status.HTTP_200_OK)
        
        elif 'company_nameedit' in request.POST:
                print(request.POST)
                userdata.company_name = request.POST.getlist('company_nameedit')
                userdata.position = request.POST.getlist('position')
                userdata.salary_range = request.POST.getlist('salary_range')
                userdata.save()
                print(userdata.company_name)
                print(userdata.position )
                print(userdata.salary_range)
                return Response(id, status=status.HTTP_200_OK)
        
        elif 'your_intrest' in request.POST:
                print(request.POST)
                userdata.your_intrest = request.POST.getlist('your_intrest')
                userdata.save()
                return Response(id, status=status.HTTP_200_OK)
        
        elif 'non_intrest' in request.POST:
                print(request.POST)
                userdata.non_intrest = request.POST.getlist('non_intrest')
                userdata.save()
                return Response(id, status=status.HTTP_200_OK)
        
        elif 'complexion' in request.POST:
                print(request.POST)
                userdata.complexion = request.POST.getlist('complexion')
                userdata.save()
                return Response(id, status=status.HTTP_200_OK)
        
        elif 'food_taste' in request.POST:
                print(request.POST)
                userdata.food_taste = request.POST.getlist('food_taste')
                userdata.save()
                return Response(id, status=status.HTTP_200_OK)

        elif 'profile_picture' in request.FILES:
                print(request.FILES['profile_picture'])
                fs = FileSystemStorage()
                profileup = str(request.FILES['profile_picture']).replace(" ", "_")
                profile_path = fs.save(f"{id}/id_card/" +
                profileup, request.FILES['profile_picture'])
                full_path = all_image_url+fs.url(profile_path)
                userdata.profile_picture = full_path
                userdata.save()
                return Response(id, status=status.HTTP_200_OK)
        
        elif 'selfie' in request.FILES:
                print(request.FILES['selfie'])
                fs = FileSystemStorage()
                selfieup = str(request.FILES['selfie']).replace(" ", "_")
                selfie_path = fs.save(f"{id}/images/selfie/" +
                selfieup, request.FILES['selfie'])
                full_path = all_image_url+fs.url(selfie_path)
                userdata.selfie = full_path
                userdata.save()
                return Response(id, status=status.HTTP_200_OK)
        
        elif 'full_size_image' in request.FILES:
                print(request.FILES['full_size_image'])
                fs = FileSystemStorage()
                full_size_imageup = str(request.FILES['full_size_image']).replace(" ", "_")
                full_size_image_path = fs.save(f"{id}/images/full_size_image/" +
                full_size_imageup, request.FILES['full_size_image'])
                full_path = all_image_url+fs.url(full_size_image_path)
                userdata.full_size_image = full_path
                userdata.save()
                return Response(id, status=status.HTTP_200_OK)
        
        elif 'family' in request.FILES:
                print(request.FILES['family'])
                fs = FileSystemStorage()
                familyup = str(request.FILES['family']).replace(" ", "_")
                family_path = fs.save(f"{id}/images/family/" +
                familyup, request.FILES['family'])
                full_path = all_image_url+fs.url(family_path)
                userdata.family_image = full_path
                userdata.save()
                return Response(id, status=status.HTTP_200_OK)
        
        elif 'gallery' in request.FILES or 'file_0' in request.FILES:
                print(request.FILES)
                print(lengthgallery)
                image_names = []
                image_list = []
                gallery_web = []
                web_multi_image = request.FILES
                web_multi_imagekey = str(web_multi_image.keys())
                # web_multi_image.pop("selfie")
                print(web_multi_image)
                for x in web_multi_image.keys():
                    gallery_web.append(web_multi_image[x])
                print(gallery_web)
                a = gallery_web
                for y in a:
                    print((y))
               
                # request.FILES.getlist('gallery')
                # print(request.FILES.getlist('gallery'))
                userdata = serializer.ProfileFinder.objects.get(uid=id)
                fs = FileSystemStorage()
                
                if "file_0" in web_multi_imagekey:
                    for i in a:
                        image_names.append(str(i).replace(" ","_"))
                    print(image_names)
                    for qq in range(0,1):
                       for iname in range(0,len(image_names)):
                           gallery_path = fs.save(
                           f"{id}/images/gallery/"+image_names[iname], request.FILES[f'file_{iname}'])
                        #    image_list.append("http://54.159.186.219:8000"+fs.url(gallery_path))
                           lengthgallery.append(all_image_url+fs.url(gallery_path))
                
                else:   
                    for sav in request.FILES.getlist('gallery'):
                        sa = fs.save(
                            f"{id}/images/gallery/"+sav.name, sav)
                        image_names.append(str(sa).replace(" ","_"))
                        # for i in request.FILES.getlist('gallery'):
                        #     image_names.append(str(i).replace(" ","_"))
                        print(image_names)
                        for iname in image_names:
                            # gallery_path = fs.save(
                            #     f"{id}/images/gallery/"+iname, request.FILES['gallery'])
                            gallery_path = iname
                            # image_list.append("http://54.159.186.219:8000"+fs.url(gallery_path))
                            lengthgallery.append(all_image_url+fs.url(gallery_path))
                gallery = str(lengthgallery)
                print(gallery)
                userdata.gallery = gallery
                userdata.save()
                return Response(id, status=status.HTTP_200_OK)
        
        elif 'gallerydelete' in request.POST:
            print(request.POST['gallerydelete'].find("media"))
            print(request.POST['gallerydelete'][request.POST['gallerydelete'].find("media"):])
            lengthgallery.remove(request.POST['gallerydelete'])
            userdata.gallery = str(lengthgallery)
            userdata.save()
            import os
            if os.path.exists(request.POST['gallerydelete'][request.POST['gallerydelete'].find("media"):]):
                os.remove(request.POST['gallerydelete'][request.POST['gallerydelete'].find("media"):])
            
            return Response(id, status=status.HTTP_200_OK)
    except:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def alldata(request):
    if request.method == 'GET':
       allDataa = serializer.ProfileFinder.objects.all()
       alldataserializer = serializer.ProfileFinderSerializer(allDataa,many=True)
    return Response(data=alldataserializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def all_female_user_data(request,id):
    if request.method == 'GET':
        allDataa = serializer.ProfileFinder.objects.filter(gender = "female").values()
        blocked=serializer.block.objects.filter(who_blocked_id=id).values()[0]
        print(blocked)
        if str(blocked['blocked_id'] )== "None" and str(blocked['who_blocked_me'] )== "None":
            print("yes")
            rec_dict = {}
            rec_list = []
            for x in allDataa:
                rec_list.append(x)
            rec_dict[id] = rec_list 
            return JsonResponse(rec_dict)
        elif str(blocked['who_blocked_me'] )== "None":
            blocked_id = blocked['blocked_id'][1:-2].replace("'","").replace(" ","").split(",")
            # print(blocked_id)
            alldata_list = list(allDataa)
            print(alldata_list)
            print(blocked_id)
            all_list=[]
            userlist=[]
            #requested sent
            request_sent = []
            for y in alldata_list:
                userlist.append(y['uid'])
                all_list.append(y['uid'])
            print(userlist)
            for i,z in enumerate(blocked_id):
                userlist.remove(z)
            print(userlist)
            
            for i,q in enumerate(userlist):
                numb = all_list.index(q)
                print(numb)
                get_Selected = alldata_list[numb]
                request_sent.append(get_Selected)
            print(request_sent)
            rec_dict = {}
            rec_list = []
            for x in request_sent:
                rec_list.append(x)
            rec_dict[id] = rec_list 
            print("elif")
            return JsonResponse(rec_dict)
        elif str(blocked['blocked_id'] )== "None" and str(blocked['who_blocked_me'] )!= "None":
            print("who blocked me")
            blocked_id = blocked['who_blocked_me'][1:-2].replace("'","").replace(" ","").split(",")
            print(blocked_id)
            alldata_list = list(allDataa)
            print(alldata_list)
            print(blocked_id)
            all_list=[]
            userlist=[]
            #requested sent
            request_sent = []
            for y in alldata_list:
                userlist.append(y['uid'])
                all_list.append(y['uid'])
            print(userlist)
            for i,z in enumerate(blocked_id):
                userlist.remove(z)
            print(userlist)
            
            for i,q in enumerate(userlist):
                numb = all_list.index(q)
                print(numb)
                get_Selected = alldata_list[numb]
                request_sent.append(get_Selected)
            print(request_sent)
            rec_dict = {}
            rec_list = []
            for x in request_sent:
                rec_list.append(x)
            rec_dict[id] = rec_list 
            # print("elif")
            return JsonResponse(rec_dict)
 
        else:
            blocked_id = blocked['blocked_id'][1:-2].replace("'","").replace(" ","").split(",")
            # print(blocked_id)
            alldata_list = list(allDataa)
            print(alldata_list)
            print(blocked_id)
            all_list=[]
            userlist=[]
            #requested sent
            request_sent = []
            for y in alldata_list:
                userlist.append(y['uid'])
                all_list.append(y['uid'])
            print(userlist)
            for i,z in enumerate(blocked_id):
                userlist.remove(z)
            print(userlist)
            
            for i,q in enumerate(userlist):
                numb = all_list.index(q)
                print(numb)
                get_Selected = alldata_list[numb]
                request_sent.append(get_Selected)
            print(request_sent)

            #for who blocked me
            blocked_id_me = blocked['who_blocked_me'][1:-2].replace("'","").replace(" ","").split(",")
            # print(blocked_id)
            # alldata_list = list(allDataa)
            # print(alldata_list)
            print(blocked_id)
            all_list_me=[]
            userlist_me=[]
            #requested sent
            request_sent_me = []
            for y in request_sent:
                userlist_me.append(y['uid'])
                all_list_me.append(y['uid'])
            print(userlist_me)
            for i,z in enumerate(blocked_id_me):
                userlist_me.remove(z)
            print(userlist_me)
            
            for i,q in enumerate(userlist_me):
                numb = all_list_me.index(q)
                print(numb)
                get_Selected = request_sent[numb]
                request_sent_me.append(get_Selected)
            print(request_sent_me)

            print("else")
            rec_dict = {}
            rec_list = []
            for x in request_sent_me:
                rec_list.append(x)
            rec_dict[id] = rec_list 
            return JsonResponse(rec_dict)
            # allDataa = serializer.ProfileFinder.objects.filter(gender = "female")
            # alldataserializer = serializer.ProfileFinderSerializer(allDataa,many=True)
            # return Response(data=alldataserializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def all_male_user_data(request,id):
    if request.method == 'GET':
        allDataa = serializer.ProfileFinder.objects.filter(gender = "male").values()
        blocked=serializer.block.objects.filter(who_blocked_id=id).values()[0]
        print(blocked)
        if str(blocked['blocked_id'] )== "None" and str(blocked['who_blocked_me'] )== "None":
            print("yes")
            rec_dict = {}
            rec_list = []
            for x in allDataa:
                rec_list.append(x)
            rec_dict[id] = rec_list 
            return JsonResponse(rec_dict)
        elif str(blocked['who_blocked_me'] )== "None":
            blocked_id = blocked['blocked_id'][1:-2].replace("'","").replace(" ","").split(",")
            # print(blocked_id)
            alldata_list = list(allDataa)
            print(alldata_list)
            print(blocked_id)
            all_list=[]
            userlist=[]
            #requested sent
            request_sent = []
            for y in alldata_list:
                userlist.append(y['uid'])
                all_list.append(y['uid'])
            print(userlist)
            for i,z in enumerate(blocked_id):
                userlist.remove(z)
            print(userlist)
            
            for i,q in enumerate(userlist):
                numb = all_list.index(q)
                print(numb)
                get_Selected = alldata_list[numb]
                request_sent.append(get_Selected)
            print(request_sent)
            rec_dict = {}
            rec_list = []
            for x in request_sent:
                rec_list.append(x)
            rec_dict[id] = rec_list 
            print("elif")
            return JsonResponse(rec_dict)
        elif str(blocked['blocked_id'] )== "None" and str(blocked['who_blocked_me'] )!= "None":
            print("who blocked me")
            blocked_id = blocked['who_blocked_me'][1:-2].replace("'","").replace(" ","").split(",")
            print(blocked_id)
            alldata_list = list(allDataa)
            print(alldata_list)
            print(blocked_id)
            all_list=[]
            userlist=[]
            #requested sent
            request_sent = []
            for y in alldata_list:
                userlist.append(y['uid'])
                all_list.append(y['uid'])
            print(userlist)
            for i,z in enumerate(blocked_id):
                userlist.remove(z)
            print(userlist)
            
            for i,q in enumerate(userlist):
                numb = all_list.index(q)
                print(numb)
                get_Selected = alldata_list[numb]
                request_sent.append(get_Selected)
            print(request_sent)
            rec_dict = {}
            rec_list = []
            for x in request_sent:
                rec_list.append(x)
            rec_dict[id] = rec_list 
            # print("elif")
            return JsonResponse(rec_dict)
 
        else:
            blocked_id = blocked['blocked_id'][1:-2].replace("'","").replace(" ","").split(",")
            # print(blocked_id)
            alldata_list = list(allDataa)
            print(alldata_list)
            print(blocked_id)
            all_list=[]
            userlist=[]
            #requested sent
            request_sent = []
            for y in alldata_list:
                userlist.append(y['uid'])
                all_list.append(y['uid'])
            print(userlist)
            for i,z in enumerate(blocked_id):
                userlist.remove(z)
            print(userlist)
            
            for i,q in enumerate(userlist):
                numb = all_list.index(q)
                print(numb)
                get_Selected = alldata_list[numb]
                request_sent.append(get_Selected)
            print(request_sent)

            #for who blocked me
            blocked_id_me = blocked['who_blocked_me'][1:-2].replace("'","").replace(" ","").split(",")
            # print(blocked_id)
            # alldata_list = list(allDataa)
            # print(alldata_list)
            print(blocked_id)
            all_list_me=[]
            userlist_me=[]
            #requested sent
            request_sent_me = []
            for y in request_sent:
                userlist_me.append(y['uid'])
                all_list_me.append(y['uid'])
            print(userlist_me)
            for i,z in enumerate(blocked_id_me):
                userlist_me.remove(z)
            print(userlist_me)
            
            for i,q in enumerate(userlist_me):
                numb = all_list_me.index(q)
                print(numb)
                get_Selected = request_sent[numb]
                request_sent_me.append(get_Selected)
            print(request_sent_me)

            print("else")
            rec_dict = {}
            rec_list = []
            for x in request_sent_me:
                rec_list.append(x)
            rec_dict[id] = rec_list 
            return JsonResponse(rec_dict)
    #    allDataa = serializer.ProfileFinder.objects.filter(gender = "male")
    #    alldataserializer = serializer.ProfileFinderSerializer(allDataa,many=True)
    # return Response(data=alldataserializer.data, status=status.HTTP_200_OK)

@api_view(['GET','POST'])
def requested_list(request, id):
    try:
       
        if request.method == 'GET':
            alldata=serializer.ProfileFinder.objects.filter(uid=id).values()
            gender = alldata[0]['gender']
            requestdataa = serializer.sender_list.objects.filter(sender_uid = id)
            requestdata = serializer.sender_list.objects.filter(sender_uid = id).values()
            received = requestdata[0]['received_uid']
            print(received)
            
            if str(received) == "None":
                print("yes")
                request_sent= ""
                print(request_sent)
                rec_dict = {}
                rec_dict[id] = request_sent 
                print(rec_dict)
            else:
                print("no")
                received_uid_list = received[1:-2].replace("'","").replace(" ","").split(",")
                print(received_uid_list)
                if gender == "female":
                   allmaleuser=serializer.ProfileFinder.objects.filter(gender = "male").values()
                #    print(allmaleuser)
                   #find uid position
                   userlist=[]
                   #requested sent
                   request_sent = []
                   for y in allmaleuser:
                       userlist.append(y['uid'])
                   print(userlist)
                   for i,x in enumerate(received_uid_list):
                       numb = userlist.index(x)
                       get_Selected = allmaleuser[numb]
                       get_Selected['action'] = requestdata[0]['action'][1:-2].replace("'","").replace(" ","").split(",")[i]
                       request_sent.append(get_Selected)
                       print(get_Selected)
                elif gender == "male":
                    allfemaleuser=serializer.ProfileFinder.objects.filter(gender = "female").values()
                    #find uid position
                    userlist=[]
                    #requested sent
                    request_sent = []
                    for y in allfemaleuser:
                        userlist.append(y['uid'])
                        # print(y['uid'])
                    for i,x in enumerate(received_uid_list):
                        numb = userlist.index(x)
                        get_Selected = allfemaleuser[numb]
                        get_Selected['action'] = requestdata[0]['action'][1:-2].replace("'","").replace(" ","").split(",")[i]
                        request_sent.append(get_Selected)
                        print(request_sent)
                rec_dict = {}
                rec_list = []
                for x in request_sent:
                    # rec = {}
                    # rec['received_uid'] = x
                    rec_list.append(x)
                rec_dict[id] = rec_list 
            print(rec_dict)
            # print(requestdata[0]['action'][1:-2].replace("'","").replace(" ","").split(","))
            return JsonResponse(rec_dict)
            # requestdataserializer = serializer.SenderSerializer(requestdataa,many=True)
            # return Response(data=requestdataserializer.data, status=status.HTTP_200_OK)
            
            
    

        elif request.method == "POST":
            # print(request.POST)
            userdata_sender = serializer.sender_list.objects.get(sender_uid=id)
            userdata_sender_list = serializer.sender_list.objects.filter(sender_uid=id).values()
            remove_userdata_sender_list = userdata_sender_list[0]
            del remove_userdata_sender_list['id']
            del remove_userdata_sender_list['sender_uid']
            # del remove_userdata_sender_list['action']
            print(remove_userdata_sender_list)
            
            userdata_sender_listed_dict = {}
            datas={
                'received_uid' : request.POST['received_uid'],
                'request_phone_number' : request.POST['request_phone_number'],
                'request_whatsapp_number' : request.POST['request_whatsapp_number'],
                'request_address' : request.POST['request_address'],
                'request_horoscope' : request.POST['request_horoscope'],
                'request_social_media_link' : request.POST['request_social_media_link'],
                'action' : "empty"
            }
            print(datas)
            none_to_list = [remove_userdata_sender_list['received_uid']]
            for none in none_to_list:
                a = str(none)
                print(a)
            if a == "None":
                print("new")
                for x in remove_userdata_sender_list:
                   add = []
                   add.append(datas[x])
                   userdata_sender_listed_dict[x] = str(add)
                print(userdata_sender_listed_dict)
            
            elif datas['received_uid'] in remove_userdata_sender_list['received_uid']:
                change_list = remove_userdata_sender_list['received_uid']
                find_position = change_list[1:-2].replace("'","").replace(" ","").split(",")

                print(find_position.index(datas['received_uid']))
                for x in remove_userdata_sender_list:
                    add = remove_userdata_sender_list[x][1:-2].replace("'","").replace(" ","").split(",")
                    add[find_position.index(datas['received_uid'])] = datas[x]
                    print(add[find_position.index(datas['received_uid'])])
                    userdata_sender_listed_dict[x] = str(add)
                print(userdata_sender_listed_dict)
            else:
                print("nil")
                for x in remove_userdata_sender_list:
                   add = remove_userdata_sender_list[x][1:-2].replace("'","").replace(" ","").split(",")
                   add.append(datas[x])
                   userdata_sender_listed_dict[x] = str(add)
                print(userdata_sender_listed_dict)
#received_uid
            userdata_received = serializer.received_list.objects.get(received_uid=request.POST['received_uid'])
            userdata_received_list = serializer.received_list.objects.filter(received_uid=request.POST['received_uid']).values()
            # print(userdata_received_list)
            remove_userdata_received_list = userdata_received_list[0]
            del remove_userdata_received_list['id']
            del remove_userdata_received_list['received_uid']
            # del remove_userdata_received_list['action']
            # print(remove_userdata_received_list)
            userdata_received_listed_dict = {}
            
            dataa={
                'sender_uid' : id,
                'request_phone_number' : request.POST['request_phone_number'],
                'request_whatsapp_number' : request.POST['request_whatsapp_number'],
                'request_address' : request.POST['request_address'],
                'request_horoscope' : request.POST['request_horoscope'],
                'request_social_media_link' : request.POST['request_social_media_link'],
                'action' : "empty"
            }
            print(dataa['sender_uid'])
            none_to_list_b = [remove_userdata_received_list['sender_uid']]
            for none_b in none_to_list_b:
                b = str(none_b)
                print(b)
            if b == "None":
                print("new")
                for x in remove_userdata_received_list:
                   add = []
                   add.append(dataa[x])
                   userdata_received_listed_dict[x] = str(add)
                print(userdata_received_listed_dict)

            elif dataa['sender_uid'] in remove_userdata_received_list['sender_uid']:
                change_list = remove_userdata_received_list['sender_uid']
                find_position = change_list[1:-2].replace("'","").replace(" ","").split(",")

                print(find_position.index(dataa['sender_uid']))
                for x in remove_userdata_received_list:
                    add = remove_userdata_received_list[x][1:-2].replace("'","").replace(" ","").split(",")
                    add[find_position.index(dataa['sender_uid'])] = dataa[x]
                    print(add[find_position.index(dataa['sender_uid'])])
                    userdata_received_listed_dict[x] = str(add)
                print(userdata_received_listed_dict)
            else:
                print("nil")
                for x in remove_userdata_received_list:
                   add = remove_userdata_received_list[x][1:-2].replace("'","").replace(" ","").split(",")
                   print(add)
                   add.append(dataa[x])
                   userdata_received_listed_dict[x] = str(add)
                print(userdata_received_listed_dict)
           
            sender_list = serializer.sender_request_Serializer(
            instance=userdata_sender, data=userdata_sender_listed_dict, partial=True)
            received_list = serializer.received_request_Serializer(
            instance=userdata_received, data=userdata_received_listed_dict, partial=True)
            if sender_list.is_valid() and received_list.is_valid():
                sender_list.save()
                received_list.save()
                print("valid data")
                return Response({"valid Data"}, status=status.HTTP_200_OK)
            else:
                return Response({"Bad Request"}, status=status.HTTP_403_FORBIDDEN)
            # return Response(id, status=status.HTTP_200_OK)
                
    except:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET','POST'])
def received_list(request, id):
    try:
        if request.method == 'GET':
                alldata=serializer.ProfileFinder.objects.filter(uid=id).values()
                gender = alldata[0]['gender']
                requestdataa = serializer.received_list.objects.filter(received_uid = id)
                requestdata = serializer.received_list.objects.filter(received_uid = id).values()
                print(requestdata)
                sender_uid_list = requestdata[0]['sender_uid']
                if str(sender_uid_list) == "None":
                    print("yes")
                    request_sent= ""
                    print(request_sent)
                    rec_dict = {}
                    rec_dict[id] = request_sent 
                    print(rec_dict)
                else:
                    print("no")
                    received_uid_list = sender_uid_list[1:-2].replace("'","").replace(" ","").split(",")
                    print(received_uid_list)
                
                    if gender == "female":
                       allmaleuser=serializer.ProfileFinder.objects.filter(gender = "male").values()
                    #    print(allmaleuser)
                       #find uid position
                       userlist=[]
                       #requested sent
                       request_sent = []
                       for y in allmaleuser:
                           userlist.append(y['uid'])
                       print(userlist)
                       for i,x in enumerate(received_uid_list):
                           numb = userlist.index(x)
                           get_Selected = allmaleuser[numb]
                           get_Selected['action'] = requestdata[0]['action'][1:-2].replace("'","").replace(" ","").split(",")[i]
                           request_sent.append(get_Selected)
                        #    request_sent.append(allmaleuser[numb])
                        #    print(allmaleuser[numb])
                    elif gender == "male":
                        allfemaleuser=serializer.ProfileFinder.objects.filter(gender = "female").values()
                        #find uid position
                        userlist=[]
                        #requested sent
                        request_sent = []
                        for y in allfemaleuser:
                            userlist.append(y['uid'])
                            # print(y['uid'])
                        for i,x in enumerate(received_uid_list):
                            numb = userlist.index(x)
                            get_Selected = allfemaleuser[numb]
                            get_Selected['action'] = requestdata[0]['action'][1:-2].replace("'","").replace(" ","").split(",")[i]
                            request_sent.append(get_Selected)
                            # request_sent.append(allfemaleuser[numb])
                            # print(allfemaleuser[numb])
                    rec_dict = {}
                    rec_list = []
                    for x in request_sent:
                        # rec = {}
                        # rec['received_uid'] = x
                        rec_list.append(x)
                    rec_dict[id] = rec_list 
                    # print(rec_dict)
                return JsonResponse(rec_dict)
            
        elif request.method == 'POST':
            print(request.POST) 
            print(request.POST['uid']) 
            print(id)
            #received
            getid_list = serializer.received_list.objects.filter(received_uid = id).values()
            find_position =getid_list[0]['sender_uid'][1:-2].replace("'","").replace(" ","").split(",")
            position_get = find_position.index(request.POST['uid'])
            print(position_get) 
            action_list =getid_list[0]['action'][1:-2].replace("'","").replace(" ","").split(",")
            action_list[position_get]= request.POST['action']
            print(action_list)
            getid = serializer.received_list.objects.get(received_uid = id)
            getid.action = str(action_list)
            getid.save()
            #sender
            getid_list_b = serializer.sender_list.objects.filter(sender_uid = request.POST['uid']).values()
            print(getid_list_b)
            find_position_b =getid_list_b[0]['received_uid'][1:-2].replace("'","").replace(" ","").split(",")
            position_get_b = find_position_b.index(id)
            print(position_get_b) 
            action_list_b =getid_list_b[0]['action'][1:-2].replace("'","").replace(" ","").split(",")
            action_list_b[position_get_b]= request.POST['action']
            print(action_list_b)
            #save
            
            getid_b = serializer.sender_list.objects.get(sender_uid = request.POST['uid'])
            getid_b.action = str(action_list_b)
            getid_b.save()
            return Response({"valid Data"}, status=status.HTTP_200_OK)

    except:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET','POST'])
def block(request, id):
    try:
        if request.method == 'GET':
            alldata=serializer.ProfileFinder.objects.filter(uid=id).values()
            blocked=serializer.block.objects.filter(who_blocked_id=id).values()[0]
            sender_uid_list = blocked['blocked_id']
            if str(sender_uid_list) == "None":
                print("yes")
                request_sent= ""
                # print(request_sent)
                rec_dict = {}
                rec_dict[id] = request_sent 
                # print(rec_dict)
                return JsonResponse(rec_dict)

            else:
                print("no")
                blocked_id = blocked['blocked_id'][1:-2].replace("'","").replace(" ","").split(",")
                block_reason_data = blocked['reason'][1:-2].replace("'","").replace(" ","").split(",")
                blocked_list=[]
                for i,x in enumerate(blocked_id):
                    # print(x)
                    blocked_data=serializer.ProfileFinder.objects.filter(uid=x).values()[0]
                    blocked_data['block_reason'] = block_reason_data[i]
                    blocked_list.append(blocked_data)
                block_dict = {}
                block_list = []
                for x in blocked_list:
                    block_list.append(x)
                block_dict[id] = blocked_list 
                # print(block_dict)
                return JsonResponse(block_dict)
        elif request.method == 'POST':
            print(id)
            #unblock
            if "unblock" in request.POST:
                print(request.POST)
                blocked_userdata = serializer.block.objects.get(who_blocked_id=id)
                blocked_list_values = serializer.block.objects.filter(who_blocked_id=id).values()[0]
                print(blocked_list_values)
                block_idd = blocked_list_values['blocked_id'][1:-2].replace("'","").replace(" ","").split(",")
                block_reason = blocked_list_values['reason'][1:-2].replace("'","").replace(" ","").split(",")
                # block_idd.remove(request.POST['unblock'])
                position = block_idd.index(request.POST['unblock'])  
                block_idd.pop(position)    
                block_reason.pop(position)               
                if len(block_idd) == 0:
                    # blocked_all_list = {'who_blocked_id' : id,}
                    blocked_all_list={
                        'who_blocked_id' : id,
                        'blocked_id' : "None",
                        'reason' : "None"
                    }
                    print(blocked_all_list)
                else:
                    # blocked_all_list = {'who_blocked_id' : id,}
                    blocked_all_list={
                        'who_blocked_id' : id,
                        'blocked_id' : str(block_idd),
                        'reason' : str(block_reason)
                    }
                    print(blocked_all_list)

                # who blocked me
                blocked_me_userdata = serializer.block.objects.get(who_blocked_id=request.POST['unblock'])
                blocked_me_list_values = serializer.block.objects.filter(who_blocked_id=request.POST['unblock']).values()[0]
                print(blocked_me_list_values)
                block_me_idd = blocked_me_list_values['who_blocked_me'][1:-2].replace("'","").replace(" ","").split(",")
                position = block_me_idd.index(id)  
                block_me_idd.pop(position)  
                print(block_me_idd) 
                if len(block_me_idd) == 0:
                    print("yes")
                    # blocked_me_all_list = {'who_blocked_id' : request.POST['unblock'],}
                    blocked_me_all_list={
                        'who_blocked_id' : request.POST['unblock'],
                        'who_blocked_me' : "None"
                    }
                    print(blocked_me_all_list)
                else:
                    # blocked_me_all_list = {'who_blocked_id' : request.POST['unblock'],}
                    blocked_me_all_list={
                        'who_blocked_id' : request.POST['unblock'],
                        'who_blocked_me' : str(block_me_idd)
                    }
                    print(blocked_me_all_list)
                #save
                #blocked id
                blocked_list = serializer.blocked_Serializer(
                instance=blocked_userdata, data=blocked_all_list, partial=True)
                #who blcoked me
                blocked_me_list = serializer.blocked_me_Serializer(
                instance=blocked_me_userdata, data=blocked_me_all_list, partial=True)
                if blocked_list.is_valid()  and blocked_me_list.is_valid():
                    blocked_list.save()
                    blocked_me_list.save()
                    print("valid data")
                    return Response({"valid Data"}, status=status.HTTP_200_OK)
                else:
                    return Response({"Bad Request"}, status=status.HTTP_403_FORBIDDEN)
            #block    
            else:
                print(request.POST)
                blocked_userdata = serializer.block.objects.get(who_blocked_id=id)
                blocked_list_values = serializer.block.objects.filter(who_blocked_id=id).values()[0]
                print(blocked_list_values)
                del blocked_list_values['id']
                del blocked_list_values['who_blocked_id']
                del blocked_list_values['who_blocked_me']
    
                blocked_all_list = {'who_blocked_id' : id,}
                datas={
                    'who_blocked_id' : id,
                    'blocked_id' : request.POST['blocked_id'],
                    'reason' : request.POST['reason']
                }
                print(datas)
                
                none_to_list = [blocked_list_values['blocked_id']]
                for none in none_to_list:
                    a = str(none)
                    print(a)
                #for new
                if a == "None":
                    print("new")
                    for x in blocked_list_values:
                       add = []
                       add.append(datas[x])
                       print(add)
                       blocked_all_list[x] = str(add)
                    print(blocked_all_list)
                else:
                    print("nil")
                    for x in blocked_list_values:
                       add = blocked_list_values[x][1:-2].replace("'","").replace(" ","").split(",")
                       add.append(datas[x])
                       blocked_all_list[x] = str(add)
                    print(blocked_all_list)
                
                #who blocked me
                blocked_me_userdata = serializer.block.objects.get(who_blocked_id=request.POST['blocked_id'])
                blocked_me_list_values = serializer.block.objects.filter(who_blocked_id=request.POST['blocked_id']).values()[0]
                print(blocked_me_list_values)
                del blocked_me_list_values['id']
                del blocked_me_list_values['who_blocked_id']
                del blocked_me_list_values['blocked_id']
                del blocked_me_list_values['reason']
                blocked_me_all_list = {'who_blocked_id' : request.POST['blocked_id'],}
                dataa={
                    'who_blocked_id' : request.POST['blocked_id'],
                    'who_blocked_me' : id
                }
                print(dataa)
                none_to_me_list = [blocked_me_list_values['who_blocked_me']]
                for none in none_to_me_list:
                    a = str(none)
                    print(a)
                #for new
                if a == "None":
                    print("new")
                    for x in blocked_me_list_values:
                       add = []
                       add.append(dataa[x])
                       print(add)
                       blocked_me_all_list[x] = str(add)
                    print(blocked_me_all_list)
                else:
                    print("nil")
                    for x in blocked_me_list_values:
                       add = blocked_me_list_values[x][1:-2].replace("'","").replace(" ","").split(",")
                       add.append(dataa[x])
                       blocked_me_all_list[x] = str(add)
                    print(blocked_me_all_list)
    
                #save
                #blocked id
                blocked_list = serializer.blocked_Serializer(
                instance=blocked_userdata, data=blocked_all_list, partial=True)
                #who blcoked me
                blocked_me_list = serializer.blocked_me_Serializer(
                instance=blocked_me_userdata, data=blocked_me_all_list, partial=True)
                if blocked_list.is_valid() and blocked_me_list.is_valid() :
                    blocked_list.save()
                    blocked_me_list.save()
                    print("valid data")
                    return Response({"valid Data"}, status=status.HTTP_200_OK)
                else:
                    return Response({"Bad Request"}, status=status.HTTP_403_FORBIDDEN)
                
    except:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['GET','POST'])
def favorites(request, id):
    try:
        if request.method == 'GET':
            alldata=serializer.ProfileFinder.objects.filter(uid=id).values()
            gender = alldata[0]['gender']
            requestdataa = serializer.favorite.objects.filter(my_id = id)
            requestdata = serializer.favorite.objects.filter(my_id = id).values()
            received = requestdata[0]['myfavorite_id']
            print(received)
            
            if str(received) == "None":
                print("yes")
                request_sent= ""
                print(request_sent)
                rec_dict = {}
                rec_dict[id] = request_sent 
                print(rec_dict)
            
            else:
                print("no")
                received_uid_list = received[1:-2].replace("'","").replace(" ","").split(",")
                print(received_uid_list)
                if gender == "female":
                   allmaleuser=serializer.ProfileFinder.objects.filter(gender = "male").values()
                #    print(allmaleuser)
                   #find uid position
                   userlist=[]
                   #requested sent
                   request_sent = []
                   for y in allmaleuser:
                       userlist.append(y['uid'])
                   print(userlist)
                   for i,x in enumerate(received_uid_list):
                       numb = userlist.index(x)
                       get_Selected = allmaleuser[numb]
                    #    get_Selected['action'] = requestdata[0]['action'][1:-2].replace("'","").replace(" ","").split(",")[i]
                       request_sent.append(get_Selected)
                       print(get_Selected)
                elif gender == "male":
                    allfemaleuser=serializer.ProfileFinder.objects.filter(gender = "female").values()
                    #find uid position
                    userlist=[]
                    #requested sent
                    request_sent = []
                    for y in allfemaleuser:
                        userlist.append(y['uid'])
                        # print(y['uid'])
                    for i,x in enumerate(received_uid_list):
                        numb = userlist.index(x)
                        get_Selected = allfemaleuser[numb]
                        # get_Selected['action'] = requestdata[0]['action'][1:-2].replace("'","").replace(" ","").split(",")[i]
                        request_sent.append(get_Selected)
                        print(request_sent)
                rec_dict = {}
                rec_list = []
                for x in request_sent:
                    # rec = {}
                    # rec['received_uid'] = x
                    rec_list.append(x)
                rec_dict[id] = rec_list 
            print(rec_dict)
            # print(requestdata[0]['action'][1:-2].replace("'","").replace(" ","").split(","))
            return JsonResponse(rec_dict)
        elif request.method == 'POST':
            print(id)
            print(request.POST)
            blocked_userdata = serializer.favorite.objects.get(my_id=id)
            blocked_list_values = serializer.favorite.objects.filter(my_id=id).values()[0]
            print(blocked_list_values)
            del blocked_list_values['id']
            del blocked_list_values['my_id']
            del blocked_list_values['who_favorite_me_id']
            # print(blocked_list_values[1:-2].replace("'","").replace(" ","").split(","))
            # print(request.POST) 

            blocked_all_list = {'my_id' : id,}
            datas={
                'my_id' : id,
                'myfavorite_id' : request.POST['myfavorite_id']
            }
            print(datas)
            
            none_to_list = [blocked_list_values['myfavorite_id']]
            for none in none_to_list:
                a = str(none)
                print(a)
            #for new
            if a == "None":
                print("new")
                for x in blocked_list_values:
                   add = []
                   add.append(datas[x])
                   print(add)
                   blocked_all_list[x] = str(add)
                   print(blocked_all_list)

            elif datas['myfavorite_id'] in blocked_list_values['myfavorite_id']:
                change_list = blocked_list_values['myfavorite_id']
                find_position = change_list[1:-2].replace("'","").replace(" ","").split(",")

                print(find_position.index(datas['myfavorite_id']))
                for x in blocked_list_values:
                    add = blocked_list_values[x][1:-2].replace("'","").replace(" ","").split(",")
                    add[find_position.index(datas['myfavorite_id'])] = datas[x]
                    print(add[find_position.index(datas['myfavorite_id'])])
                    blocked_all_list[x] = str(add)
                print(blocked_all_list)
            else:
                print("nil")
                for x in blocked_list_values:
                   add = blocked_list_values[x][1:-2].replace("'","").replace(" ","").split(",")
                   add.append(datas[x])
                   blocked_all_list[x] = str(add)
                print(blocked_all_list)
            
            #who blocked me
            blocked_me_userdata = serializer.favorite.objects.get(my_id=request.POST['myfavorite_id'])
            blocked_me_list_values = serializer.favorite.objects.filter(my_id=request.POST['myfavorite_id']).values()[0]
            print(blocked_me_list_values)
            del blocked_me_list_values['id']
            del blocked_me_list_values['my_id']
            del blocked_me_list_values['myfavorite_id']
            blocked_me_all_list = {'my_id' : request.POST['myfavorite_id'],}
            dataa={
                'my_id' : request.POST['myfavorite_id'],
                'who_favorite_me_id' : id
            }
            print(dataa)
            none_to_me_list = [blocked_me_list_values['who_favorite_me_id']]
            for none in none_to_me_list:
                a = str(none)
                print(a)
            #for new
            if a == "None":
                print("new")
                for x in blocked_me_list_values:
                   add = []
                   add.append(dataa[x])
                   print(add)
                   blocked_me_all_list[x] = str(add)
                print(blocked_me_all_list)
            elif dataa['who_favorite_me_id'] in blocked_me_list_values['who_favorite_me_id']:
                print("replace")
                change_list = blocked_me_list_values['who_favorite_me_id']
                find_position = change_list[1:-2].replace("'","").replace(" ","").split(",")

                print(find_position.index(dataa['who_favorite_me_id']))
                for x in blocked_me_list_values:
                    add = blocked_me_list_values[x][1:-2].replace("'","").replace(" ","").split(",")
                    add[find_position.index(dataa['who_favorite_me_id'])] = dataa[x]
                    print(add[find_position.index(dataa['who_favorite_me_id'])])
                    blocked_me_all_list[x] = str(add)
                print(blocked_me_all_list)
            else:
                print("add")
                for x in blocked_me_list_values:
                   add = blocked_me_list_values[x][1:-2].replace("'","").replace(" ","").split(",")
                   add.append(dataa[x])
                   blocked_me_all_list[x] = str(add)
                print(blocked_me_all_list)

            #save
            #blocked id
            blocked_list = serializer.favorite_Serializer(
            instance=blocked_userdata, data=blocked_all_list, partial=True)
            #who blcoked me
            blocked_me_list = serializer.favorite_me_Serializer(
            instance=blocked_me_userdata, data=blocked_me_all_list, partial=True)
            if blocked_list.is_valid() and blocked_me_list.is_valid() :
                blocked_list.save()
                blocked_me_list.save()
                print("valid data")
                return Response({"valid Data"}, status=status.HTTP_200_OK)
            else:
                return Response({"Bad Request"}, status=status.HTTP_403_FORBIDDEN)
            
    except:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET','POST'])
def favorites_to_me(request, id):
    try:
        if request.method == 'GET':
                alldata=serializer.ProfileFinder.objects.filter(uid=id).values()
                gender = alldata[0]['gender']
                requestdataa = serializer.favorite.objects.filter(my_id = id)
                requestdata = serializer.favorite.objects.filter(my_id = id).values()
                print(requestdata)
                sender_uid_list = requestdata[0]['who_favorite_me_id']
                if str(sender_uid_list) == "None":
                    print("yes")
                    request_sent= ""
                    print(request_sent)
                    rec_dict = {}
                    rec_dict[id] = request_sent 
                    print(rec_dict)
                else:
                    print("no")
                    received_uid_list = sender_uid_list[1:-2].replace("'","").replace(" ","").split(",")
                    print(received_uid_list)
                
                    if gender == "female":
                       allmaleuser=serializer.ProfileFinder.objects.filter(gender = "male").values()
                    #    print(allmaleuser)
                       #find uid position
                       userlist=[]
                       #requested sent
                       request_sent = []
                       for y in allmaleuser:
                           userlist.append(y['uid'])
                       print(userlist)
                       for i,x in enumerate(received_uid_list):
                           numb = userlist.index(x)
                           get_Selected = allmaleuser[numb]
                        #    get_Selected['action'] = requestdata[0]['action'][1:-2].replace("'","").replace(" ","").split(",")[i]
                           request_sent.append(get_Selected)
                        #    request_sent.append(allmaleuser[numb])
                        #    print(allmaleuser[numb])
                    elif gender == "male":
                        allfemaleuser=serializer.ProfileFinder.objects.filter(gender = "female").values()
                        #find uid position
                        userlist=[]
                        #requested sent
                        request_sent = []
                        for y in allfemaleuser:
                            userlist.append(y['uid'])
                            # print(y['uid'])
                        for i,x in enumerate(received_uid_list):
                            numb = userlist.index(x)
                            get_Selected = allfemaleuser[numb]
                            # get_Selected['action'] = requestdata[0]['action'][1:-2].replace("'","").replace(" ","").split(",")[i]
                            request_sent.append(get_Selected)
                            # request_sent.append(allfemaleuser[numb])
                            # print(allfemaleuser[numb])
                    rec_dict = {}
                    rec_list = []
                    for x in request_sent:
                        # rec = {}
                        # rec['received_uid'] = x
                        rec_list.append(x)
                    rec_dict[id] = rec_list 
                    # print(rec_dict)
                return JsonResponse(rec_dict)
      
            
    except:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
def happy_couples(request, id):
    try:
      
        if request.method == 'POST':
            print(request.POST)
            print(request.FILES)
            image_names = []
            image_list = []
            gallery_web = []
            web_multi_image = request.FILES
            web_multi_imagekey = str(web_multi_image.keys())
            # web_multi_image.pop("selfie")
            print(web_multi_imagekey)
            for x in web_multi_image.keys():
                gallery_web.append(web_multi_image[x])
            print(gallery_web)
            # a = gallery_web[4:]
            for y in gallery_web:
                print((y))
           
            # request.FILES.getlist('gallery')
            # print(request.FILES.getlist('gallery'))
            # userdata = serializer.ProfileFinder.objects.get(uid=id)
            fs = FileSystemStorage()
            
            if "file_0" in web_multi_imagekey:
                for i in gallery_web:
                    image_names.append(str(i).replace(" ","_"))
                print(image_names)
                for qq in range(0,1):
                   for iname in range(0,len(image_names)):
                       gallery_path = fs.save(
                       f"{id}/images/happy_couples/"+image_names[iname], request.FILES[f'file_{iname}'])
                    #    image_list.append("http://54.159.186.219:8000"+fs.url(gallery_path))
                       image_list.append(all_image_url+fs.url(gallery_path))
            
            else:   
                for sav in request.FILES.getlist('image_videous'):
                    sa = fs.save(
                        f"{id}/images/happy_couples/"+sav.name, sav)
                    image_names.append(str(sa).replace(" ","_"))
                # for i in request.FILES.getlist('gallery'):
                #     image_names.append(str(i).replace(" ","_"))
                print(image_names)
                for iname in image_names:
                    # gallery_path = fs.save(
                    #     f"{id}/images/gallery/"+iname, request.FILES['gallery'])
                    gallery_path = iname
                    # image_list.append("http://54.159.186.219:8000"+fs.url(gallery_path))
                    image_list.append(all_image_url+fs.url(gallery_path))
            print(image_list)
            data={
            'groom_name':request.POST['groom_name'],
            'groom_id':request.POST['groom_id'],
            'bride_name':request.POST['bride_name'],
            'bride_id':request.POST['bride_id'],
            'date_of_marriage':request.POST['date_of_marriage'],
            'worde_about_marriyo':request.POST['worde_about_marriyo'],
            'image_videous':str(image_list)
            }
            print(data)
            happy_list= serializer.happy_list_Serializer(data=data)
            if happy_list.is_valid():
                happy_list.save()
                print("valid data")
                return Response(id, status=status.HTTP_200_OK)

    except:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def happy_couples_all(request):
    try:
        if request.method == 'GET':
            alldata=serializer.happy_couples.objects.all()
            # print(alldata)
            alldataserializer = serializer.happy_couple_Serializer(alldata,many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)
    except:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST','GET'])
def happy_couples_one(request,id):
    try:
        if "groom_id" in request.POST:
           print(request.POST)
        alldata=serializer.happy_couples.objects.filter(groom_id = id).values()
        # for x in alldata:
        #     print(x)
        # return JsonResponse(x)
        alldataserializer = serializer.happy_couple_Serializer(alldata,many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)
                
            # onedata=serializer.happy_couples.objects.get(groom_id=request.POST['groom_id'])
            # print(onedata)
            # return JsonResponse(onedata)
            #     alldataserializer = serializer.happy_couple_Serializer(onedata,many=True)
            # return Response(data=alldataserializer.data, status=status.HTTP_200_OK)
            
    except:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST','GET'])
def saved_search(request,id):
    try:
        my=serializer.ProfileFinder.objects.filter(uid=id).values()
        # print(my[0])
        #find gender
        if my[0]['gender'] == "female":
           print("female")
           alldata = serializer.ProfileFinder.objects.filter(gender = "male").values()
           
        elif my[0]['gender'] == "male":
            print("male")
            alldata = serializer.ProfileFinder.objects.filter(gender = "female").values()
        # print(alldata)
        if request.method == "POST":
            print(request.POST)
            if "tag" in request.POST:
                matc={
                        'my_id':id,
                        'tag':request.POST['tag'],
                        'country':request.POST['country'],
                        'city':request.POST['city'],
                        'age':int(request.POST['age']),
                        'complexion':str(request.POST.getlist('complexion')),
                        'gender':request.POST['gender'],
                        'denomination':request.POST['denomination']
                    }
                print(matc)
                p = []
                for x in alldata:
                    print(type(matc['age']))
                    print(type(x['age']))
                    # if matc['a'] == x['marital_status'] :
                    #     a = x['uid']
                    # elif matc['a'] == "":
                    #     a = ""
                    # else:
                    #     a = "no"
                    if matc['country'] == x['r_country']:
                        b = x['uid']
                    elif matc['country'] == "":
                        b = ""
                    else:
                        b = "no"
                    if matc['city'] == x['r_state'] :
                        c = x['uid']
                    elif matc['city'] == "":
                        c = ""
                    else:
                        c = "no"
                    if matc['age'] == x['age']:
                        d = x['uid']
                    elif matc['age'] == "":
                        d = ""
                    else:
                        d = "no"
                    if matc['complexion'] in x['complexion']:
                        e = x['uid']
                        print("complexionyes")
                    elif matc['complexion'] == "[]":
                        e = ""
                    else:
                        e = "no"
                        print("complexionno")
                    if matc['gender'] == x['gender']:
                        f = x['uid']
                    elif matc['gender'] == "":
                        f = ""
                    else:
                        f = "no"
                    if matc['denomination'] == x['denomination']:
                        g = x['uid']
                    elif matc['denomination'] == "":
                        g = ""
                    else:
                        g = "no"
                    # if matc['h'] in x['are_you_working_now']:
                    #     h = x['uid']
                    # elif matc['h'] == "":
                    #     h = ""
                    # else:
                    #     h = "no"
                    pref = {b,c,d,e,f,g}
                    print(pref)
                    if "no" not in pref:
                        pref.remove("")
                        for con in pref:
                           p.append(con)
                           print(p)
                    # else:
                    #     pref.remove("")
                    #     print(pref)
                print(p)
                        
                # my_preference=[]
                # userlist=[]
                # for y in alldata:
                #     userlist.append(y['uid'])
                # print(userlist)
                # for x in p:
                #     # print(x)
                #     numb = userlist.index(x)
                #     print(numb)
                #     get_Selected = alldata[numb]
                #     my_preference.append(get_Selected)
                # print(my_preference)
                matc_final={
                        'my_id':id,
                        'tag':request.POST['tag'],
                        'country':request.POST['country'],
                        'city':request.POST['city'],
                        'age':int(request.POST['age']),
                        'complexion':str(request.POST.getlist('complexion')),
                        'gender':request.POST['gender'],
                        'denomination':request.POST['denomination'],
                        'filterd_data':str(p)
                    }
                # saved_me_list = serializer.saved_Serializer(
                # instance=saved_me_userdata, data=matc, partial=True)
                saved_me_list= serializer.saved_list_Serializer(data=matc_final)
                if saved_me_list.is_valid():
                    saved_me_list.save()
                    print("valid data")
                    return Response({"valid Data"}, status=status.HTTP_200_OK)
                else:
                    return Response({"Bad Request"}, status=status.HTTP_403_FORBIDDEN)
            elif "tag_edit" in request.POST:
                print(request.POST)
                matc_edit={
                        'my_id':id,
                        'tag':request.POST['tag_edit'],
                        'country':request.POST['country'],
                        'city':request.POST['city'],
                        'age':int(request.POST['age']),
                        'complexion':str(request.POST.getlist('complexion')),
                        'gender':request.POST['gender'],
                        'denomination':request.POST['denomination']
                    }
                print(matc_edit)
                p = []
                for x in alldata:
                    print(type(matc_edit['age']))
                    print(type(x['age']))
                    # if matc_edit['a'] == x['marital_status'] :
                    #     a = x['uid']
                    # elif matc_edit['a'] == "":
                    #     a = ""
                    # else:
                    #     a = "no"
                    if matc_edit['country'] == x['r_country']:
                        b = x['uid']
                    elif matc_edit['country'] == "":
                        b = ""
                    else:
                        b = "no"
                    if matc_edit['city'] == x['r_state'] :
                        c = x['uid']
                    elif matc_edit['city'] == "":
                        c = ""
                    else:
                        c = "no"
                    if matc_edit['age'] == x['age']:
                        d = x['uid']
                    elif matc_edit['age'] == "":
                        d = ""
                    else:
                        d = "no"
                    if matc_edit['complexion'] in x['complexion']:
                        e = x['uid']
                        print("complexionyes")
                    elif matc_edit['complexion'] == "[]":
                        e = ""
                    else:
                        e = "no"
                        print("complexionno")
                    if matc_edit['gender'] == x['gender']:
                        f = x['uid']
                    elif matc_edit['gender'] == "":
                        f = ""
                    else:
                        f = "no"
                    if matc_edit['denomination'] == x['denomination']:
                        g = x['uid']
                    elif matc_edit['denomination'] == "":
                        g = ""
                    else:
                        g = "no"
                    # if matc_edit['h'] in x['are_you_working_now']:
                    #     h = x['uid']
                    # elif matc_edit['h'] == "":
                    #     h = ""
                    # else:
                    #     h = "no"
                    pref = {b,c,d,e,f,g}
                    print(pref)
                    if "no" not in pref:
                        pref.remove("")
                        for con in pref:
                           p.append(con)
                           print(p)
                    # else:
                    #     pref.remove("")
                    #     print(pref)
                print(p)

                        
                # my_preference=[]
                # userlist=[]
                # for y in alldata:
                #     userlist.append(y['uid'])
                # print(userlist)
                # for x in p:
                #     # print(x)
                #     numb = userlist.index(x)
                #     print(numb)
                #     get_Selected = alldata[numb]
                #     my_preference.append(get_Selected)
                # print(my_preference)
                my=serializer.saved_search.objects.get(id=request.POST['id'])
                my.tag=matc_edit['tag']
                my.country=matc_edit['country']
                my.city=matc_edit['city']
                my.age=matc_edit['age']
                my.complexion=matc_edit['complexion']
                my.gender=matc_edit['gender']
                my.denomination=matc_edit['denomination']
                my.filterd_data = str(p)
                my.save()
                print(my)
            elif "remove" in request.POST:
                print(request.POST)
                my=serializer.saved_search.objects.get(id=request.POST['remove'])
                my.delete()

                
    except:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)
    
    finally:
        my_saved=serializer.saved_search.objects.filter(my_id=id).values() 
        # print(my_saved)     
        rec_dict = {}
        rec_list = []
        for x in my_saved:
            # rec = {}
            # rec['received_uid'] = x
            rec_list.append(x)
        rec_dict[id] = rec_list 
        # print(rec_dict)
        return JsonResponse(rec_dict)  

@api_view(['POST','GET'])
def my_investigator(request,id):
    try:
        if request.method == 'GET':
            alldata=serializer.ProfileFinder.objects.filter(uid=id).values()[0]
            jsonDec = json.decoder.JSONDecoder()

            
            # gender = alldata[0]['gender']
            # requestdataa = serializer.sender_list.objects.filter(sender_uid = id)
            # requestdata = serializer.sender_list.objects.filter(sender_uid = id).values()
            # received = requestdata[0]['received_uid']
            # print(received)
            my_investigator_id = alldata['my_investigator']
            print(my_investigator_id)
            
            if str(my_investigator_id) == "None":
                print("none")
                request_sent= ""
                # print(request_sent)
                rec_dict = {}
                rec_dict[id] = request_sent 
                # print(rec_dict)
            else:
                print("something else")
                received_uid_list = my_investigator_id[1:-2].replace("'","").replace(" ","").split(",")
                print(received_uid_list)
                allinvestigator_users=pi_serializer.private_investigator.objects.all().values()
                # print(allinvestigator_users)
                # find uid position
                investigators_id=[]
                #requested sent
                request_sent = []
                for y in allinvestigator_users:
                    investigators_id.append(y['uid'])
                print(investigators_id)
                for i,x in enumerate(received_uid_list):
                    numb = investigators_id.index(x)
                    # print(numb)
                    #find position 
                    find_pos = received_uid_list.index(x)
                    find_ans = jsonDec.decode(alldata['answer'])                    
                    print(find_pos)
                    print(find_ans[find_pos])
                    #percentage
                    total_length = len(find_ans[find_pos])
                    completed_length = []
                    for x in find_ans[find_pos]:
                        if "empty" != x:
                           completed_length.append(x)
                    total_percent = len(completed_length)/(total_length)*100
                    print(total_percent)
                    get_Selected = allinvestigator_users[numb]
                    get_Selected['percentage'] = int(total_percent)
                    request_sent.append(get_Selected)
                    # print(request_sent)
              
                rec_dict = {}
                rec_list = []
                for x in request_sent:
                    # rec = {}
                    # rec['received_uid'] = x
                    rec_list.append(x)
                rec_dict[id] = rec_list 
            # print(rec_dict)
            # # print(requestdata[0]['action'][1:-2].replace("'","").replace(" ","").split(","))
            return JsonResponse(rec_dict)
            # # requestdataserializer = serializer.SenderSerializer(requestdataa,many=True)
            # # return Response(data=requestdataserializer.data, status=status.HTTP_200_OK)


        if request.method == "POST":
            Questina=[]
            answera=[]
            print(request.POST)
            userdataa =  serializer.ProfileFinder.objects.filter(uid=request.POST['pf_id']).values()[0]
            # print(type(userdataa.my_client))
            print(str(userdataa["my_investigator"]))
            userdata = serializer.ProfileFinder.objects.get(uid=request.POST['pf_id'])
            print(userdata)
    #neww
            if  userdataa["my_investigator"] is None:
                print("new")
                Questina.append(("empty".split()))
                answera.append(("empty".split()))
                print(Questina)
                print(answera)
                data={
                'my_investigator':str(request.POST["pi_id"].split()),
                'rating':str("empty".split()),
                'feedback':str("empty".split()),
                'Questin':json.dumps(Questina),
                'answer':json.dumps(answera),
            }
   #replace 
            # elif request.POST["pi_id"] in userdataa["my_investigator"]:
            #     print("replace")
            #     replace = userdataa["my_investigator"][1:-2].replace("'","").replace(" ","").split(",")
            #     rating = userdataa["rating"][1:-2].replace("'","").replace(" ","").split(",")
            #     feedback = userdataa["feedback"][1:-2].replace("'","").replace(" ","").split(",")
            #     position = replace.index(request.POST["pi_id"])
            #     print(position)
            #     replace[position] = request.POST["pi_id"]
                
            #     data={
            #         'my_investigator':str(replace),
            #         'rating':str(rating),
            #         'feedback':str(feedback),
            # }
    #adding
            else:
                print("Add")
                jsonDec = json.decoder.JSONDecoder()
                add = userdataa["my_investigator"][1:-2].replace("'","").replace(" ","").split(",")
                rating = userdataa["rating"][1:-2].replace("'","").replace(" ","").split(",")
                feedback = userdataa["feedback"][1:-2].replace("'","").replace(" ","").split(",")
                Questin = jsonDec.decode(userdataa["Questin"])
                answer = jsonDec.decode(userdataa["answer"])
                print(Questin)
                print(answer)
                add.append(request.POST["pi_id"])
                rating.append("empty")
                feedback.append("empty")
                Questin.append(("empty".split()))
                answer.append(("empty".split()))
                data={
                    'my_investigator':str(add),
                    'rating':str(rating),
                    'feedback':str(feedback),
                    'Questin':json.dumps(Questin),
                    'answer':json.dumps(answer),
            }
            print(data)
            myclientserializer = serializer.my_investigator_serializer(
                instance=userdata, data=data, partial=True)
            if myclientserializer.is_valid():
                myclientserializer.save()
                print("Valid Data")
            
                return Response(id, status=status.HTTP_200_OK)

        else:
            return Response({"sserializer issue"}, status=status.HTTP_403_FORBIDDEN)
    except:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST','GET'])
def my_question_and_Answer(request,id):
    try:
        if request.method == 'GET':
            alldata=serializer.ProfileFinder.objects.filter(uid=id).values()[0]
            if str(alldata['Questin']) == "None":
                print("none")
                request_sent= ""
                # print(request_sent)
                rec_dict = {}
                rec_dict[id] = request_sent 
        
            else:
                print("something else")
                print(alldata['Questin'][1:-2].replace("'",""))
                convert = alldata['Questin'][1:-2].replace("'","").split(",")
                #dictionary
                Qus_and_answer_list=[]
                #converted to list
                convert_qus = alldata['Questin'][1:-2].replace("'","").split(",")
                convert_ans = alldata['answer'][1:-2].replace("'","").split(",")
                # print(alldata['answer'][1:-1].replace("'","").split(","))
                print(convert_ans)
                
                for x in range(0,len(convert_qus)):
                    Qus_and_answer={}
                    # print(convert_ans[x].strip())
                    # print(convert_qus[1:-2].replace("'",""))
                    Qus_and_answer['question'] = convert_qus[x].strip()
                    Qus_and_answer['answer'] = convert_ans[x].strip()
                    Qus_and_answer_list.append(Qus_and_answer)
                # print(Qus_and_answer_list)

                request_sent = convert
                
                rec_dict = {}
                rec_list = []
                for x in Qus_and_answer_list:
                    # rec = {}
                    # rec['received_uid'] = x
                    rec_list.append(x)
                rec_dict[id] = rec_list 
            return JsonResponse(rec_dict)


        if request.method == "POST":
            
            jsonDec = json.decoder.JSONDecoder()
            userdataa =  serializer.ProfileFinder.objects.filter(uid=id).values()[0]
            userdata =  serializer.ProfileFinder.objects.get(uid=id)
            # print(userdata)
            qus=[]
            ans=[]
            if "Questin" in request.POST:
                print("question")
                print(request.POST)
                print(userdataa["my_investigator"])
                qus_raised_investigator_pos = userdataa["my_investigator"][1:-1].replace("'","").replace(" ","").split(",").index(request.POST['my_investigator'])
                print(qus_raised_investigator_pos)
                my_question = jsonDec.decode(userdataa["Questin"])
                my_answer = jsonDec.decode(userdataa["answer"])
                separate_value=my_question[qus_raised_investigator_pos]
                separate_value_ans = my_answer[qus_raised_investigator_pos]
                print(separate_value)
                if "empty" in separate_value:
                    print("empty value")
                    separate_value.remove("empty")
                    separate_value_ans.remove("empty")
                    separate_value.append(request.POST['Questin'])
                    separate_value_ans.append("empty")
                else:
                    print("no")
                    separate_value.append(request.POST['Questin'])
                    separate_value_ans.append("empty")
                print(separate_value)
                my_question[qus_raised_investigator_pos] = separate_value
                my_answer[qus_raised_investigator_pos] = separate_value_ans 
                print(my_question)
                # add_qus = userdataa["Questin"][1:-1].replace("'","").split(",")
                # add_ans = userdataa["answer"][1:-1].replace("'","").split(",")
                # for i,x in enumerate(add_qus):
                #     add_qus[i] = x.strip()
                # add_qus.append(request.POST["Questin"])
                # add_ans.append("empty")
                data={
                    'Questin':json.dumps(my_question),
                    'answer': json.dumps(my_answer),
                }
                print(data)
                # if userdataa["Questin"] == None:
                #     print("new")
                #     qus.append(request.POST['Questin'])
                #     ans.append("empty")
                #     data={
                #         'Questin' : str(qus),
                #         'answer': str(ans),
                #     }
                # else:
                #     print("Add")
                #     print(userdataa["Questin"])
                #     add_qus = userdataa["Questin"][1:-1].replace("'","").split(",")
                #     add_ans = userdataa["answer"][1:-1].replace("'","").split(",")
                #     # for i,x in enumerate(add_qus):
                #     #     add_qus[i] = x.strip()
                #     add_qus.append(request.POST["Questin"])
                #     add_ans.append("empty")
                #     print(add_ans)
                #     data={
                #         'Questin':str(add_qus),
                #         'answer': str(add_ans),
                # }
                # print(data)
                
            elif "answer" in request.POST:
                print("answer")
                print(request.POST)
                qus_raised_investigator_pos = userdataa["my_investigator"][1:-1].replace("'","").replace(" ","").split(",").index(request.POST['my_investigator'])
                print(qus_raised_investigator_pos)
                #allvalue
                Questin = jsonDec.decode(userdataa["Questin"])
                answer = jsonDec.decode(userdataa["answer"])
                #separate value by investigator
                add_qus = jsonDec.decode(userdataa["Questin"])[qus_raised_investigator_pos]
                add_ans = jsonDec.decode(userdataa["answer"])[qus_raised_investigator_pos]
                print(add_qus.index(request.POST['question']))
                #replace answer
                add_qus[add_qus.index(request.POST['question'])] = request.POST['question']
                add_ans[add_qus.index(request.POST['question'])] = request.POST['answer']
                Questin[qus_raised_investigator_pos] = add_qus
                answer[qus_raised_investigator_pos] = add_ans
                print(add_qus)
                print(add_ans)
                data={
                        'Questin':json.dumps(Questin),
                        'answer': json.dumps(answer),
                }
                print(data)
            myqus = serializer.my_question_and_answer(
                instance=userdata, data=data, partial=True)
            if myqus.is_valid():
                myqus.save()
                print("Valid Data")
                return Response(id, status=status.HTTP_200_OK)
        else:
            return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)

    except:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST','GET'])
def ratings_feedback(request,id):
    try:
        if request.method=="POST":
            print(request.POST)
            userdataa =  serializer.ProfileFinder.objects.filter(uid=id).values()[0]
            userdata =  serializer.ProfileFinder.objects.get(uid=id)
            print("replace")
            investigator = userdataa["my_investigator"][1:-1].replace("'","").split(",")
            for i,x in enumerate(investigator):
                    investigator[i] = x.strip() 
            print(investigator)
            find_pos = investigator.index(request.POST['investigator_uid'])
            print(find_pos)
            if 'rating' not in request.POST:
                feedback = userdataa["feedback"][1:-1].replace("'","").split(",")
                rating = userdataa["rating"][1:-1].replace("'","").split(",")
                feedback[find_pos] = request.POST['feedback']
                rating[find_pos] = 0
                print(feedback)
                print(rating)
            else:
                feedback = userdataa["feedback"][1:-1].replace("'","").split(",")
                rating = userdataa["rating"][1:-1].replace("'","").split(",")
                feedback[find_pos] = request.POST['feedback']
                rating[find_pos] = float(request.POST['rating'])
                print(feedback)
                print(rating)
            data={
                    'feedback':str(feedback),
                    'rating': str(rating),
            }
            print(data)
            print(request.POST['investigator_uid'])
            #pi ratings
            pi_id = request.POST['investigator_uid']
            pidata =  models.private_investigator.objects.get(uid=pi_id)
            pidataa =  models.private_investigator.objects.filter(uid=pi_id).values()[0]
            print(pidataa['all_ratings'])
            investigator = pidataa["my_client"][1:-1].replace("'","").split(",")
            for i,x in enumerate(investigator):
                    investigator[i] = x.strip() 
            print(investigator)
            find_poss = investigator.index(id)
            print(find_pos)
            allrating = pidataa['all_ratings'][1:-1].replace("'","").split(",")
            for i,x in enumerate(allrating):
                    allrating[i] = x.strip() 
            print(allrating)
            allrating[find_poss] = str(float(request.POST['rating']))
            print(allrating)
            #total ratings
            total_r = []
            one=[]
            two=[]
            three=[]
            four=[]
            five=[]
            
            
            for j in allrating:
                if "empty" != j:
                    print(j)
                    if j == "1.0":
                        one.append(j)
                    elif j == "2.0":
                        two.append(j)
                    elif j == "3.0":
                        three.append(j)
                    elif j == "4.0":
                        four.append(j)
                    elif j== "5.0":
                        five.append(j)
            print(one)
            print(two)
            print(three)
            print(four)
            print(five)
            score_total = len(five)*5 + len(four) * 4 + len(three) * 3 + len(two) * 2 + len(one) * 1
            response_total = len(five)+ len(four) + len(three) + len(two)+len(one)
            total_ratings = score_total/response_total
            print(score_total)
            print(response_total)
                
                
        
            datab={
                'all_ratings':str(allrating),
                'total_ratings':int(total_ratings)
            }
            print(datab)

            
            myrating = serializer.feedback_and_rating(
                instance=userdata, data=data, partial=True)
            allrating = pi_serializer.all_ratings_serializer(
                instance=pidata, data=datab, partial=True)
            if myrating.is_valid() and allrating.is_valid():
                myrating.save()
                allrating.save()
                print("Valid Data")
                return Response(id, status=status.HTTP_200_OK)
                
            else:
                return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)

    except:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def my_manager(request,id):
    try:
        if request.method == "POST":
            print(request.POST)
            userdataa =  serializer.ProfileFinder.objects.filter(uid=request.POST['pf_id']).values()[0]
            # print(type(userdataa.my_client))
            print(str(userdataa["my_manager"]))
            userdata = serializer.ProfileFinder.objects.get(uid=request.POST['pf_id'])
            print(userdata)
    #neww
            if  userdataa["my_manager"] is None:
                print("new")
                data={
                'my_manager':json.dumps(request.POST["pm_id"].split()),
                'complaints':json.dumps("empty".split()),
                'complaints_replay':json.dumps("empty".split()),
            }
   #replace 
            # elif request.POST["pi_id"] in userdataa["my_investigator"]:
            #     print("replace")
            #     replace = userdataa["my_investigator"][1:-2].replace("'","").replace(" ","").split(",")
            #     rating = userdataa["rating"][1:-2].replace("'","").replace(" ","").split(",")
            #     feedback = userdataa["feedback"][1:-2].replace("'","").replace(" ","").split(",")
            #     position = replace.index(request.POST["pi_id"])
            #     print(position)
            #     replace[position] = request.POST["pi_id"]
                
            #     data={
            #         'my_investigator':str(replace),
            #         'rating':str(rating),
            #         'feedback':str(feedback),
            # }
    #adding
            else:
                print("Add")
                jsonDec = json.decoder.JSONDecoder()
                add = jsonDec.decode(userdataa["my_manager"])
                complaints = jsonDec.decode(userdataa["complaints"])
                complaints_replay = jsonDec.decode(userdataa["complaints_replay"])
                print(complaints)
                add.append(request.POST["pm_id"])
                complaints.append("empty")
                complaints_replay.append("empty")
                data={
                    'my_manager':json.dumps(add),
                    'complaints':json.dumps(complaints),
                    'complaints_replay':json.dumps(complaints_replay),
            }
            print(data)
            myclientserializer = serializer.my_manager_serializer(
                instance=userdata, data=data, partial=True)
            if myclientserializer.is_valid():
                myclientserializer.save()
                print("Valid Data")
            
                return Response(id, status=status.HTTP_200_OK)

        else:
            return Response({"sserializer issue"}, status=status.HTTP_403_FORBIDDEN)
    except:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def my_complaints(request,id):
    try:
        
        if request.method == "POST":
            
            jsonDec = json.decoder.JSONDecoder()
            userdataa =  serializer.ProfileFinder.objects.filter(uid=id).values()[0]
            userdata =  serializer.ProfileFinder.objects.get(uid=id)
            # print(userdata)
            qus=[]
            ans=[]
            if "complaints" in request.POST:
                print("complaints")
                print(request.POST)
                print(userdataa["my_manager"])
                qus_raised_investigator_pos = jsonDec.decode(userdataa["my_manager"]).index(request.POST['my_manager'])
                print(qus_raised_investigator_pos)
                complaints = jsonDec.decode(userdataa["complaints"])
                complaints_replay = jsonDec.decode(userdataa["complaints_replay"])
                separate_value=complaints[qus_raised_investigator_pos]
                separate_value_ans = complaints_replay[qus_raised_investigator_pos]
                print(separate_value)
                print(separate_value_ans)
                if "empty" in separate_value:
                    print("empty value")
                    # separate_value.remove("empty")
                    # separate_value_ans.remove("empty")
                    separate_value = request.POST['complaints']
                    separate_value_ans = "empty"
                else:
                    print("no")
                    separate_value = request.POST['complaints']
                    separate_value_ans = "empty"
                print(separate_value)
                complaints[qus_raised_investigator_pos] = separate_value
                complaints_replay[qus_raised_investigator_pos] = separate_value_ans 
                print(complaints)
                # add_qus = userdataa["Questin"][1:-1].replace("'","").split(",")
                # add_ans = userdataa["answer"][1:-1].replace("'","").split(",")
                # for i,x in enumerate(add_qus):
                #     add_qus[i] = x.strip()
                # add_qus.append(request.POST["Questin"])
                # add_ans.append("empty")
                data={
                    'complaints':json.dumps(complaints),
                    'complaints_replay': json.dumps(complaints_replay),
                }
                print(data)
               
            elif "complaints_replay" in request.POST:
                print("complaints_replay")
                print(request.POST)
                qus_raised_investigator_pos = jsonDec.decode(userdataa["my_manager"]).index(request.POST['my_manager'])
                print(qus_raised_investigator_pos)
                #allvalue
                complaints = jsonDec.decode(userdataa["complaints"])
                complaints_replay = jsonDec.decode(userdataa["complaints_replay"])
                #separate value by investigator
                add_qus = jsonDec.decode(userdataa["complaints"])[qus_raised_investigator_pos]
                add_ans = jsonDec.decode(userdataa["complaints_replay"])[qus_raised_investigator_pos]
                # print(add_qus.index(request.POST['pf_complaints']))
                #replace answer
                print(add_qus)
                # add_qus[add_qus.index(request.POST['pf_complaints'])] = request.POST['pf_complaints']
                # add_ans[add_qus.index(request.POST['pf_complaints'])] = request.POST['complaints_replay']
                # complaints[qus_raised_investigator_pos] = add_qus
                complaints_replay[qus_raised_investigator_pos] =  request.POST['complaints_replay']
                print(add_qus)
                print(add_ans)
                data={
                        'complaints':json.dumps(complaints),
                        'complaints_replay': json.dumps(complaints_replay),
                }
                print(data)
            myqus = serializer.complaints_and_complaints_replay(
                instance=userdata, data=data, partial=True)
            if myqus.is_valid():
                myqus.save()
                print("Valid Data")
                return Response(id, status=status.HTTP_200_OK)
        else:
            return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)

    except:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)


