from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,JsonResponse

from apiapp import models
from virtualExpert import hm_serializer
from virtualExpert.models import hiringmanager,Profilemanager,salesmanager,affliate_marketing,ad_distributor,ad_provider,users
from virtualExpert.hm_serializer import upload_acc_Serializer
from virtualExpert import hm_extension

from rest_framework.decorators import api_view,renderer_classes,permission_classes
from rest_framework.response import Response
from rest_framework import status,generics

from django.core.files.storage import FileSystemStorage
from django.db.models import Q
import requests
import json
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated,AllowAny
import datetime
import yagmail


jsondec = json.decoder.JSONDecoder()
# Create your views here.
all_image_url = "http://127.0.0.1:3000/"
@api_view(['POST'])
def hm_signup(request):
    try:
        try:
            if hm_extension.validate_email(request.data['email']):
                return Response("User Already Exists", status=status.HTTP_302_FOUND)
            else:
                x = datetime.datetime.now()
                datas = {
                    'email': request.data["email"],
                    'mobile': request.data["mobile"],
                    'password': request.data["password"],
                    'first_name': request.POST['first_name'],
                    'last_name': request.POST['last_name'],
                    'uid': hm_extension.id_generate(),
                    'otp': hm_extension.otp_generate(),
                    'created_date':str(x.strftime("%d"))+" "+str(x.strftime("%B"))+","+str(x.year)
                }
                print(datas)
                dataserializer = hm_serializer.SignupSerializer(data=datas)
                print(datas['uid'])
                if dataserializer.is_valid():
                    dataserializer.save()
                    print("Valid Data")
                    hm_extension.send_mail(datas['email'], datas['otp'])
                    print("Email send")
                    return Response(datas['uid'], status=status.HTTP_200_OK)
                else:
                    return Response({"Bad Request"}, status=status.HTTP_403_FORBIDDEN)
        except:
            return Response({"Invalid Json Format (OR) Invalid Key"}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({"Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def hm_otp(request, id):
    try:
        try:
            if hm_extension.validate_otp(id, int(request.data['user_otp'])):
                try:
                    userSpecificData = hiringmanager.objects.get(uid=id)
                    print(userSpecificData)
                    serializer_validate = hm_serializer.OTPSerializer(
                        instance=userSpecificData, data=request.data, partial=True)
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
def hm_signin(request):
    try:
        try:
            if hm_extension.validate_email(request.data['email']):
                if hm_extension.verify_user(request.data['email'], request.data['password']):
                    if hm_extension.verify_user_otp(request.data['email']):
                        return Response(hm_extension.get_user_id(request.data['email']), status=status.HTTP_200_OK)
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
def hm_profile_picture(request,id):
    try:
        print(id)
        print(request.FILES['profile_picture'])
        fs = FileSystemStorage()
        userdata = hm_serializer.hiringmanager.objects.get(uid=id)
        
        id_card = str(request.FILES['profile_picture']).replace(" ", "_")
        print(id_card)
        print(id)
        path = fs.save(f"virtual_expert/hiring_manager/{id}/profile_picture/"+id_card, request.FILES['profile_picture'])

        # full_path = "http://54.159.186.219:8000"+fs.url(path)
        full_path = all_image_url+fs.url(path)
        print(full_path)

        data = {          
            'profile_picture': full_path
           
        }

        print(data)
        basicdetailsserializer = hm_serializer.profile_picture_Serializer(
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
def hm_upload_account(request,id):
    # try:
    if request.method=="POST":
        print( "Backend", request.POST)
        # if request.method == "POST":
        image_names = []
        image_list = []
        cert_name=[]
        cert_list=[]
        print(request.POST)
        fs = FileSystemStorage()
        userdata = hiringmanager.objects.get(uid=id)
        # print(userdata)
        if 'personal_city' in request.POST:
            personal_city = request.POST['personal_city']
        else:
            personal_city = "empty"

        if 'office_city' in request.POST:
            office_city = request.POST['office_city']
        else:
            office_city = "empty"
        #degree certificate
        if 'degree_cer' in request.FILES:
            for sav in request.FILES.getlist('degree_cer'): 
                degree_certificate_1 = fs.save(
                            f"virtual_expert/hiring_manager/{id}/degree_certificate/"+sav.name, sav)
                image_names.append(str( degree_certificate_1).replace(" ","_"))
            for iname in image_names:
                path_deg = iname
                image_list.append(all_image_url+fs.url(path_deg))
            degree_cer=str(image_list)
        else:
            degree_cer="empty"
        # Aadhaar 
        if 'aadhaar_card' in request.FILES:
            aadhaar_no = request.POST['aadhaar_no']
            aadhaar_card_1= str(request.FILES['aadhaar_card']).replace(" ", "_")
            path_adhar = fs.save(f"virtual_expert/hiring_manager/{id}/aadhaar_card/"+aadhaar_card_1, request.FILES['aadhaar_card'])
            full_path_aadhaar = all_image_url+fs.url(path_adhar)
        else:
            aadhaar_no = "empty"
            full_path_aadhaar = "empty"
        #  Pan_Card
        if 'pan_card' in request.FILES:
            pan_no = request.POST['pan_no']
            pan_card_1 = str(request.FILES['pan_card']).replace(" ", "_")
            path1 = fs.save(f"virtual_expert/hiring_manager/{id}/pan_card/"+pan_card_1, request.FILES['pan_card'])
            full_path_pan = all_image_url+fs.url(path1)
        else:
            pan_no = "empty"
            full_path_pan = "empty"
        # Driving Licence
        if 'drive_licence' in request.FILES:
            drive_licence_no = request.POST['drive_licence_no']
            drive_licence_date = request.POST['drive_licence_date']
            licence_state = request.POST['licence_state']
            drive_licence_1 = str(request.FILES['drive_licence']).replace(" ", "_")
            path1 = fs.save(f"virtual_expert/hiring_manager/{id}/driving_licence/"+drive_licence_1, request.FILES['drive_licence'])
            full_path_lic = all_image_url+fs.url(path1)
        else:
            drive_licence_no = "empty"
            drive_licence_date = "empty"
            licence_state = "empty"
            full_path_lic = "empty"

        
         # Previous Application Details
            
        if request.POST['past_applied_date'] == '':
            past_applied_date = "empty"
            past_applied_position =  "empty"
        else:
            past_applied_date = request.POST['past_applied_date']
            past_applied_position = request.POST['past_applied_position']
        # Govt Job 
        if request.POST['govtjob_start_date'] == '':
            govtjob_start_date = "empty"
            govtjob_end_date = "empty"
        else:
            govtjob_start_date = request.POST['govtjob_start_date']
            govtjob_end_date = request.POST['govtjob_end_date']
        # notary Licence
        if request.POST['notary_lic_no'] == '':
            notary_lic_no = "empty"
            notary_issued = "empty"
            notary_state = "empty"
        else:
            notary_lic_no = request.POST['notary_lic_no']
            notary_issued = request.POST['notary_issued']
            notary_state = request.POST['notary_state']
            
        if request.POST['judgment_felony'] == '':
            judgment_felony= "empty"
        else:
            judgment_felony = request.POST['judgment_felony']

        #experience certificate
        if 'expr_certi' in request.FILES:
            for sav in request.FILES.getlist('expr_certi'): 
                exp_certificate_1 = fs.save(
                            f"virtual_expert/hiring_manager/{id}/experience_certificate/"+sav.name, sav)
                cert_name.append(str( exp_certificate_1).replace(" ","_"))
                
            for iname in cert_name:
                path_exp = iname
                cert_list.append(all_image_url+fs.url(path_exp))
           
            full_path_ex = str(cert_list)
        else:
            full_path_ex = "empty"

        if request.POST['mariyo_work_type'] == "Personal":
            company_name="empty"
            company_address= "empty"
            gst_number = "empty"
            gst_certificate = "empty"
            company_phone = "empty"
            company_email = "empty"
        else:
            #gst certificate
            gst_certificate_1 = str(request.FILES['gst_certificate']).replace(" ", "_")
            path = fs.save(f"virtual_expert/hiring_manager/{id}/gst_certificate/"+gst_certificate_1, request.FILES['gst_certificate'])
            full_path_gst = all_image_url+fs.url(path)

            gst_number = request.POST['gst_number']
            gst_certificate = full_path_gst
            company_name = request.POST['company_name']
            company_address = request.POST['company_address']
            company_phone = request.POST['company_phone']
            company_email = request.POST['company_email']          
            
        if request.POST['work_job_title'] == '':
            work_job_title = "empty"
        else:
            work_job_title =json.dumps(request.POST.getlist('work_job_title'))
        if request.POST['work_company_name'] == '':
            work_company_name = "empty"
        else:
            work_company_name = json.dumps(request.POST.getlist('work_company_name'))
        if request.POST['work_start_date'] == '':
            work_start_date = "empty"
        else:
            work_start_date = json.dumps(request.POST.getlist('work_start_date'))

        if request.POST['starting_salary'] == '':
            starting_salary = "empty"
        else:
            starting_salary = json.dumps(request.POST.getlist('starting_salary'))

        if request.POST['work_end_date'] == '':
            work_end_date = "empty"
        else:
            work_end_date = json.dumps(request.POST.getlist('work_end_date'))

        if request.POST['final_salary'] == '':
            final_salary = "empty"
        else:
            final_salary = json.dumps(request.POST.getlist('final_salary'))

        if request.POST['reason_leaving'] == '':
            reason_leaving = "empty"
        else:
            reason_leaving =json.dumps(request.POST.getlist('reason_leaving'))

        if request.POST['work_review_y'] == '':
            work_review_y = "empty"
        else:
            work_review_y =json.dumps(request.POST.getlist('work_review_y'))

        if request.POST['skills'] == '':
            skills= "empty"
        else:
            skills = json.dumps(request.POST.getlist('skills'))
            
        if request.POST['curent_busines'] == '':
            curent_busines = "empty"
        else:
            curent_busines = request.POST['curent_busines']

        if request.POST['past_business'] == '':
            past_business = "empty"
        else:
            past_business =request.POST['past_business']

        data = {
            'office_name': request.POST['office_name'],
            'office_country': request.POST['office_country'],
            'office_city': office_city,
            'office_address': request.POST['office_address'],
            # 'first_name': request.POST['first_name'],
            # 'last_name': request.POST['last_name'],
            'personal_country': request.POST['personal_country'],
            'personal_city':personal_city,
            'personal_dob': request.POST['personal_dob'],
            'personal_age': request.POST['personal_age'],
            'house_number' : request.POST['house_number'],
            'street_name' : request.POST['street_name'],
            'pin_code' : request.POST['pin_code'],
            'my_hiring_manager': request.POST['my_hiring_manager'],           
            # 'id_card': full_path

            'aadhaar_no' : aadhaar_no,
            'aadhaar_card': full_path_aadhaar,
            'pan_no':pan_no,
            'pan_card':full_path_pan,
            'drive_licence_no' :drive_licence_no,
            'drive_licence' : full_path_lic,
            'drive_licence_date' :drive_licence_date,
            'licence_state' :licence_state,
            'past_applied_date':past_applied_date,
            'past_applied_position':past_applied_position,
            'govtjob_start_date':govtjob_start_date,
            'govtjob_end_date': govtjob_end_date,
            'judgment_felony' : judgment_felony,
            'notary_lic_no' : notary_lic_no,
            'notary_issued ':notary_issued,
            'notary_state' : notary_state,
            'level_education': json.dumps(request.POST.getlist('level_education')),           
            'field_study': json.dumps(request.POST.getlist('field_study')),
            'school_colege' : json.dumps(request.POST.getlist('school_colege')),
            'completed_year' : json.dumps(request.POST.getlist('completed_year')), 
            'study_location': json.dumps(request.POST.getlist('study_location')),
            'degree_cer' : degree_cer,
            'skills' : skills,
            'work_job_title' : work_job_title,           
            'work_company_name' : work_company_name,
            'work_start_date' : work_start_date,
            'starting_salary' : starting_salary,
            'work_end_date' :  work_end_date,
            'final_salary' : final_salary,
            'reason_leaving' : reason_leaving,
            'work_review_y' :  work_review_y,
            'expr_certi' : full_path_ex,
            'curent_busines' : curent_busines,
            'past_business' : past_business,
            'mariyo_work_type' : request.POST['mariyo_work_type'],
            'company_name' : company_name,
            'company_address' : company_address,
            'company_phone' : company_phone,
            'company_email' : company_email,
            'gst_number' :  gst_number,
            'gst_certificate' : gst_certificate,         
            # 'arn_no': arn_no,                       
        }
        print(notary_issued)
        basicdetailsserializer = hm_serializer.upload_acc_Serializer(
            instance=userdata, data=data, partial=True)
        print(userdata)
        if basicdetailsserializer.is_valid():
            print("validated")
            basicdetailsserializer.save()
            print("Valid Data")
            #hiring manager
            userdata1 = hiringmanager.objects.get(uid= request.POST['my_hiring_manager'])
            hm_data = hiringmanager.objects.filter(uid= request.POST['my_hiring_manager']).values()[0]
            hm_userdata = hiringmanager.objects.filter(uid=id).values()[0]
            
            if hm_data['hiring_manager'] == None:
                hiring_manager = [] 
                print("new")
                hiring_manager.append(hm_userdata)
            else:
                print("add")
                hiring_manager = jsondec.decode(hm_data['hiring_manager'])
                # print(my_profile_add)
                hiring_manager.append(hm_userdata)
            data1={
                'hiring_manager': json.dumps(hiring_manager)
            }
            # print(data1)
            hmdetailsserializer = hm_serializer.hiring_manager_Serializer(
            instance=userdata1, data=data1, partial=True)
            if hmdetailsserializer.is_valid():
                hmdetailsserializer.save()
                print("valid data")
            
            return Response(id, status=status.HTTP_200_OK)
        else:
            print("Problem")
            
            return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
    # except:
    else:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def hm_edit_account(request,id):
    try:
        print(request.POST)
        print(request.FILES)
        fs = FileSystemStorage()
        userdata = hiringmanager.objects.get(uid=id)
        userdataa = hiringmanager.objects.filter(uid=id).values()[0]
        print("userdataa")
        if "profile_picture" in request.FILES:
            id_card = str(request.FILES['profile_picture']).replace(" ", "_")
            path = fs.save(f"virtual_expert/hiring_manager/{id}/profile_picture/"+id_card, request.FILES['profile_picture'])
    
            # full_path = "http://54.159.186.219:8000"+fs.url(path)
            full_path = all_image_url+fs.url(path)
        else:
            full_path = userdataa['profile_picture']

        if 'office_city' in request.POST:
            office_city = request.POST['office_city']
        else:
            office_city = "empty"

        if 'personal_city' in request.POST:
            personal_city = request.POST['personal_city']
        else:
            personal_city = "empty"


        data = {
            'office_name': request.POST['office_name'],
            'office_country': request.POST['office_country'],
            'office_city': office_city,
            'office_address': request.POST['office_address'],
            'first_name': request.POST['first_name'],
            'last_name': request.POST['last_name'],
            'personal_country': request.POST['personal_country'],
            'personal_city': personal_city,
            'personal_address': request.POST['personal_address'],
            # 'notary': request.POST['notary'],           
            'profile_picture': full_path
           
        }

        print(data)
        basicdetailsserializer = hm_serializer.edit_acc_Serializer(
            instance=userdata, data=data, partial=True)
        if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
        else:
            return Response({"sserializer issue"}, status=status.HTTP_403_FORBIDDEN)
    except:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def hm_my_data(request,id):
    if request.method == 'GET':
       allDataa = hm_serializer.hiringmanager.objects.filter(uid=id)
       alldataserializer = hm_serializer.hiringmanagerSerializer(allDataa,many=True)
    return Response(data=alldataserializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def all_hm_data(request):
    if request.method == 'GET':
       allDataa = hm_serializer.hiringmanager.objects.all()
       alldataserializer = hm_serializer.hiringmanagerSerializer(allDataa,many=True)
    return Response(data=alldataserializer.data, status=status.HTTP_200_OK)

#profile_manager_upload_account
@api_view(['POST'])
def profile_manager_upload_account(request,id):
    try:
        print(request.POST)
        print(request.FILES)
        print(id)
        fs = FileSystemStorage()
        userdata = Profilemanager.objects.get(uid=id)
        #id card
        id_card = str(request.FILES['id_card']).replace(" ", "_")
        path_one = fs.save(f"virtual_expert/profile_manager/{id}/id_card/"+id_card, request.FILES['id_card'])

        # full_path = "http://54.159.186.219:8000"+fs.url(path)
        full_path_one = all_image_url+fs.url(path_one)
        #signed Document
        signed = str(request.FILES['sign_document']).replace(" ", "_")
        path_two = fs.save(f"virtual_expert/profile_manager/{id}/signed_document/"+signed, request.FILES['sign_document'])
        # full_path = "http://54.159.186.219:8000"+fs.url(path)
        full_path_two = all_image_url+fs.url(path_two)
        #verification Image
        verification = str(request.FILES['verification_img']).replace(" ", "_")
        path_three = fs.save(f"virtual_expert/profile_manager/{id}/verification_image/"+verification, request.FILES['verification_img'])
        # full_path = "http://54.159.186.219:8000"+fs.url(path)
        verification_img = all_image_url+fs.url(path_three)
        #office
        if 'office_city' in request.POST:
            office_city = request.POST['office_city']
        else:
            office_city = "empty"
        #personal
        if "personal_city" in request.POST:
            city = request.POST['personal_city']
        else:
            city = "None"
        #degree certificate
        try:
            degree_certificate_1 = str(request.FILES['degree_cer']).replace(" ", "_")
            path_deg = fs.save(f"virtual_expert/profile_manager/{id}/degree_certificate/"+degree_certificate_1, request.FILES['degree_cer'])
            full_path_degree = all_image_url+fs.url(path_deg)
        except:
            full_path_degree = userdata.degree_cer
         #experience certificate
        
        try:
            ex_certificate_1 = str(request.FILES['ex_cer']).replace(" ", "_")
            path_ex = fs.save(f"virtual_expert/profile_manager/{id}/experience_certificate/"+ex_certificate_1, request.FILES['ex_cer'])
            full_path_ex = all_image_url+fs.url(path_ex)
        except:
            full_path_ex = userdata.ex_cer
        #type
        if request.POST['work_type'] == "Personal":
            gst_number = "empty"
            gst_certificate = "empty"
            company_pan_no = "empty"
            arn_no = "empty"
            pan_card = "empty"
        else:
            #gst certificate
            try:
                gst_certificate_1 = str(request.FILES['gst_certificate']).replace(" ", "_")
                path = fs.save(f"virtual_expert/profile_manager/{id}/gst_certificate/"+gst_certificate_1, request.FILES['gst_certificate'])
                full_path_gst = all_image_url+fs.url(path)
            except:
                full_path_gst = userdata.gst_certificate
            #pan card
            try:
                pan_card_1 = str(request.FILES['pan_card']).replace(" ", "_")
                path1 = fs.save(f"virtual_expert/profile_manager/{id}/pan_card/"+pan_card_1, request.FILES['pan_card'])
                full_path_pan = all_image_url+fs.url(path1)
            except:
                full_path_pan = userdata.pan_card
            #############
            gst_number = request.POST['gst_number']
            gst_certificate = full_path_gst
            company_pan_no = request.POST['company_pan_no']
            arn_no = request.POST['arn_no']
            pan_card = full_path_pan
        #work
        if request.POST['work_job_title'] == '':
            work_job_title = "empty"
        else:
            work_job_title = request.POST['work_job_title']
        if request.POST['work_company_name'] == '':
            work_company_name = "empty"
        else:
            work_company_name = request.POST['work_company_name']
        if request.POST['work_job_location'] == '':
            work_job_location = "empty"
        else:
            work_job_location = request.POST['work_job_location']
        if request.POST['ex_job_title'] == '':
            ex_job_title = "empty"
        else:
            ex_job_title =request.POST['ex_job_title']
        if request.POST['ex_company_name'] == '':
            ex_company_name = "empty"
        else:
            ex_company_name =request.POST['ex_company_name']
        if request.POST['year_experience'] == '':
            year_experience = "empty"
        else:
            year_experience =request.POST['year_experience']
        if request.POST['ex_location'] == '':
            ex_location = "empty"
        else:
            ex_location =request.POST['ex_location']
        print("helo")
        data = {
            'office_name': request.POST['office_name'],
            'office_country': request.POST['office_country'],
            'office_city': office_city,
            'office_address': request.POST['office_address'],  
            'first_name': request.POST['first_name'],
            'last_name': request.POST['last_name'],
            'personal_country': request.POST['personal_country'],
            'personal_city': city,
            'personal_address': request.POST['personal_address'],
            'level_education': json.dumps(request.POST.getlist('level_education')),           
            'field_study': json.dumps(request.POST.getlist('field_study')),           
            'work_job_title': work_job_title,           
            'work_company_name': work_company_name,           
            'work_job_location': work_job_location,           
            'ex_job_title': ex_job_title,           
            'ex_company_name': ex_company_name,           
            'year_experience': year_experience,           
            'ex_location': ex_location,           
            'degree_cer': full_path_degree,           
            'ex_cer': full_path_ex,           
            'work_type': request.POST['work_type'],           
            'gst_number': gst_number,           
            'gst_certificate': gst_certificate,           
            'company_pan_no': company_pan_no,           
            'arn_no': arn_no,           
            'pan_card': pan_card,       
            'id_card': full_path_one,
            'sign_document': full_path_two,
            'verification_img':verification_img   
        }

        print(data)
        basicdetailsserializer = hm_serializer.profile_manager_acc_Serializer(
            instance=userdata, data=data, partial=True)
        if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")

            #hiring manager
            get_uid = Profilemanager.objects.filter(uid=id).values()[0]
            print(get_uid["notary"])
            userdata1 = hiringmanager.objects.get(uid= get_uid["notary"])
            print(userdata1)
            hm_data = hiringmanager.objects.filter(uid= get_uid["notary"]).values()[0]
            # hm_userdata = hiringmanager.objects.filter(uid=id).values()[0]
            print(hm_data['my_profile_manager'])
        
            my_profile_manager = jsondec.decode(hm_data['my_profile_manager']) 
            alter_values = []
            print("new")
            print(get_uid['uid'])
            for x in my_profile_manager:
                if get_uid['uid'] == x['uid']:
                    alter_values.append(get_uid)
                else:
                    alter_values.append(x)
            data1={
                'my_profile_manager': json.dumps(alter_values)
            }
            print(data1)
            hmdetailsserializer = hm_serializer.my_profile_manager_Serializer(
            instance=userdata1, data=data1, partial=True)
            if hmdetailsserializer.is_valid():
                hmdetailsserializer.save()
                print("valid data")
            return Response(id, status=status.HTTP_200_OK)
        else:
            return Response({"sserializer issue"}, status=status.HTTP_403_FORBIDDEN)
    except:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)
    
#aad_provider_upload_account
@api_view(['POST'])
def ad_provider_upload_account(request,id):
    try:
        print(request.POST)
        print(request.FILES)
        fs = FileSystemStorage()
        userdata = ad_provider.objects.get(uid=id)
        id_card = str(request.FILES['id_card']).replace(" ", "_")
        path_one = fs.save(f"virtual_expert/ad_provider/{id}/id_card/"+id_card, request.FILES['id_card'])

        # full_path = "http://54.159.186.219:8000"+fs.url(path)
        full_path_one = all_image_url+fs.url(path_one)
        signed = str(request.FILES['sign_document']).replace(" ", "_")
        path_two = fs.save(f"virtual_expert/ad_provider/{id}/signed_document/"+signed, request.FILES['sign_document'])
        full_path_two = all_image_url+fs.url(path_two)
        #verification Image
        verification = str(request.FILES['verification_img']).replace(" ", "_")
        path_three = fs.save(f"virtual_expert/ad_provider/{id}/verification_image/"+verification, request.FILES['verification_img'])
        # full_path = "http://54.159.186.219:8000"+fs.url(path)
        verification_img = all_image_url+fs.url(path_three)
        #office
        if 'office_city' in request.POST:
            office_city = request.POST['office_city']
        else:
            office_city = "empty"
        #personal
        if "personal_city" in request.POST:
            city = request.POST['personal_city']
        else:
            city = "None"
        #degree certificate
        try:
            degree_certificate_1 = str(request.FILES['degree_cer']).replace(" ", "_")
            path_deg = fs.save(f"virtual_expert/ad_provider/{id}/degree_certificate/"+degree_certificate_1, request.FILES['degree_cer'])
            full_path_degree = all_image_url+fs.url(path_deg)
        except:
            full_path_degree = userdata.degree_cer
         #experience certificate
        
        try:
            ex_certificate_1 = str(request.FILES['ex_cer']).replace(" ", "_")
            path_ex = fs.save(f"virtual_expert/ad_provider/{id}/experience_certificate/"+ex_certificate_1, request.FILES['ex_cer'])
            full_path_ex = all_image_url+fs.url(path_ex)
        except:
            full_path_ex = userdata.ex_cer
        #type
        if request.POST['work_type'] == "Personal":
            gst_number = "empty"
            gst_certificate = "empty"
            company_pan_no = "empty"
            arn_no = "empty"
            pan_card = "empty"
        else:
            #gst certificate
            try:
                gst_certificate_1 = str(request.FILES['gst_certificate']).replace(" ", "_")
                path = fs.save(f"virtual_expert/ad_provider/{id}/gst_certificate/"+gst_certificate_1, request.FILES['gst_certificate'])
                full_path_gst = all_image_url+fs.url(path)
            except:
                full_path_gst = userdata.gst_certificate
            #pan card
            try:
                pan_card_1 = str(request.FILES['pan_card']).replace(" ", "_")
                path1 = fs.save(f"virtual_expert/ad_provider/{id}/pan_card/"+pan_card_1, request.FILES['pan_card'])
                full_path_pan = all_image_url+fs.url(path1)
            except:
                full_path_pan = userdata.pan_card
            #############
            gst_number = request.POST['gst_number']
            gst_certificate = full_path_gst
            company_pan_no = request.POST['company_pan_no']
            arn_no = request.POST['arn_no']
            pan_card = full_path_pan
        #work
        if request.POST['work_job_title'] == '':
            work_job_title = "empty"
        else:
            work_job_title = request.POST['work_job_title']
        if request.POST['work_company_name'] == '':
            work_company_name = "empty"
        else:
            work_company_name = request.POST['work_company_name']
        if request.POST['work_job_location'] == '':
            work_job_location = "empty"
        else:
            work_job_location = request.POST['work_job_location']
        if request.POST['ex_job_title'] == '':
            ex_job_title = "empty"
        else:
            ex_job_title =request.POST['ex_job_title']
        if request.POST['ex_company_name'] == '':
            ex_company_name = "empty"
        else:
            ex_company_name =request.POST['ex_company_name']
        if request.POST['year_experience'] == '':
            year_experience = "empty"
        else:
            year_experience =request.POST['year_experience']
        if request.POST['ex_location'] == '':
            ex_location = "empty"
        else:
            ex_location =request.POST['ex_location']
        print("helo")
        data = {
            'office_name': request.POST['office_name'],
            'office_country': request.POST['office_country'],
            'office_city': office_city,
            'office_address': request.POST['office_address'],  
            'first_name': request.POST['first_name'],
            'last_name': request.POST['last_name'],
            'personal_country': request.POST['personal_country'],
            'personal_city': city,
            'personal_address': request.POST['personal_address'],
            'level_education': json.dumps(request.POST.getlist('level_education')),           
            'field_study': json.dumps(request.POST.getlist('field_study')),           
            'work_job_title': work_job_title,           
            'work_company_name': work_company_name,           
            'work_job_location': work_job_location,           
            'ex_job_title': ex_job_title,           
            'ex_company_name': ex_company_name,           
            'year_experience': year_experience,           
            'ex_location': ex_location,           
            'degree_cer': full_path_degree,           
            'ex_cer': full_path_ex,           
            'work_type': request.POST['work_type'],           
            'gst_number': gst_number,           
            'gst_certificate': gst_certificate,           
            'company_pan_no': company_pan_no,           
            'arn_no': arn_no,           
            'pan_card': pan_card,       
            'id_card': full_path_one,
            'sign_document': full_path_two,
            'verification_img':verification_img
           
        }

        print(data)
        basicdetailsserializer = hm_serializer.ad_provider_acc_Serializer(
            instance=userdata, data=data, partial=True)
        if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")

            #hiring manager
            get_uid = ad_provider.objects.filter(uid=id).values()[0]
            print(get_uid["hiring_manager"])
            userdata1 = hiringmanager.objects.get(uid= get_uid["hiring_manager"])
            print(userdata1)
            hm_data = hiringmanager.objects.filter(uid= get_uid["hiring_manager"]).values()[0]
            # hm_userdata = hiringmanager.objects.filter(uid=id).values()[0]
            print(hm_data['ad_provider'])
        
            ad_providerr = jsondec.decode(hm_data['ad_provider']) 
            alter_values = []
            print("new")
            print(get_uid['uid'])
            for x in ad_providerr:
                if get_uid['uid'] == x['uid']:
                    alter_values.append(get_uid)
                else:
                    alter_values.append(x)
            data1={
                'ad_provider': json.dumps(alter_values)
            }
            print(data1)
            hmdetailsserializer = hm_serializer.ad_provider_Serializer(
            instance=userdata1, data=data1, partial=True)
            if hmdetailsserializer.is_valid():
                hmdetailsserializer.save()
                print("valid data")
            return Response(id, status=status.HTTP_200_OK)
        else:
            return Response({"sserializer issue"}, status=status.HTTP_403_FORBIDDEN)
    except:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)
    
#aad_distributor_upload_account
@api_view(['POST'])
def ad_distributor_upload_account(request,id):
    try:
        print(request.POST)
        print(request.FILES)
        fs = FileSystemStorage()
        userdata = ad_distributor.objects.get(uid=id)
        id_card = str(request.FILES['id_card']).replace(" ", "_")
        path_one = fs.save(f"virtual_expert/ad_distributor/{id}/id_card/"+id_card, request.FILES['id_card'])
        print(userdata)
        # full_path = "http://54.159.186.219:8000"+fs.url(path)
        full_path_one = all_image_url+fs.url(path_one)
        signed = str(request.FILES['sign_document']).replace(" ", "_")
        path_two = fs.save(f"virtual_expert/ad_distributor/{id}/signed_document/"+signed, request.FILES['sign_document'])
        # full_path = "http://54.159.186.219:8000"+fs.url(path)
        full_path_two = all_image_url+fs.url(path_two)

        #verification Image
        verification = str(request.FILES['verification_img']).replace(" ", "_")
        path_three = fs.save(f"virtual_expert/ad_distributor/{id}/verification_image/"+verification, request.FILES['verification_img'])
        # full_path = "http://54.159.186.219:8000"+fs.url(path)
        verification_img = all_image_url+fs.url(path_three)
        #office
        if 'office_city' in request.POST:
            office_city = request.POST['office_city']
        else:
            office_city = "empty"
        #personal
        if "personal_city" in request.POST:
            city = request.POST['personal_city']
        else:
            city = "None"
        #degree certificate
        try:
            degree_certificate_1 = str(request.FILES['degree_cer']).replace(" ", "_")
            path_deg = fs.save(f"virtual_expert/ad_distributor/{id}/degree_certificate/"+degree_certificate_1, request.FILES['degree_cer'])
            full_path_degree = all_image_url+fs.url(path_deg)
        except:
            full_path_degree = userdata.degree_cer
         #experience certificate
        
        try:
            ex_certificate_1 = str(request.FILES['ex_cer']).replace(" ", "_")
            path_ex = fs.save(f"virtual_expert/ad_distributor/{id}/experience_certificate/"+ex_certificate_1, request.FILES['ex_cer'])
            full_path_ex = all_image_url+fs.url(path_ex)
        except:
            full_path_ex = userdata.ex_cer
        #type
        if request.POST['work_type'] == "Personal":
            gst_number = "empty"
            gst_certificate = "empty"
            company_pan_no = "empty"
            arn_no = "empty"
            pan_card = "empty"
        else:
            #gst certificate
            try:
                gst_certificate_1 = str(request.FILES['gst_certificate']).replace(" ", "_")
                path = fs.save(f"virtual_expert/ad_distributor/{id}/gst_certificate/"+gst_certificate_1, request.FILES['gst_certificate'])
                full_path_gst = all_image_url+fs.url(path)
            except:
                full_path_gst = userdata.gst_certificate
            #pan card
            try:
                pan_card_1 = str(request.FILES['pan_card']).replace(" ", "_")
                path1 = fs.save(f"virtual_expert/ad_distributor/{id}/pan_card/"+pan_card_1, request.FILES['pan_card'])
                full_path_pan = all_image_url+fs.url(path1)
            except:
                full_path_pan = userdata.pan_card
            #############
            gst_number = request.POST['gst_number']
            gst_certificate = full_path_gst
            company_pan_no = request.POST['company_pan_no']
            arn_no = request.POST['arn_no']
            pan_card = full_path_pan
        #work
        if request.POST['work_job_title'] == '':
            work_job_title = "empty"
        else:
            work_job_title = request.POST['work_job_title']
        if request.POST['work_company_name'] == '':
            work_company_name = "empty"
        else:
            work_company_name = request.POST['work_company_name']
        if request.POST['work_job_location'] == '':
            work_job_location = "empty"
        else:
            work_job_location = request.POST['work_job_location']
        if request.POST['ex_job_title'] == '':
            ex_job_title = "empty"
        else:
            ex_job_title =request.POST['ex_job_title']
        if request.POST['ex_company_name'] == '':
            ex_company_name = "empty"
        else:
            ex_company_name =request.POST['ex_company_name']
        if request.POST['year_experience'] == '':
            year_experience = "empty"
        else:
            year_experience =request.POST['year_experience']
        if request.POST['ex_location'] == '':
            ex_location = "empty"
        else:
            ex_location =request.POST['ex_location']
        print("helo")
        data = {
            'office_name': request.POST['office_name'],
            'office_country': request.POST['office_country'],
            'office_city': office_city,
            'office_address': request.POST['office_address'],  
            'first_name': request.POST['first_name'],
            'last_name': request.POST['last_name'],
            'personal_country': request.POST['personal_country'],
            'personal_city': city,
            'personal_address': request.POST['personal_address'],
            'level_education': json.dumps(request.POST.getlist('level_education')),           
            'field_study': json.dumps(request.POST.getlist('field_study')),           
            'work_job_title': work_job_title,           
            'work_company_name': work_company_name,           
            'work_job_location': work_job_location,           
            'ex_job_title': ex_job_title,           
            'ex_company_name': ex_company_name,           
            'year_experience': year_experience,           
            'ex_location': ex_location,           
            'degree_cer': full_path_degree,           
            'ex_cer': full_path_ex,           
            'work_type': request.POST['work_type'],           
            'gst_number': gst_number,           
            'gst_certificate': gst_certificate,           
            'company_pan_no': company_pan_no,           
            'arn_no': arn_no,           
            'pan_card': pan_card,       
            'id_card': full_path_one,
            'sign_document': full_path_two,
            'verification_img':verification_img
           
        }

        print(data)
        basicdetailsserializer = hm_serializer.ad_distributor_acc_Serializer(
            instance=userdata, data=data, partial=True)
        if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")

            #hiring manager
            get_uid = ad_distributor.objects.filter(uid=id).values()[0]
            print(get_uid["hiring_manager"])
            userdata1 = hiringmanager.objects.get(uid= get_uid["hiring_manager"])
            print(userdata1)
            hm_data = hiringmanager.objects.filter(uid= get_uid["hiring_manager"]).values()[0]
            # hm_userdata = hiringmanager.objects.filter(uid=id).values()[0]
            print(hm_data['ad_distributor'])
        
            ad_distributorr = jsondec.decode(hm_data['ad_distributor']) 
            alter_values = []
            print("new")
            print(get_uid['uid'])
            for x in ad_distributorr:
                if get_uid['uid'] == x['uid']:
                    alter_values.append(get_uid)
                else:
                    alter_values.append(x)
            data1={
                'ad_distributor': json.dumps(alter_values)
            }
            print(data1)
            hmdetailsserializer = hm_serializer.ad_distributor_Serializer(
            instance=userdata1, data=data1, partial=True)
            if hmdetailsserializer.is_valid():
                hmdetailsserializer.save()
                print("valid data")
            return Response(id, status=status.HTTP_200_OK)
        else:
            return Response({"sserializer issue"}, status=status.HTTP_403_FORBIDDEN)
    except:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)

#sales_upload_account
@api_view(['POST'])
def sales_upload_account(request,id):
    try:
        print(request.POST)
        print(request.FILES)
        fs = FileSystemStorage()
        userdata = salesmanager.objects.get(uid=id)
        id_card = str(request.FILES['id_card']).replace(" ", "_")
        path_one = fs.save(f"virtual_expert/sales_manager/{id}/id_card/"+id_card, request.FILES['id_card'])

        # full_path = "http://54.159.186.219:8000"+fs.url(path)
        full_path_one = all_image_url+fs.url(path_one)
        signed = str(request.FILES['sign_document']).replace(" ", "_")
        path_two = fs.save(f"virtual_expert/sales_manager/{id}/signed_document/"+signed, request.FILES['sign_document'])

        # full_path = "http://54.159.186.219:8000"+fs.url(path)
        full_path_two = all_image_url+fs.url(path_two)
        
        #verification Image
        verification = str(request.FILES['verification_img']).replace(" ", "_")
        path_three = fs.save(f"virtual_expert/sales_manager/{id}/verification_image/"+verification, request.FILES['verification_img'])
        # full_path = "http://54.159.186.219:8000"+fs.url(path)
        verification_img = all_image_url+fs.url(path_three)
        
        #personal
        if "personal_city" in request.POST:
            city = request.POST['personal_city']
        else:
            city = "None"
        #degree certificate
        try:
            degree_certificate_1 = str(request.FILES['degree_cer']).replace(" ", "_")
            path_deg = fs.save(f"virtual_expert/sales_manager/{id}/degree_certificate/"+degree_certificate_1, request.FILES['degree_cer'])
            full_path_degree = all_image_url+fs.url(path_deg)
        except:
            full_path_degree = userdata.degree_cer
         #experience certificate
        
        try:
            ex_certificate_1 = str(request.FILES['ex_cer']).replace(" ", "_")
            path_ex = fs.save(f"virtual_expert/sales_manager/{id}/experience_certificate/"+ex_certificate_1, request.FILES['ex_cer'])
            full_path_ex = all_image_url+fs.url(path_ex)
        except:
            full_path_ex = userdata.ex_cer
        #type
        if request.POST['work_type'] == "Personal":
            gst_number = "empty"
            gst_certificate = "empty"
            company_pan_no = "empty"
            arn_no = "empty"
            pan_card = "empty"
        else:
            #gst certificate
            try:
                gst_certificate_1 = str(request.FILES['gst_certificate']).replace(" ", "_")
                path = fs.save(f"virtual_expert/sales_manager/{id}/gst_certificate/"+gst_certificate_1, request.FILES['gst_certificate'])
                full_path_gst = all_image_url+fs.url(path)
            except:
                full_path_gst = userdata.gst_certificate
            #pan card
            try:
                pan_card_1 = str(request.FILES['pan_card']).replace(" ", "_")
                path1 = fs.save(f"virtual_expert/sales_manager/{id}/pan_card/"+pan_card_1, request.FILES['pan_card'])
                full_path_pan = all_image_url+fs.url(path1)
            except:
                full_path_pan = userdata.pan_card
            #############
            gst_number = request.POST['gst_number']
            gst_certificate = full_path_gst
            company_pan_no = request.POST['company_pan_no']
            arn_no = request.POST['arn_no']
            pan_card = full_path_pan
        #work
        if request.POST['work_job_title'] == '':
            work_job_title = "empty"
        else:
            work_job_title = request.POST['work_job_title']
        if request.POST['work_company_name'] == '':
            work_company_name = "empty"
        else:
            work_company_name = request.POST['work_company_name']
        if request.POST['work_job_location'] == '':
            work_job_location = "empty"
        else:
            work_job_location = request.POST['work_job_location']
        if request.POST['ex_job_title'] == '':
            ex_job_title = "empty"
        else:
            ex_job_title =request.POST['ex_job_title']
        if request.POST['ex_company_name'] == '':
            ex_company_name = "empty"
        else:
            ex_company_name =request.POST['ex_company_name']
        if request.POST['year_experience'] == '':
            year_experience = "empty"
        else:
            year_experience =request.POST['year_experience']
        if request.POST['ex_location'] == '':
            ex_location = "empty"
        else:
            ex_location =request.POST['ex_location']
        print("helo")
        data = {
            'full_name': request.POST['full_name'],
            'personal_country': request.POST['personal_country'],
            'personal_city': city,
            'personal_address': request.POST['personal_address'],  
            'level_education': json.dumps(request.POST.getlist('level_education')),           
            'field_study': json.dumps(request.POST.getlist('field_study')),           
            'work_job_title': work_job_title,           
            'work_company_name': work_company_name,           
            'work_job_location': work_job_location,           
            'ex_job_title': ex_job_title,           
            'ex_company_name': ex_company_name,           
            'year_experience': year_experience,           
            'ex_location': ex_location,           
            'degree_cer': full_path_degree,           
            'ex_cer': full_path_ex,           
            'work_type': request.POST['work_type'],           
            'gst_number': gst_number,           
            'gst_certificate': gst_certificate,           
            'company_pan_no': company_pan_no,           
            'arn_no': arn_no,           
            'pan_card': pan_card,       
            'id_card': full_path_one,
            'sign_document': full_path_two,
            'verification_img':verification_img
           
        }

        print(data)
        basicdetailsserializer = hm_serializer.sales_acc_Serializer(
            instance=userdata, data=data, partial=True)
        if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")

            #hiring manager
            get_uid = salesmanager.objects.filter(uid=id).values()[0]
            print(get_uid["hiring_manager"])
            userdata1 = hiringmanager.objects.get(uid= get_uid["hiring_manager"])
            print(userdata1)
            hm_data = hiringmanager.objects.filter(uid= get_uid["hiring_manager"]).values()[0]
            # hm_userdata = hiringmanager.objects.filter(uid=id).values()[0]
            print(hm_data['sales_manager'])
        
            sales_manager = jsondec.decode(hm_data['sales_manager']) 
            alter_values = []
            print("new")
            print(get_uid['uid'])
            for x in sales_manager:
                if get_uid['uid'] == x['uid']:
                    alter_values.append(get_uid)
                else:
                    alter_values.append(x)
            data1={
                'sales_manager': json.dumps(alter_values)
            }
            print(data1)
            hmdetailsserializer = hm_serializer.sales_manager_Serializer(
            instance=userdata1, data=data1, partial=True)
            if hmdetailsserializer.is_valid():
                hmdetailsserializer.save()
                print("valid data")
            
            return Response(id, status=status.HTTP_200_OK)
        else:
            return Response({"sserializer issue"}, status=status.HTTP_403_FORBIDDEN)
    except:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)
    
#hiring_upload_account
@api_view(['POST'])
def hiring_upload_account(request,id):
    try:
        print(request.POST)
        print(request.FILES)
        fs = FileSystemStorage()
        userdata = hiringmanager.objects.get(uid=id)
        id_card = str(request.FILES['id_card']).replace(" ", "_")
        path_one = fs.save(f"virtual_expert/hiring_manager/{id}/id_card/"+id_card, request.FILES['id_card'])

        # full_path = "http://54.159.186.219:8000"+fs.url(path)
        full_path_one = all_image_url+fs.url(path_one)
        signed = str(request.FILES['sign_document']).replace(" ", "_")
        path_two = fs.save(f"virtual_expert/hiring_manager/{id}/signed_document/"+signed, request.FILES['sign_document'])

        # full_path = "http://54.159.186.219:8000"+fs.url(path)
        full_path_two = all_image_url+fs.url(path_two)
        
        #verification Image
        verification = str(request.FILES['verification_img']).replace(" ", "_")
        path_three = fs.save(f"virtual_expert/hiring_manager/{id}/verification_image/"+verification, request.FILES['verification_img'])
        # full_path = "http://54.159.186.219:8000"+fs.url(path)
        verification_img = all_image_url+fs.url(path_three)
        #office
        if 'office_city' in request.POST:
            office_city = request.POST['office_city']
        else:
            office_city = "empty"
        #personal
        if "personal_city" in request.POST:
            city = request.POST['personal_city']
        else:
            city = "None"
        #degree certificate
        try:
            degree_certificate_1 = str(request.FILES['degree_cer']).replace(" ", "_")
            path_deg = fs.save(f"virtual_expert/hiring_manager/{id}/degree_certificate/"+degree_certificate_1, request.FILES['degree_cer'])
            full_path_degree = all_image_url+fs.url(path_deg)
        except:
            full_path_degree = userdata.degree_cer
         #experience certificate
        
        try:
            ex_certificate_1 = str(request.FILES['ex_cer']).replace(" ", "_")
            path_ex = fs.save(f"virtual_expert/hiring_manager/{id}/experience_certificate/"+ex_certificate_1, request.FILES['ex_cer'])
            full_path_ex = all_image_url+fs.url(path_ex)
        except:
            full_path_ex = userdata.ex_cer
        #type
        if request.POST['work_type'] == "Personal":
            gst_number = "empty"
            gst_certificate = "empty"
            company_pan_no = "empty"
            arn_no = "empty"
            pan_card = "empty"
        else:
            #gst certificate
            try:
                gst_certificate_1 = str(request.FILES['gst_certificate']).replace(" ", "_")
                path = fs.save(f"virtual_expert/hiring_manager/{id}/gst_certificate/"+gst_certificate_1, request.FILES['gst_certificate'])
                full_path_gst = all_image_url+fs.url(path)
            except:
                full_path_gst = userdata.gst_certificate
            #pan card
            try:
                pan_card_1 = str(request.FILES['pan_card']).replace(" ", "_")
                path1 = fs.save(f"virtual_expert/hiring_manager/{id}/pan_card/"+pan_card_1, request.FILES['pan_card'])
                full_path_pan = all_image_url+fs.url(path1)
            except:
                full_path_pan = userdata.pan_card
            #############
            gst_number = request.POST['gst_number']
            gst_certificate = full_path_gst
            company_pan_no = request.POST['company_pan_no']
            arn_no = request.POST['arn_no']
            pan_card = full_path_pan
        #work
        if request.POST['work_job_title'] == '':
            work_job_title = "empty"
        else:
            work_job_title = request.POST['work_job_title']
        if request.POST['work_company_name'] == '':
            work_company_name = "empty"
        else:
            work_company_name = request.POST['work_company_name']
        if request.POST['work_job_location'] == '':
            work_job_location = "empty"
        else:
            work_job_location = request.POST['work_job_location']
        if request.POST['ex_job_title'] == '':
            ex_job_title = "empty"
        else:
            ex_job_title =request.POST['ex_job_title']
        if request.POST['ex_company_name'] == '':
            ex_company_name = "empty"
        else:
            ex_company_name =request.POST['ex_company_name']
        if request.POST['year_experience'] == '':
            year_experience = "empty"
        else:
            year_experience =request.POST['year_experience']
        if request.POST['ex_location'] == '':
            ex_location = "empty"
        else:
            ex_location =request.POST['ex_location']
        print("helo")
        data = {
            'office_name': request.POST['office_name'],
            'office_country': request.POST['office_country'],
            'office_city': office_city,
            'office_address': request.POST['office_address'],  
            'first_name': request.POST['first_name'],
            'last_name': request.POST['last_name'],
            'personal_country': request.POST['personal_country'],
            'personal_city': city,
            'personal_address': request.POST['personal_address'],
            'level_education': json.dumps(request.POST.getlist('level_education')),           
            'field_study': json.dumps(request.POST.getlist('field_study')),           
            'work_job_title': work_job_title,           
            'work_company_name': work_company_name,           
            'work_job_location': work_job_location,           
            'ex_job_title': ex_job_title,           
            'ex_company_name': ex_company_name,           
            'year_experience': year_experience,           
            'ex_location': ex_location,           
            'degree_cer': full_path_degree,           
            'ex_cer': full_path_ex,           
            'work_type': request.POST['work_type'],           
            'gst_number': gst_number,           
            'gst_certificate': gst_certificate,           
            'company_pan_no': company_pan_no,           
            'arn_no': arn_no,           
            'pan_card': pan_card,       
            'id_card': full_path_one,
            'sign_document': full_path_two,
            'verification_img':verification_img
           
        }
        print(data)
        basicdetailsserializer = hm_serializer.hiring_acc_Serializer(
            instance=userdata, data=data, partial=True)
        if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            
            #hiring manager
            get_uid = hiringmanager.objects.filter(uid=id).values()[0]
            print(get_uid["my_hiring_manager"])
            userdata1 = hiringmanager.objects.get(uid= get_uid["my_hiring_manager"])
            print(userdata1)
            hm_data = hiringmanager.objects.filter(uid= get_uid["my_hiring_manager"]).values()[0]
            # hm_userdata = hiringmanager.objects.filter(uid=id).values()[0]
            print(hm_data['hiring_manager'])
        
            hiring_manager = jsondec.decode(hm_data['hiring_manager']) 
            alter_values = []
            print("new")
            print(get_uid['uid'])
            for x in hiring_manager:
                if get_uid['uid'] == x['uid']:
                    alter_values.append(get_uid)
                else:
                    alter_values.append(x)
            data1={
                'hiring_manager': json.dumps(alter_values)
            }
            print(data1)
            hmdetailsserializer = hm_serializer.hiring_manager_Serializer(
            instance=userdata1, data=data1, partial=True)
            if hmdetailsserializer.is_valid():
                hmdetailsserializer.save()
                print("valid data")
            
            return Response(id, status=status.HTTP_200_OK)
        else:
            return Response({"sserializer issue"}, status=status.HTTP_403_FORBIDDEN)
    except:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)
    
#afilliate_upload_account
@api_view(['POST'])
def affiliate_upload_account(request,id):
    try:
        print(request.POST)
        print(request.FILES)
        fs = FileSystemStorage()
        userdata = affliate_marketing.objects.get(uid=id)
        # userdata.pop('created_date')
        id_card = str(request.FILES['id_card']).replace(" ", "_")
        path_one = fs.save(f"virtual_expert/affliate_marketing/{id}/id_card/"+id_card, request.FILES['id_card'])

        # full_path = "http://54.159.186.219:8000"+fs.url(path)
        full_path_one = all_image_url+fs.url(path_one)
        signed = str(request.FILES['sign_document']).replace(" ", "_")
        path_two = fs.save(f"virtual_expert/affliate_marketing/{id}/signed_document/"+signed, request.FILES['sign_document'])

        # full_path = "http://54.159.186.219:8000"+fs.url(path)
        full_path_two = all_image_url+fs.url(path_two)
        #verification Image
        verification = str(request.FILES['verification_img']).replace(" ", "_")
        path_three = fs.save(f"virtual_expert/affliate_marketing/{id}/verification_image/"+verification, request.FILES['verification_img'])
        # full_path = "http://54.159.186.219:8000"+fs.url(path)
        verification_img = all_image_url+fs.url(path_three)
        
        #personal
        if "personal_city" in request.POST:
            city = request.POST['personal_city']
        else:
            city = "None"
        #degree certificate
        try:
            degree_certificate_1 = str(request.FILES['degree_cer']).replace(" ", "_")
            path_deg = fs.save(f"virtual_expert/affliate_marketing/{id}/degree_certificate/"+degree_certificate_1, request.FILES['degree_cer'])
            full_path_degree = all_image_url+fs.url(path_deg)
        except:
            full_path_degree = userdata.degree_cer
         #experience certificate
        
        try:
            ex_certificate_1 = str(request.FILES['ex_cer']).replace(" ", "_")
            path_ex = fs.save(f"virtual_expert/affliate_marketing/{id}/experience_certificate/"+ex_certificate_1, request.FILES['ex_cer'])
            full_path_ex = all_image_url+fs.url(path_ex)
        except:
            full_path_ex = userdata.ex_cer
        #type
        if request.POST['work_type'] == "Personal":
            gst_number = "empty"
            gst_certificate = "empty"
            company_pan_no = "empty"
            arn_no = "empty"
            pan_card = "empty"
        else:
            #gst certificate
            try:
                gst_certificate_1 = str(request.FILES['gst_certificate']).replace(" ", "_")
                path = fs.save(f"virtual_expert/affliate_marketing/{id}/gst_certificate/"+gst_certificate_1, request.FILES['gst_certificate'])
                full_path_gst = all_image_url+fs.url(path)
            except:
                full_path_gst = userdata.gst_certificate
            #pan card
            try:
                pan_card_1 = str(request.FILES['pan_card']).replace(" ", "_")
                path1 = fs.save(f"virtual_expert/affliate_marketing/{id}/pan_card/"+pan_card_1, request.FILES['pan_card'])
                full_path_pan = all_image_url+fs.url(path1)
            except:
                full_path_pan = userdata.pan_card
            #############
            gst_number = request.POST['gst_number']
            gst_certificate = full_path_gst
            company_pan_no = request.POST['company_pan_no']
            arn_no = request.POST['arn_no']
            pan_card = full_path_pan
        #work
        if request.POST['work_job_title'] == '':
            work_job_title = "empty"
        else:
            work_job_title = request.POST['work_job_title']
        if request.POST['work_company_name'] == '':
            work_company_name = "empty"
        else:
            work_company_name = request.POST['work_company_name']
        if request.POST['work_job_location'] == '':
            work_job_location = "empty"
        else:
            work_job_location = request.POST['work_job_location']
        if request.POST['ex_job_title'] == '':
            ex_job_title = "empty"
        else:
            ex_job_title =request.POST['ex_job_title']
        if request.POST['ex_company_name'] == '':
            ex_company_name = "empty"
        else:
            ex_company_name =request.POST['ex_company_name']
        if request.POST['year_experience'] == '':
            year_experience = "empty"
        else:
            year_experience =request.POST['year_experience']
        if request.POST['ex_location'] == '':
            ex_location = "empty"
        else:
            ex_location =request.POST['ex_location']
        print("helo")
        data = {
            'full_name': request.POST['full_name'],
            'personal_country': request.POST['personal_country'],
            'personal_city': city,
            'personal_address': request.POST['personal_address'],  
            'level_education': json.dumps(request.POST.getlist('level_education')),           
            'field_study': json.dumps(request.POST.getlist('field_study')),           
            'work_job_title': work_job_title,           
            'work_company_name': work_company_name,           
            'work_job_location': work_job_location,           
            'ex_job_title': ex_job_title,           
            'ex_company_name': ex_company_name,           
            'year_experience': year_experience,           
            'ex_location': ex_location,           
            'degree_cer': full_path_degree,           
            'ex_cer': full_path_ex,           
            'work_type': request.POST['work_type'],           
            'gst_number': gst_number,           
            'gst_certificate': gst_certificate,           
            'company_pan_no': company_pan_no,           
            'arn_no': arn_no,           
            'pan_card': pan_card,       
            'id_card': full_path_one,
            'sign_document': full_path_two,
            'verification_img':verification_img
           
        }

        print(data)
        basicdetailsserializer = hm_serializer.affiliate_marketing_acc_Serializer(
            instance=userdata, data=data, partial=True)
        if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")

            #hiring manager
            get_uid = affliate_marketing.objects.filter(uid=id).values()[0]
            get_uid.pop('created_date')
            print(get_uid["hiring_manager"])
            userdata1 = hiringmanager.objects.get(uid= get_uid["hiring_manager"])
            print(userdata1)
            hm_data = hiringmanager.objects.filter(uid= get_uid["hiring_manager"]).values()[0]
            # hm_userdata = hiringmanager.objects.filter(uid=id).values()[0]
            print(hm_data['affiliate_marketing'])
            
            affiliate_marketing = jsondec.decode(hm_data['affiliate_marketing']) 
            alter_values = []
            print("new")
            print(get_uid['uid'])
            for x in affiliate_marketing:
                if get_uid['uid'] == x['uid']:
                    alter_values.append(get_uid)
                else:
                    alter_values.append(x)
            data1={
                'affiliate_marketing': json.dumps(alter_values)
            }
            print(data1)
            hmdetailsserializer = hm_serializer.affiliate_markting_Serializer(
            instance=userdata1, data=data1, partial=True)
            if hmdetailsserializer.is_valid():
                hmdetailsserializer.save()
                print("valid data")
            
            return Response(id, status=status.HTTP_200_OK)
        else:
            return Response({"sserializer issue"}, status=status.HTTP_403_FORBIDDEN)
    except:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)
    
#private investigator
@api_view(['POST'])
def private_investigator_upload_account(request,id):
    try:
        print(request.POST)
        print(request.FILES)
        fs = FileSystemStorage()
        userdata = models.private_investigator.objects.get(uid=id)
        
        id_card = str(request.FILES['id_card']).replace(" ", "_")
        path_one = fs.save(f"virtual_expert/private_investigator/{id}/id_card/"+id_card, request.FILES['id_card'])

        # full_path = "http://54.159.186.219:8000"+fs.url(path)
        full_path_one = all_image_url+fs.url(path_one)
        signed = str(request.FILES['sign_document']).replace(" ", "_")
        path_two = fs.save(f"virtual_expert/private_investigator/{id}/signed_document/"+signed, request.FILES['sign_document'])

        # full_path = "http://54.159.186.219:8000"+fs.url(path)
        full_path_two = all_image_url+fs.url(path_two)
        #verification Image
        verification = str(request.FILES['verification_img']).replace(" ", "_")
        path_three = fs.save(f"virtual_expert/private_investigator/{id}/verification_image/"+verification, request.FILES['verification_img'])
        # full_path = "http://54.159.186.219:8000"+fs.url(path)
        verification_img = all_image_url+fs.url(path_three)
        #office
        if 'office_city' in request.POST:
            office_city = request.POST['office_city']
        else:
            office_city = "empty"
        #personal
        if "personal_city" in request.POST:
            city = request.POST['personal_city']
        else:
            city = "None"
        #degree certificate
        try:
            degree_certificate_1 = str(request.FILES['degree_cer']).replace(" ", "_")
            path_deg = fs.save(f"virtual_expert/private_investigator/{id}/degree_certificate/"+degree_certificate_1, request.FILES['degree_cer'])
            full_path_degree = all_image_url+fs.url(path_deg)
        except:
            full_path_degree = userdata.degree_cer
         #experience certificate
        
        try:
            ex_certificate_1 = str(request.FILES['ex_cer']).replace(" ", "_")
            path_ex = fs.save(f"virtual_expert/private_investigator/{id}/experience_certificate/"+ex_certificate_1, request.FILES['ex_cer'])
            full_path_ex = all_image_url+fs.url(path_ex)
        except:
            full_path_ex = userdata.ex_cer
        #type
        if request.POST['work_type'] == "Personal":
            gst_number = "empty"
            gst_certificate = "empty"
            company_pan_no = "empty"
            arn_no = "empty"
            pan_card = "empty"
        else:
            #gst certificate
            try:
                gst_certificate_1 = str(request.FILES['gst_certificate']).replace(" ", "_")
                path = fs.save(f"virtual_expert/private_investigator/{id}/gst_certificate/"+gst_certificate_1, request.FILES['gst_certificate'])
                full_path_gst = all_image_url+fs.url(path)
            except:
                full_path_gst = userdata.gst_certificate
            #pan card
            try:
                pan_card_1 = str(request.FILES['pan_card']).replace(" ", "_")
                path1 = fs.save(f"virtual_expert/private_investigator/{id}/pan_card/"+pan_card_1, request.FILES['pan_card'])
                full_path_pan = all_image_url+fs.url(path1)
            except:
                full_path_pan = userdata.pan_card
            #############
            gst_number = request.POST['gst_number']
            gst_certificate = full_path_gst
            company_pan_no = request.POST['company_pan_no']
            arn_no = request.POST['arn_no']
            pan_card = full_path_pan
        #work
        if request.POST['work_job_title'] == '':
            work_job_title = "empty"
        else:
            work_job_title = request.POST['work_job_title']
        if request.POST['work_company_name'] == '':
            work_company_name = "empty"
        else:
            work_company_name = request.POST['work_company_name']
        if request.POST['work_job_location'] == '':
            work_job_location = "empty"
        else:
            work_job_location = request.POST['work_job_location']
        if request.POST['ex_job_title'] == '':
            ex_job_title = "empty"
        else:
            ex_job_title =request.POST['ex_job_title']
        if request.POST['ex_company_name'] == '':
            ex_company_name = "empty"
        else:
            ex_company_name =request.POST['ex_company_name']
        if request.POST['year_experience'] == '':
            year_experience = "empty"
        else:
            year_experience =request.POST['year_experience']
        if request.POST['ex_location'] == '':
            ex_location = "empty"
        else:
            ex_location =request.POST['ex_location']
        print("helo")
        data = {
            'office_name': request.POST['office_name'],
            'office_country': request.POST['office_country'],
            'office_city': office_city,
            'office_address': request.POST['office_address'],  
            'first_name': request.POST['first_name'],
            'last_name': request.POST['last_name'],
            'personal_country': request.POST['personal_country'],
            'personal_city': city,
            'personal_address': request.POST['personal_address'],
            'level_education': json.dumps(request.POST.getlist('level_education')),           
            'field_study': json.dumps(request.POST.getlist('field_study')),           
            'work_job_title': work_job_title,           
            'work_company_name': work_company_name,           
            'work_job_location': work_job_location,           
            'ex_job_title': ex_job_title,           
            'ex_company_name': ex_company_name,           
            'year_experience': year_experience,           
            'ex_location': ex_location,           
            'degree_cer': full_path_degree,           
            'ex_cer': full_path_ex,           
            'work_type': request.POST['work_type'],           
            'gst_number': gst_number,           
            'gst_certificate': gst_certificate,           
            'company_pan_no': company_pan_no,           
            'arn_no': arn_no,           
            'pan_card': pan_card,       
            'id_card': full_path_one,
            'sign_document': full_path_two,
            'verification_img':verification_img
           
        }

        print(data)
        basicdetailsserializer = hm_serializer.private_investigator_acc_Serializer(
            instance=userdata, data=data, partial=True)
        if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")

            #hiring manager
            get_uid = models.private_investigator.objects.filter(uid=id).values()[0]
            print(get_uid["hiring_manager"])
            userdata1 = hiringmanager.objects.get(uid= get_uid["hiring_manager"])
            print(userdata1)
            hm_data = hiringmanager.objects.filter(uid= get_uid["hiring_manager"]).values()[0]
            # hm_userdata = models.hiringmanager.objects.filter(uid=id).values()[0]
            print(hm_data['private_investigator'])
        
            private_investigator = jsondec.decode(hm_data['private_investigator']) 
            alter_values = []
            print("new")
            print(get_uid['uid'])
            for x in private_investigator:
                if get_uid['uid'] == x['uid']:
                    alter_values.append(get_uid)
                else:
                    alter_values.append(x)
            data1={
                'private_investigator': json.dumps(alter_values)
            }
            print(data1)
            hmdetailsserializer = hm_serializer.private_investigator_Serializer(
            instance=userdata1, data=data1, partial=True)
            if hmdetailsserializer.is_valid():
                hmdetailsserializer.save()
                print("valid data")
            
            return Response(id, status=status.HTTP_200_OK)
        else:
            return Response({"sserializer issue"}, status=status.HTTP_403_FORBIDDEN)
    except:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def add_user(request,id):
    try:
        if request.method == "POST":
            print(request.POST)
            if "delete" in request.POST:
                allData = users.objects.get(uid = request.POST["delete"])
                allData.delete()
                return Response({"Delete"}, status=status.HTTP_200_OK)
            elif "edit" in request.POST:
                print(request.POST)
                print(request.POST['edit'])
                allData = users.objects.get(uid = request.POST["edit"])
                print(request.POST.getlist('access_Privileges'))
                data={
                    'first_name': request.POST['first_name'],
                    'last_name':request.POST['last_name'],
                        'email': request.POST['email'],
                        'mobile':request.POST['mobile'],
                            'password': request.POST['password'],
                                'access_Privileges': json.dumps(request.POST.getlist('access_Privileges')),
                                # 'location':request.POST['location'],
                            
                }
                print(data)
                serializer_validate = hm_serializer.hiringedit_user_Serializer(
                        instance=allData, data=data, partial=True)
                if serializer_validate.is_valid():
                    serializer_validate.save()
                    print("Valid Data")

                    return Response({"edited Data"}, status=status.HTTP_200_OK)

            else:
                print("hm")
                allData = users.objects.all().values()
                print(allData)
                for i in allData:
                    if request.POST['email'] == i['email']:
                        return Response({"User already Exixts"}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
                    else:
                        pass
                print("jii")
                data={
                    'aid':request.POST['creator'],
                    'uid':hm_extension.id_generate(),
                    'first_name': request.POST['first_name'],
                    'last_name':request.POST['last_name'],
                        'email': request.POST['email'],
                        'mobile':request.POST['mobile'],
                            'password': request.POST['password'],
                                'access_Privileges': json.dumps(request.POST.getlist('access_Privileges')),
                                    'work': request.POST['work'],
                                    # 'creator':request.POST['creator'],
                                    # 'location':request.POST['location'],                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
                                    


                }
                print(data)
                myclientserializer = hm_serializer.add_used_Serializer( data=data)
                if myclientserializer.is_valid():
                    myclientserializer.save()
                    print("Valid Data")

                    return Response({"valid Data"}, status=status.HTTP_200_OK)

    except:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def my_users_data(request,id):
    if request.method == 'GET':
       allDataa = users.objects.filter(aid = id)
       alldataserializer = hm_serializer.add_used_Serializer(allDataa,many=True)
    return Response(data=alldataserializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def single_users_data(request,id):
    if request.method == 'GET':
       allDataa = users.objects.filter(uid = id)
       alldataserializer = hm_serializer.add_used_Serializer(allDataa,many=True)
    return Response(data=alldataserializer.data, status=status.HTTP_200_OK)




#///// Email Updation////// 
@api_view(["POST"])
def hm_email_update(request,id):
    try:
        userdata =  hm_serializer.hiringmanager.objects.get(uid=id)

        data={
            'email': request.data["email"],
        }
        basicdetailsserializer = hm_serializer.update_email_serializer(
                    instance=userdata, data=data, partial=True)
        if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
        else:
            return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
    except:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)
    

# ////// Password Rest in Account Settings//////////
@api_view(["POST"])
def hm_password_reset(request,id):
    try:
        print(request.POST)
        # userdata = hm_serializer.hiringmanager.objects.get(uid=id)
        
        email=request.POST['pass_reset']
        sender = 'abijithmailforjob@gmail.com'
        password = 'kgqzxinytwbspurf'
        subject = "Marriyo client password Reset"
        content = f"""
        PasswordResetform : {f"http://127.0.0.1:3000/hm_password_resett/{id}"}
        """
        yagmail.SMTP(sender, password).send(
            to=email,
            subject=subject,
            contents=content
        )
        print("send email")

    except:
        return Response("nochange")
    
@api_view(["POST"])
def hm_password_update(request,id):
    try:
        userdata =  hm_serializer.hiringmanager.objects.get(uid=id)

        data={
            'password': request.POST["password"],
        }
        basicdetailsserializer = hm_serializer.update_password_serializer(
                    instance=userdata, data=data, partial=True)
        if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
        else:
            return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
    except:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)
    
# ///////forget Password/////
@api_view(['POST'])
def hm_forget_password(request):
   
    if request.method == "POST":        
        print(request.POST)
        userdata1 = hm_serializer.hiringmanager.objects.get(email=request.POST['email'])
        userdata = hm_serializer.hiringmanager.objects.filter(email=request.POST['email']).values()[0]
        user_id=userdata['uid']
        data = {   
                     'email':request.POST['email'],
                    'otp1': hm_extension.otp_generate()
                    }
            
        print(data)
        dataserializer = hm_serializer.update_otp_serializer(data=data, instance=userdata1,partial=True)
        print(dataserializer)
        if dataserializer.is_valid():
            print("done")
            dataserializer.save()
            print("Valid Data")
            hm_extension.send_mail_password(data['email'],data['otp1'])
            print("Email send")
            return Response(userdata['uid'], status=status.HTTP_200_OK)
        else:
            return Response({"serializer Issue"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({"Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)           
    

@api_view(['POST'])
def hm_forget_password_otp(request, id):
    try:

            try:
                if hm_extension.validate_otp1(id, int(request.data['user_otp1'])):
                    try:
                        print("userotp",request.data['user_otp1'])
                        userSpecificData = hm_serializer.hiringmanager.objects.get(uid=id)
                        print(userSpecificData)
                        serializer_validate = hm_serializer.OTP1Serializer(
                            instance=userSpecificData, data=request.POST, partial=True)
                        if serializer_validate.is_valid():
                            print("done")
                            serializer_validate.save()
                            print("Valid OTP")
                            if hm_extension.verify_forget_otp(id):
                                print("verified")
                                return Response(id, status=status.HTTP_200_OK)
                            else:
                                return Response({"Cannot Verify OTP"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                        else:
                            return Response({"Invalid OTP"}, status=status.HTTP_404_NOT_FOUND)
                    except:
                        return Response({"serializer Issue"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    return Response({"Wrong OTP"}, status=status.HTTP_403_FORBIDDEN)
            except:
                return Response({"Invalid Json Format (OR) Invalid Key"}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({"Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
def hm_delete_data(request):   
    try:
        print(request.data['email'])
        data_to_delete = hm_serializer.hiringmanager.objects.get(email = request.data['email'])

        if data_to_delete:
            data_to_delete.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "Data not found"}, status=status.HTTP_404_NOT_FOUND)
    except:
        return Response({"Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
      
# All Notifications Updation 
@api_view(['POST'])
def notification_up(request):
    if request.method == "POST":
        print(request.data)
        data={
            'not_id':hm_extension.id_generate(),
            'noter_id': request.data['noter_id'],
            'not_message': request.data['not_message'],
            'notify_id':request.data['notify_id'],

        }
        basicdetailsserializer = hm_serializer.notificationSerializer(data = data)
        if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response({'success'},status=status.HTTP_200_OK)
        else:
            print("not valid")
            return Response({"serializer prblm"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


# Getting Notification List for all users    
@api_view(['GET'])
def notification_data(request,id):
    if request.method == 'GET':
       allDataa = hm_serializer.Notification.objects.filter(notify_id = id).order_by('-notify_date')
       alldataserializer = hm_serializer.notificationlistSerializer(allDataa,many=True)
    return Response(data=alldataserializer.data, status=status.HTTP_200_OK)

# delete single notification 
@api_view(["POST"])
def hm_notify_delete(request,id):
    try:
        delete_data = hm_serializer.Notification.objects.filter(not_id = id).values()
        print(delete_data)
        if delete_data:
            delete_data.delete()
            return Response({"Deleted"}, status=status.HTTP_200_OK)
        else:
            return Response({"Data not found"}, status=status.HTTP_404_NOT_FOUND)
    except:
        return Response({"Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
# Delete All Notification
@api_view(['POST'])  
def delete_all_notification(request,id):
    try:
        delete_all=hm_serializer.Notification.objects.filter(notify_id = id)
        print(delete_all)
        if delete_all:
            delete_all.delete()
            return Response({'All Deleted'},status=status.HTTP_200_OK)
        else:
            return Response({'no data'},status=status.HTTP_404_NOT_FOUND)
    except:
        return Response({'server prblm'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# HM notification Status change
@api_view(["POST"])
def hm_notify_status_true(request,id):
    try:
        user=get_object_or_404(hiringmanager,uid=id)
        user.notification_status=True
        user.save()
        return Response("success",status=status.HTTP_200_OK)
    except:
        return Response("nostatus",status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["POST"])
def hm_notify_status_false(request,id):
    try:
        user=get_object_or_404(hiringmanager,uid=id)
        user.notification_status=False
        user.save()
        return Response("success",status=status.HTTP_200_OK)
    except:
        return Response("nostatus",status=status.HTTP_400_BAD_REQUEST)
    
