from django.shortcuts import render
from django.http import HttpResponse,JsonResponse


from virtualExpert import ad_pro_serializer,hm_serializer,sm_serializer
from virtualExpert import models
from virtualExpert.models import ad_provider,users
from virtualExpert import ad_pro_extension

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
import math



# Create your views here.
all_image_url = "http://127.0.0.1:3000/"
@api_view(['POST'])
def ad_pro_signup(request):
    try:
        try:
            if ad_pro_extension.validate_email(request.data['email']):
                return Response("User Already Exists", status=status.HTTP_302_FOUND)
            else:
                x = datetime.datetime.now()
                datas = {
                    'email': request.data["email"],
                    'mobile': request.data["mobile"],
                    'password': request.data["password"],
                    'uid': ad_pro_extension.id_generate(),
                    'otp': ad_pro_extension.otp_generate(),
                    'created_date':str(x.strftime("%d"))+" "+str(x.strftime("%B"))+","+str(x.year)
                }
                print(datas)
                dataserializer = ad_pro_serializer.SignupSerializer(data=datas)
                print(datas['uid'])
                if dataserializer.is_valid():
                    dataserializer.save()
                    print("Valid Data")
                    ad_pro_extension.send_mail(datas['email'], datas['otp'])
                    print("Email send")
                    return Response(datas['uid'], status=status.HTTP_200_OK)
                else:
                    return Response({"Bad Request"}, status=status.HTTP_403_FORBIDDEN)
        except:
            return Response({"Invalid Json Format (OR) Invalid Key"}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({"Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST'])
def ad_pro_otp(request, id):
    try:
        try:
            if ad_pro_extension.validate_otp(id, int(request.data['user_otp'])):
                try:
                    userSpecificData = models.ad_provider.objects.get(uid=id)
                    print(userSpecificData)
                    serializer_validate = ad_pro_serializer.OTPSerializer(
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
def ad_pro_signin(request):
    try:
        try:
            if ad_pro_extension.validate_email(request.data['email']):
                if ad_pro_extension.verify_user(request.data['email'], request.data['password']):
                    if ad_pro_extension.verify_user_otp(request.data['email']):
                        if ad_pro_extension.get_user_id(request.data['email']):
                            return Response(ad_pro_extension.get_user_id(request.data['email']), status=status.HTTP_200_OK)
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
def ad_pro_profile_picture(request,id):
    try:
        print(request.FILES['profile_picture'])
        fs = FileSystemStorage()
        userdata = ad_pro_serializer.ad_provider.objects.get(uid=id)
        id_card = str(request.FILES['profile_picture']).replace(" ", "_")
        print(id_card)
        print(id)
        path = fs.save(f"virtual_expert/ad_provider/{id}/profile_picture/"+id_card, request.FILES['profile_picture'])

        # full_path = "http://54.159.186.219:8000"+fs.url(path)
        full_path = all_image_url+fs.url(path)
        print(full_path)

        data = {          
            'profile_picture': full_path
           
        }

        print(data)
        basicdetailsserializer = ad_pro_serializer.profile_picture_Serializer(
            instance=userdata, data=data, partial=True)
        if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
        else:
            return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
    except:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def ad_pro_upload_account(request,id):
    try:
        jsondec = json.decoder.JSONDecoder()
        print(request.POST)
        fs = FileSystemStorage()
        userdata = ad_pro_serializer.ad_provider.objects.get(uid=id)
        # print(userdata)
        # id_card = str(request.FILES['id_card']).replace(" ", "_")
        # path = fs.save(f"virtual_expert/ad_provider/{id}/id_card/"+id_card, request.FILES['id_card'])

        # # full_path = "http://54.159.186.219:8000"+fs.url(path)
        # full_path = all_image_url+fs.url(path)
        # print(full_path)
        if "personal_city" in request.POST:
            city = request.POST['personal_city']
        else:
            city = "None"
        #degree certificate
        degree_certificate_1 = str(request.FILES['degree_cer']).replace(" ", "_")
        path_deg = fs.save(f"virtual_expert/ad_provider/{id}/degree_certificate/"+degree_certificate_1, request.FILES['degree_cer'])
        full_path_degree = all_image_url+fs.url(path_deg)
         #experience certificate
        if 'ex_cer' in request.FILES:
            ex_certificate_1 = str(request.FILES['ex_cer']).replace(" ", "_")
            path_ex = fs.save(f"virtual_expert/ad_provider/{id}/experience_certificate/"+ex_certificate_1, request.FILES['ex_cer'])
            full_path_ex = all_image_url+fs.url(path_ex)
        else:
            full_path_ex = "empty"
        if request.POST['work_type'] == "Personal":
            gst_number = "empty"
            gst_certificate = "empty"
            company_pan_no = "empty"
            arn_no = "empty"
            pan_card = "empty"
        else:
            #gst certificate
            gst_certificate_1 = str(request.FILES['gst_certificate']).replace(" ", "_")
            path = fs.save(f"virtual_expert/ad_provider/{id}/gst_certificate/"+gst_certificate_1, request.FILES['gst_certificate'])
            full_path_gst = all_image_url+fs.url(path)
            #pan card
            pan_card_1 = str(request.FILES['pan_card']).replace(" ", "_")
            path1 = fs.save(f"virtual_expert/ad_provider/{id}/pan_card/"+pan_card_1, request.FILES['pan_card'])
            full_path_pan = all_image_url+fs.url(path1)
            #############
            gst_number = request.POST['gst_number']
            gst_certificate = full_path_gst
            company_pan_no = request.POST['company_pan_no']
            arn_no = request.POST['arn_no']
            pan_card = full_path_pan
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
            'office_city': request.POST['office_city'],
            'office_address': request.POST['office_address'],
            'first_name': request.POST['first_name'],
            'last_name': request.POST['last_name'],
            'personal_country': request.POST['personal_country'],
            'personal_city': city,
            'personal_address': request.POST['personal_address'],           
            # 'id_card': full_path,
            'hiring_manager': request.POST['hiring_manager'],
            'sales_manager': request.POST['sales_manager'],
            'type':request.POST['type'],
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
            'pan_card': pan_card  
        }

        print(data)
        basicdetailsserializer = ad_pro_serializer.upload_acc_Serializer(
            instance=userdata, data=data, partial=True)
        if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            userdata1 = models.hiringmanager.objects.get(uid= request.POST['hiring_manager'])
            hm_data = models.hiringmanager.objects.filter(uid= request.POST['hiring_manager']).values()[0]
            userdata2 = models.salesmanager.objects.get(uid= request.POST['sales_manager'])
            sm_data = models.salesmanager.objects.filter(uid= request.POST['sales_manager']).values()[0]
            ad_pro_userdata = models.ad_provider.objects.filter(uid=id).values()[0]
            
            if hm_data['ad_provider'] == None:
                my_ad_provider = []
                print("new")
                my_ad_provider.append(ad_pro_userdata)
            else:
                print("add")
                my_ad_provider = jsondec.decode(hm_data['ad_provider'])
                # print(my_profile_add)
                my_ad_provider.append(ad_pro_userdata)

            if sm_data['ad_provider'] == None:
                my_ad_pro = []
                print("new")
                my_ad_pro.append(ad_pro_userdata)
            else:
                print("add")
                my_ad_pro = jsondec.decode(hm_data['ad_provider'])
                # print(my_profile_add)
                my_ad_pro.append(ad_pro_userdata)
            data1={
                'ad_provider': json.dumps(my_ad_provider)
            }
            data2={ 'ad_provider': json.dumps(my_ad_pro)}
            print(data1)
            print(data2)
            hmdetailsserializer = hm_serializer.ad_provider_Serializer(
            instance=userdata1, data=data1, partial=True)
            smdetailsserializer = sm_serializer.ad_provider_Serializer(
            instance=userdata2, data=data2, partial=True)
            if hmdetailsserializer.is_valid():
                hmdetailsserializer.save()
                print("valid data1")
            else:
                print("data1 not saved")
            if smdetailsserializer.is_valid():
                smdetailsserializer.save()
                print("valid data2") 
            else:
                print("data2 not saved")   
            return Response(id, status=status.HTTP_200_OK)
        else:
            return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
    except:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)

# ///All  Ad_pro Datas/////
@api_view(['GET'])
def all_ad_pro_data(request):
    if request.method == 'GET':
       allDataa = ad_pro_serializer.ad_provider.objects.all()
       alldataserializer = ad_pro_serializer.adproviderSerializer(allDataa,many=True)
    return Response(data=alldataserializer.data, status=status.HTTP_200_OK)

# //// Provider Data ////
@api_view(['GET'])
def ad_pro_my_data(request,id):
    if request.method == 'GET':
       allDataa = ad_pro_serializer.ad_provider.objects.filter(uid=id)
       alldataserializer = ad_pro_serializer.adproviderSerializer(allDataa,many=True)
    return Response(data=alldataserializer.data, status=status.HTTP_200_OK)

# //// Edit profile////
@api_view(['POST'])
def ad_pro_edit_account(request,id):
    try:
        print(request.POST)
        print(request.FILES)
        fs = FileSystemStorage()
        userdata = ad_pro_serializer.ad_provider.objects.get(uid=id)
        userdataa =ad_pro_serializer.ad_provider.objects.filter(uid=id).values()[0]
        if "profile_picture" in request.FILES:
            id_card = str(request.FILES['profile_picture']).replace(" ", "_")
            path = fs.save(f"virtual_expert/ad_provider/{id}/profile_picture/"+id_card, request.FILES['profile_picture'])
    
            # full_path = "http://54.159.186.219:8000"+fs.url(path)
            full_path = all_image_url+fs.url(path)
        else:
            full_path = userdataa['profile_picture']
        
        data = {
            'office_name': request.POST['office_name'],
            'office_country': request.POST['office_country'],
            'office_city': request.POST['office_city'],
            'office_address': request.POST['office_address'],
            'first_name': request.POST['first_name'],
            'last_name': request.POST['last_name'],
            'personal_country': request.POST['personal_country'],
            'personal_city': request.POST['personal_city'],
            'personal_address': request.POST['personal_address'],
            # 'notary': request.POST['notary'],           
            'profile_picture': full_path
        }
        
        print(data)
        basicdetailsserializer = ad_pro_serializer.edit_acc_Serializer(
            instance=userdata, data=data, partial=True)
        if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
        else:
            return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
    except:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)

#//// Create New ads//// 
@api_view(['POST'])
def create_new_ads(request,id):
    # try:
    print(request.POST)
    print(request.FILES)
    fs = FileSystemStorage()
    id_card = str(request.FILES['id_card']).replace(" ", "_")
    path = fs.save(f"virtual_expert/ad_pro_ads/{id}/id_card/"+id_card, request.FILES['id_card'])
    other_ads = str(request.FILES['other_ads']).replace(" ", "_")
    paths = fs.save(f"virtual_expert/ad_pro_ads/{id}/other_ads/"+other_ads, request.FILES['other_ads'])
    # full_path = "http://54.159.186.219:8000"+fs.url(path)
    full_path = all_image_url+fs.url(path)
    full_paths = all_image_url+fs.url(paths)
    userdata=ad_provider.objects.filter(uid=id).values()[0]
    print(userdata)
    x = datetime.datetime.now()
    if "office_state" in request.POST:
        city = request.POST['office_state']
    else:
        city = "None"

    # if "no_views" in request.POST:
    #     view_no=int(request.POST['no_views'])
    #     if view_no < 1000:
    #         view = str(view_no)
    #     elif view_no < 1000000:
    #         view= '{}k'.format(view_no // 1000)
    #     else:
    #         view= '{}M'.format(view_no // 1000000)
    # else:
    #     view=int(request.POST['no_views'])

    

    data = {
        'ad_name': request.POST['ad_name'],
        'ad_id': ad_pro_extension.ad_id_generate(),
        'ad_pro':json.dumps(userdata),
        'category': request.POST['category'],
        'ad_type': request.POST['ad_type'],
        'languages': request.POST['languages'],
        'office_country': request.POST['office_country'],
        'office_state': city,
        'office_district': request.POST['office_district'],
        'gender': request.POST['gender'],
        'age_range': request.POST['age_range'],
        'age_to': request.POST['age_to'],           
        'id_card': full_path,
        'no_views':0,
        'days_required':request.POST['days_required'],
        'times_repeat':request.POST['times_repeat'],
        'ad_details':request.POST['ad_details'],
        'other_ads':full_paths,
        'action_name':request.POST['action_name'],
        'action_url':request.POST['action_url'],
        # 'reason':request.POST['reason'],      
        'status':"Pending",
        # 'coin':request.POST['coin'],
        # 'commission':request.POST['commission'],
        'ad_created_date':str(x.strftime("%d"))+" "+str(x.strftime("%B"))+","+str(x.year),
        'ad_created_time':str(x.strftime("%I : %M %p"))

        }

    print(data)

    basicdetailsserializer = ad_pro_serializer.create_ads_Serializer(data=data)
    print("done")
    if basicdetailsserializer.is_valid():
        basicdetailsserializer.save()
        print("Valid Data")
        return Response(id, status=status.HTTP_200_OK)
    else:
        print("serializer prblm")
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
   


# //// All Ads Data ////
@api_view(['GET'])
def all_pro_ads_data(request):
    if request.method == 'GET':
        allDataa = ad_pro_serializer.ad_pro_ads.objects.all()
    #    recent_added=ad_pro_serializer.ad_pro_ads.objects.ordered_by('ad_created_date')[:10]
        alldataserializer = ad_pro_serializer.list_ads_Serializer(allDataa,many=True)
        
        
    return Response(data=alldataserializer.data, status=status.HTTP_200_OK)

# //// Single Ad Data ////
@api_view(['GET'])
def ad_pro_ad_details(request,id):
    if request.method == 'GET':
       allDataa = ad_pro_serializer.ad_pro_ads.objects.filter(ad_id = id).values()[0]
       alldataserializer = ad_pro_serializer.list_ads_Serializer(allDataa,many=False)
       
    return Response(data=alldataserializer.data, status=status.HTTP_200_OK)

# /// Edit Ads data/////
@api_view(['POST'])
def ad_pro_edit_ads(request,id):
    # try:
    print(request.POST)
    print(request.FILES)
    fs = FileSystemStorage()
    userdata = ad_pro_serializer.ad_pro_ads.objects.get(ad_id=id)
    print(userdata)
    userdataa = ad_pro_serializer.ad_pro_ads.objects.filter(ad_id=id).values()[0]
    
    if "id_card" in request.FILES:
        id_card = str(request.FILES['id_card']).replace(" ", "_")
        path = fs.save(f"virtual_expert/ad_pro_ads/{id}/id_card/"+id_card, request.FILES['id_card'])
        # full_path = "http://54.159.186.219:8000"+fs.url(path)
        full_path = all_image_url+fs.url(path)

    else:
        full_path = userdataa['id_card']
        print(full_path)

    if "other_ads" in request.FILES:
        other_ads = str(request.FILES['other_ads']).replace(" ", "_")
        paths = fs.save(f"virtual_expert/ad_pro_ads/{id}/other_ads/"+other_ads, request.FILES['other_ads'])
        # full_path = "http://54.159.186.219:8000"+fs.url(path)
        
        full_paths = all_image_url+fs.url(paths)
    else:
        
        full_paths = userdataa['other_ads']

    # if "no_views" in request.POST:
    #     value=request.POST['no_views']
    #     if value.endswith('k'):
    #         views= int(float(value[:-1]) * 1000)
    #     elif value.endswith('m'):
    #         views=int(float(value[:-1]) * 1000000)
    #     else:
    #         views= int(value)
    #     view_no=int(views)
    #     if view_no < 1000:
    #         view = str(view_no)
    #     elif view_no < 1000000:
    #         view= '{}k'.format(view_no // 1000)
    #     else:
    #         view= '{}M'.format(view_no // 1000000)
        
    data = {
        'ad_name': request.POST['ad_name'],
        'category': request.POST['category'],
        'ad_type': request.POST['ad_type'],
        'languages': request.POST['languages'],
        'office_country': request.POST['office_country'],
        'office_state': request.POST['office_state'],
        'office_district': request.POST['office_district'],
        'gender': request.POST['gender'],
        'age_range': request.POST['age_range'],
        'age_to': request.POST['age_to'],           
        'id_card': full_path,
        # 'no_views':0,
        'days_required':request.POST['days_required'],
        'times_repeat':request.POST['times_repeat'],
        'ad_details':request.POST['ad_details'],
        'other_ads':full_paths,
        'action_name':request.POST['action_name'],
        'action_url':request.POST['action_url'],     
        'status':"Pending"
         }
    
    print(data)
    basicdetailsserializer = ad_pro_serializer.edit_ads_Serializer(
        instance=userdata, data=data, partial=True)
    if basicdetailsserializer.is_valid():
        print("valid")
        basicdetailsserializer.save()
        print("Done")
        return Response(id, status=status.HTTP_200_OK)
    else:
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)


# //// paovider Email Updation ////
@api_view(["POST"])
def ad_pro_email_update(request,id):
    try:
        userdata =  ad_pro_serializer.ad_provider.objects.get(uid=id)

        data={
            'email': request.data["email"],
        }
        basicdetailsserializer = ad_pro_serializer.update_email_serializer(
                    instance=userdata, data=data, partial=True)
        if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
        else:
            return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
    except:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST) 

# //// Provider Password Reset////
@api_view(["POST"])
def ad_pro_password_reset(request,id):
    try:
        print(request.POST)
        # userdata = ad_pro_serializer.ad_provider.objects.get(uid=id)
        
        email=request.POST['pass_reset']
        sender = 'abijithmailforjob@gmail.com'
        password = 'kgqzxinytwbspurf'
        subject = "Marriyo client password"
        content = f"""
        PasswordResetform : {f"http://127.0.0.1:3000/ad_pro_password_resett/{id}"}
        """
        yagmail.SMTP(sender, password).send(
            to=email,
            subject=subject,
            contents=content
        )
        print("send email")
        return Response("success")
    except:
        return Response("nochange")
    
# /// new password updation////   
@api_view(["POST"])
def ad_pro_password_update(request,id):
    try:
        userdata =  ad_pro_serializer.ad_provider.objects.get(uid=id)

        data={
            'password': request.POST["password"],
        }
        basicdetailsserializer = ad_pro_serializer.update_password_serializer(
                    instance=userdata, data=data, partial=True)
        if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
        else:
            return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
    except:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)

# /// Ads Status change ////
@api_view(["POST"])
def ad_status_close(request,id):
    try:
        userdata = ad_pro_serializer.ad_pro_ads.objects.get(ad_id=id)

        data={
            'status':"Closed",
        }
        basicdetailsserializer = ad_pro_serializer.update_status_serializer(
                    instance=userdata, data=data, partial=True)
        if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
        else:
            return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
    except:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])  
def ad_pro_deactive_update(request,id):
    userdata = ad_pro_serializer.ad_pro_ads.objects.get(ad_id = id)
    data={
            'status':"Deactive",
        }
    basicdetailsserializer = ad_pro_serializer.update_status_serializer(
                    instance=userdata, data=data, partial=True)
    if basicdetailsserializer.is_valid():
        basicdetailsserializer.save()
        print("Valid Data")
        return Response(id, status=status.HTTP_200_OK)
    else:
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)

@api_view(["POST"])  
def status_deactive_to_active(request,id):
    print(id)
    if request.method == 'POST':
        renew=request.POST['renew_id']
        userdata = ad_pro_serializer.ad_pro_ads.objects.get(ad_id = renew)

        data={  'days_required' : request.POST['days_required'],
                'status': "Active",
            }
        
        basicdetailsserializer = ad_pro_serializer.status_active_serializer(
                        instance=userdata, data=data, partial=True)
        if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
        else:
            return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
    

# /// Providers User ///
@api_view(['POST'])
def ad_pro_add_user(request,id):
    try:
        

        if request.method == "POST":
            print(request.POST)

            if "delete" in request.POST:
                allData = users.objects.get(uid = request.POST["delete"])
                allData.delete()
                return Response({"Deleted"}, status=status.HTTP_200_OK)
            
            elif "edit" in request.POST:
                print(request.POST)
                print(request.POST['edit'])
                allData = users.objects.get(uid = request.POST["edit"])
                print(allData)
                data={
                    'first_name': request.POST['first_name'],
                    'last_name':request.POST['last_name'],
                        'email': request.POST['email'],
                        'mobile':request.POST['mobile'],
                            'password': request.POST['password'],
                                'access_Privileges': json.dumps(request.POST.getlist('access_Privileges')),
                            
                }
                print(data)
                serializer_validate = ad_pro_serializer.edit_user_Serializer(
                        instance=allData, data=data, partial=True)
                if serializer_validate.is_valid():
                    print("Valid Data")
                    serializer_validate.save()
                    print("Done")

                    return Response({"edited Data"}, status=status.HTTP_200_OK)

            else:
                allData = ad_provider.objects.all().values()
                for i in allData:
                    if request.POST['email'] == i['email']:
                        return Response({"User already Exixts"}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
                    else:
                        pass

                data={
                    'aid':request.POST['creator'],
                    'uid':ad_pro_extension.id_generate(),
                    'first_name': request.POST['first_name'],
                    'last_name':request.POST['last_name'],
                        'email': request.POST['email'],
                        'mobile':request.POST['mobile'],
                            'password': request.POST['password'],
                                'access_Privileges': json.dumps(request.POST.getlist('access_Privileges')),
                                    'work': request.POST['work'],
                                    # 'creator':request.POST['creator'],
                                    # 'location':request.POST['location']


                }
                print(data)
                myclientserializer = ad_pro_serializer.add_user_Serializer( data=data)
                if myclientserializer.is_valid():
                    print("Done")
                    myclientserializer.save()
                    print("Valid Data")

                    return Response({"valid Data"}, status=status.HTTP_200_OK)

    except:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)
    
# /// All Users Data ////
@api_view(['GET'])
def ad_pro_my_users_data(request,id):
    if request.method == 'GET':
       allDataa = users.objects.filter(aid = id)
       alldataserializer = ad_pro_serializer.add_user_Serializer(allDataa,many=True)
    return Response(data=alldataserializer.data, status=status.HTTP_200_OK)

# /// Single user data ////
@api_view(['GET'])
def ad_pro_single_users_data(request,id):
    if request.method == 'GET':
       allDataa = users.objects.filter(uid = id)
       alldataserializer = ad_pro_serializer.add_user_Serializer(allDataa,many=True)
    return Response(data=alldataserializer.data, status=status.HTTP_200_OK)


# /// Forget password ////
@api_view(['POST'])
def ad_pro_forget_password(request): 
    if request.method == "POST":        
        print(request.POST)
        userdata1 = ad_pro_serializer.ad_provider.objects.get(email=request.POST['email'])
        userdata = ad_pro_serializer.ad_provider.objects.filter(email=request.POST['email']).values()[0]
        user_id=userdata['uid']
        data = {   
             'email':request.POST['email'],
                    'otp1': ad_pro_extension.otp_generate()
                    }
            
        print(data)
        dataserializer = ad_pro_serializer.update_otp_serializer(data=data, instance=userdata1,partial=True)
        print(dataserializer)
        if dataserializer.is_valid():
            print("done")
            dataserializer.save()
            print("Valid Data")
            ad_pro_extension.send_mail_password(data['email'], data['otp1'])
            print("Email send")
            return Response(userdata['uid'], status=status.HTTP_200_OK)
        else:
            return Response({"serializer Issue"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({"Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)           
      
@api_view(['POST'])
def ad_pro_forget_password_otp(request, id):
    try:

            try:
                if ad_pro_extension.validate_otp1(id, int(request.data['user_otp1'])):
                    try:
                        print("userotp",request.data['user_otp1'])
                        userSpecificData = models.ad_provider.objects.get(uid=id)
                        print(userSpecificData)
                        serializer_validate = ad_pro_serializer.OTP1Serializer(
                            instance=userSpecificData, data=request.POST, partial=True)
                        if serializer_validate.is_valid():
                            print("done")
                            serializer_validate.save()
                            print("Valid OTP")
                            if ad_pro_extension.verify_forget_otp(id):
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
    
# Coin Value and commission Updation
    
@api_view(['POST'])
def update_coin_value(request,id):
    allDataa = models.ad_pro_ads.objects.get(ad_id = id)
    # recent_added=ad_pro_serializer.ad_pro_ads.objects.ordered_by('ad_created_date')[:10]
    alldataserializer = ad_pro_serializer.list_ads_Serializer(allDataa,many=False)
    serialized_data = alldataserializer.data
    print(serialized_data['no_views'])
    no_of_views=serialized_data['no_views']
    # for i in range(0,len(no_of_views)):
    if no_of_views != None:  
            
        if int(no_of_views) >= 4:
            views=int(no_of_views) / 4
            coin=math.ceil(views)  
            commission=10

        else:
            coin= 0
            commission= 10
   

        data = {'coin' : coin,
                'commission':commission,
                }
        basicdetailsserializer = ad_pro_serializer.update_coin_serializer(
        instance=allDataa, data=data, partial=True)
        if basicdetailsserializer.is_valid():
            print("valid")
            basicdetailsserializer.save()
            return Response("coin Added", status=status.HTTP_200_OK)
        else:
            return Response("no data", status=status.HTTP_404_NOT_FOUND)
        

