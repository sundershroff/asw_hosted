from django.shortcuts import render
from django.http import HttpResponse,JsonResponse


from virtualExpert import ad_dis_serializer,hm_serializer,sm_serializer
from virtualExpert import models
from virtualExpert.models import ad_distributor,users
from virtualExpert import ad_dis_extension

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


jsondec = json.decoder.JSONDecoder()
# Create your views here.
all_image_url = "http://127.0.0.1:3000/"
@api_view(['POST'])
def ad_dis_signup(request):
    try:
        try:
            if ad_dis_extension.validate_email(request.data['email']):
                return Response("User Already Exists", status=status.HTTP_302_FOUND)
            else:
                x = datetime.datetime.now()
                datas = {
                    'email': request.data["email"],
                    'mobile': request.data["mobile"],
                    'password': request.data["password"],
                    'uid': ad_dis_extension.id_generate(),
                    'otp': ad_dis_extension.otp_generate(),
                    'created_date':str(x.strftime("%d"))+" "+str(x.strftime("%B"))+","+str(x.year)
                }
                print(datas)
                dataserializer = ad_dis_serializer.SignupSerializer(data=datas)
                print(datas['uid'])
                if dataserializer.is_valid():
                    dataserializer.save()
                    print("Valid Data")
                    ad_dis_extension.send_mail(datas['email'], datas['otp'])
                    print("Email send")
                    return Response(datas['uid'], status=status.HTTP_200_OK)
                else:
                    return Response({"Bad Request"}, status=status.HTTP_403_FORBIDDEN)
        except:
            return Response({"Invalid Json Format (OR) Invalid Key"}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({"Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST'])
def ad_dis_otp(request, id):
    try:
        try:
            if ad_dis_extension.validate_otp(id, int(request.data['user_otp'])):
                try:
                    userSpecificData = models.ad_distributor.objects.get(uid=id)
                    print(userSpecificData)
                    serializer_validate = ad_dis_serializer.OTPSerializer(
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
def ad_dis_signin(request):
    try:
        try:
            if ad_dis_extension.validate_email(request.data['email']):
                if ad_dis_extension.verify_user(request.data['email'], request.data['password']):
                    if ad_dis_extension.verify_user_otp(request.data['email']):
                        if ad_dis_extension.get_user_id(request.data['email']):
                            return Response(ad_dis_extension.get_user_id(request.data['email']), status=status.HTTP_200_OK)
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
def ad_dis_profile_picture(request,id):
    try:
        print(request.FILES['profile_picture'])
        fs = FileSystemStorage()
        userdata = ad_dis_serializer.ad_distributor.objects.get(uid=id)
        id_card = str(request.FILES['profile_picture']).replace(" ", "_")
        print(id_card)
        print(id)
        path = fs.save(f"virtual_expert/ad_distributor/{id}/profile_picture/"+id_card, request.FILES['profile_picture'])

        # full_path = "http://54.159.186.219:8000"+fs.url(path)
        full_path = all_image_url+fs.url(path)
        print(full_path)

        data = {          
            'profile_picture': full_path
           
        }

        print(data)
        basicdetailsserializer = ad_dis_serializer.profile_picture_Serializer(
            instance=userdata, data=data, partial=True)
        if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
        else:
            return Response({"sserializer issue"}, status=status.HTTP_403_FORBIDDEN)
    except:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)



#/////// Ad_Distributors Account/Profile Details////// 
@api_view(['POST'])
def ad_dis_upload_account(request,id):
    try:
        jsondec = json.decoder.JSONDecoder()
        print(request.POST)
        # fs = FileSystemStorage()
        userdata = ad_dis_serializer.ad_distributor.objects.get(uid=id)
        # id_card = str(request.FILES['id_card']).replace(" ", "_")
        # path = fs.save(f"virtual_expert/ad_distributor/{id}/id_card/"+id_card, request.FILES['id_card'])

        # full_path = "http://54.159.186.219:8000"+fs.url(path)
        # full_path = all_image_url+fs.url(path)
        # # full_path = "http://54.159.186.219:8000"+fs.url(path)
        # full_path = all_image_url+fs.url(path)
        if "personal_city" in request.POST:
            city = request.POST['personal_city']
        else:
            city = "None"
        

        data = {
            # 'office_name': request.POST['office_name'],
            # 'office_country': request.POST['office_country'],
            # 'office_city': request.POST['office_city'],
            # 'office_address': request.POST['office_address'],
            'first_name': request.POST['first_name'],
            'last_name': request.POST['last_name'],
            'personal_country': request.POST['personal_country'],
            'personal_city': city,
            'personal_address': request.POST['personal_address'],           
            # 'id_card': full_path,
            'hiring_manager': request.POST['hiring_manager'],
            'sales_manager': request.POST['sales_manager'],
            'type':request.POST['type'],
        }

        basicdetailsserializer = ad_dis_serializer.upload_acc_Serializer(
            instance=userdata, data=data, partial=True)
        print(basicdetailsserializer)
        if basicdetailsserializer.is_valid():
            print("done")
            basicdetailsserializer.save()
            print("Valid Data")
            userdata1 = models.hiringmanager.objects.get(uid= request.POST['hiring_manager'])
            hm_data = models.hiringmanager.objects.filter(uid= request.POST['hiring_manager']).values()[0]
            userdata2 = models.salesmanager.objects.get(uid= request.POST['sales_manager'])
            sm_data = models.salesmanager.objects.filter(uid= request.POST['sales_manager']).values()[0]
            ad_pro_userdata = models.ad_distributor.objects.filter(uid=id).values()[0]
            
            if hm_data['ad_distributor'] == None:
                my_ad_provider = []
                print("new")
                my_ad_provider.append(ad_pro_userdata)
            else:
                print("add")
                my_ad_provider = jsondec.decode(hm_data['ad_distributor'])
                # print(my_profile_add)
                my_ad_provider.append(ad_pro_userdata)

            if sm_data['ad_distributor'] == None:
                my_ad_pro = []
                print("new")
                my_ad_pro.append(ad_pro_userdata)
            else:
                print("add")
                my_ad_pro = jsondec.decode(sm_data['ad_distributor'])
                # print(my_profile_add)
                my_ad_pro.append(ad_pro_userdata)
            data1={
                'ad_distributor': json.dumps(my_ad_provider)   
            }
            data2={ 'ad_distributor': json.dumps(my_ad_pro)}
            print(data1)
            hmdetailsserializer = hm_serializer.ad_distributor_Serializer(
            instance=userdata1, data=data1, partial=True)
            smdetailsserializer = sm_serializer.ad_distributor_Serializer(
            instance=userdata2, data=data2, partial=True)
            if hmdetailsserializer.is_valid():
                hmdetailsserializer.save()
                print("data1 saved")
            else:
                print("data1 not saved")
                
            if smdetailsserializer.is_valid():
                smdetailsserializer.save()
                print("data2 saved") 
            else: 
                print("data2 not saved") 
            return Response(id, status=status.HTTP_200_OK)
        else:
            return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
    except:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)


# /// All Distributors data ////
@api_view(['GET'])
def all_dis_data(request):
    if request.method == 'GET':
       allDataa = ad_dis_serializer.ad_distributor.objects.all()
       alldataserializer = ad_dis_serializer.addistributorSerializer(allDataa,many=True)
    return Response(data=alldataserializer.data, status=status.HTTP_200_OK)

# /// Distributor data ////
@api_view(['GET'])
def dis_my_data(request,id):
    if request.method == 'GET':
       allDataa = ad_dis_serializer.ad_distributor.objects.filter(uid = id)
       alldataserializer = ad_dis_serializer.addistributorSerializer(allDataa,many=True)
    return Response(data=alldataserializer.data, status=status.HTTP_200_OK)

# /// Distributor 
@api_view(['POST'])
def ad_dis_edit_account(request,id):
    try:
        print(request.POST)
        print(request.FILES)
        fs = FileSystemStorage()
        userdata = ad_dis_serializer.ad_distributor.objects.get(uid=id)
        userdataa = ad_dis_serializer.ad_distributor.objects.filter(uid=id).values()[0]
        if "profile_picture" in request.FILES:
            id_card = str(request.FILES['profile_picture']).replace(" ", "_")
            path = fs.save(f"virtual_expert/ad_distributor/{id}/profile_picture/"+id_card, request.FILES['profile_picture'])
    
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
        basicdetailsserializer = ad_dis_serializer.edit_acc_Serializer(
            instance=userdata, data=data, partial=True)
        if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
        else:
            return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
    except:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)



#/////// Ad_Distributors Ads ////// 

@api_view(['POST'])
def create_new_ads(request,id):
    # try:
    print(request.POST)
    print(request.FILES)
    fs = FileSystemStorage()
    id_card = str(request.FILES['id_card']).replace(" ", "_")
    path = fs.save(f"virtual_expert/Create_ads/{id}/id_card/"+id_card, request.FILES['id_card'])
    other_ads = str(request.FILES['other_ads']).replace(" ", "_")
    paths = fs.save(f"virtual_expert/Create_ads/{id}/other_ads/"+other_ads, request.FILES['other_ads'])
    # full_path = "http://54.159.186.219:8000"+fs.url(path)
    full_path = all_image_url+fs.url(path)
    full_paths = all_image_url+fs.url(paths)
    userdata=ad_distributor.objects.filter(uid=id).values()[0]
    print(userdata)
    x = datetime.datetime.now()

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
        'ad_id': ad_dis_extension.ad_id_generate(),
        'ad_dis':json.dumps(userdata),
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
        'no_views':0,
        'days_required':request.POST['days_required'],
        'times_repeat':request.POST['times_repeat'],
        'ad_details':request.POST['ad_details'],
        'other_ads':full_paths,
        'action_name':request.POST['action_name'],
        'action_url':request.POST['action_url'],
        # 'coin':request.POST['coin'],
        # 'reason':request.POST['reason'],      
        'status':"Pending",
        'ad_created_date':str(x.strftime("%d"))+" "+str(x.strftime("%B"))+","+str(x.year),
        'ad_created_time':str(x.strftime("%I : %M %p"))
        }

    print(data)
    basicdetailsserializer = ad_dis_serializer.create_ads_Serializer(data=data)
    print("done")
    if basicdetailsserializer.is_valid():
        basicdetailsserializer.save()
        print("Valid Data")
        return Response(id, status=status.HTTP_200_OK)
    else:
        print("serializer prblm")
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
    # except:
    #     return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def all_ads_data(request):
    if request.method == 'GET':
       allDataa = ad_dis_serializer.Create_ads.objects.all()
       alldataserializer = ad_dis_serializer.list_ads_Serializer(allDataa,many=True)
    return Response(data=alldataserializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def ad_dis_ad_details(request,id):
    if request.method == 'GET':
       allDataa = ad_dis_serializer.Create_ads.objects.filter(ad_id = id).values()[0]
       alldataserializer = ad_dis_serializer.list_ads_Serializer(allDataa,many=False)
       
    return Response(data=alldataserializer.data, status=status.HTTP_200_OK)

# /// Ads Editing/////   
@api_view(['POST'])
def ad_dis_edit_ads(request,id):
    # try:
    print(request.POST)
    print(request.FILES)
    fs = FileSystemStorage()
    userdata = ad_dis_serializer.Create_ads.objects.get(ad_id=id)
    print(userdata)
    userdataa = ad_dis_serializer.Create_ads.objects.filter(ad_id=id).values()[0]
    
    if "id_card" in request.FILES:
        id_card = str(request.FILES['id_card']).replace(" ", "_")
        path = fs.save(f"virtual_expert/Create_ads/{id}/id_card/"+id_card, request.FILES['id_card'])
        # full_path = "http://54.159.186.219:8000"+fs.url(path)
        full_path = all_image_url+fs.url(path)

    else:
        full_path = userdataa['id_card']
        print(full_path)

    if "other_ads" in request.FILES:
        other_ads = str(request.FILES['other_ads']).replace(" ", "_")
        paths = fs.save(f"virtual_expert/Create_ads/{id}/other_ads/"+other_ads, request.FILES['other_ads'])
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
        # 'reason':request.POST['reason'],      
        'status':"Pending"
         }
    
    print(data)
    basicdetailsserializer = ad_dis_serializer.edit_ads_Serializer(
        instance=userdata, data=data, partial=True)
    if basicdetailsserializer.is_valid():
        print("valid")
        basicdetailsserializer.save()
        print("Done")
        return Response(id, status=status.HTTP_200_OK)
    else:
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
   

# //// Email Update /////
@api_view(["POST"])
def ad_dis_email_update(request,id):
    try:
        userdata =  ad_dis_serializer.ad_distributor.objects.get(uid=id)

        data={
            'email': request.data["email"],
        }
        basicdetailsserializer = ad_dis_serializer.update_email_serializer(
                    instance=userdata, data=data, partial=True)
        if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
        else:
            return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
    except:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST) 


# //// Password Update /////    
@api_view(["POST"])
def ad_dis_password_reset(request,id):
    try:
        print(request.POST)
        # userdata = ad_dis_serializer.ad_distributor.objects.get(uid=id)
        
        email=request.POST['pass_reset']
        sender = 'abijithmailforjob@gmail.com'
        password = 'kgqzxinytwbspurf'
        subject = "Marriyo client password"
        content = f"""
        PasswordResetform : {f"http://localhost:8001/ad_dis_password_reset/{id}"}
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

@api_view(["POST"])
def ad_dis_password_update(request,id):
    try:
        userdata =  ad_dis_serializer.ad_distributor.objects.get(uid=id)

        data={
            'password': request.POST["password"],
        }
        basicdetailsserializer = ad_dis_serializer.update_password_serializer(
                    instance=userdata, data=data, partial=True)
        if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
        else:
            return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
    except:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)


# //// Ads Status = "Closed" /////
@api_view(["POST"])
def ad_dis_status_close(request,id):
    try:
        userdata = ad_dis_serializer.Create_ads.objects.get(ad_id=id)

        data={
            'status':"Closed",
        }
        basicdetailsserializer = ad_dis_serializer.update_status_serializer(
                    instance=userdata, data=data, partial=True)
        if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
        else:
            return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
    except:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)



# //// Ads Status = "Deactive" /////
@api_view(["POST"])  
def ad_dis_deactive_update(request,id):
    userdata = ad_dis_serializer.Create_ads.objects.get(ad_id = id)
    data={
            'status':"Deactive",
        }
    basicdetailsserializer = ad_dis_serializer.update_status_serializer(
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
        userdata = ad_dis_serializer.Create_ads.objects.get(ad_id = renew)

        data={  'days_required' : request.POST['days_required'],
                'status': "Active",
            }
        
        basicdetailsserializer = ad_dis_serializer.status_active_serializer(
                        instance=userdata, data=data, partial=True)
        if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
        else:
            return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)


# // distributor data ////   
def ad_dis_my_data(request,id):
    if request.method == 'GET':
       allDataa = models.ad_distributor.objects.filter(uid=id)
       alldataserializer = ad_dis_serializer.addistributorSerializer(allDataa,many=True)
    return Response(data=alldataserializer.data, status=status.HTTP_200_OK)



# //// Users/////
@api_view(['POST'])
def ad_dis_add_user(request,id):
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
                serializer_validate = ad_dis_serializer.edit_user_Serializer(
                        instance=allData, data=data, partial=True)
                if serializer_validate.is_valid():
                    serializer_validate.save()
                    print("Valid Data")

                    return Response({"edited Data"}, status=status.HTTP_200_OK)

            else:
                allData = ad_distributor.objects.all().values()
                for i in allData:
                    if request.POST['email'] == i['email']:
                        return Response({"User already Exixts"}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
                    else:
                        pass

                data={
                    'uid':ad_dis_extension.id_generate(),
                    'first_name': request.POST['first_name'],
                    'last_name':request.POST['last_name'],
                        'email': request.POST['email'],
                        'mobile':request.POST['mobile'],
                            'password': request.POST['password'],
                                'access_Privileges': json.dumps(request.POST.getlist('access_Privileges')),
                                    'work': request.POST['work'],
                                    'creator':request.POST['creator'],
                                    # 'location':request.POST['location']

                }
                print(data)
                myclientserializer = ad_dis_serializer.add_user_Serializer( data=data)
                if myclientserializer.is_valid():
                    myclientserializer.save()
                    print("Valid Data")

                    return Response({"valid Data"}, status=status.HTTP_200_OK)

    except:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def ad_dis_my_users_data(request,id):
    if request.method == 'GET':
       allDataa = users.objects.filter(creator = id)
       alldataserializer = ad_dis_serializer.add_user_Serializer(allDataa,many=True)
    return Response(data=alldataserializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def ad_dis_single_users_data(request,id):
    if request.method == 'GET':
       allDataa = users.objects.filter(uid = id)
       alldataserializer = ad_dis_serializer.add_user_Serializer(allDataa,many=True)
    return Response(data=alldataserializer.data, status=status.HTTP_200_OK)



# //// Forget password/////
@api_view(['POST'])
def ad_dis_forget_password(request):
   
    if request.method == "POST":        
        print(request.POST)
        userdata1 = ad_dis_serializer.ad_distributor.objects.get(email=request.POST['email'])
        userdata = ad_dis_serializer.ad_distributor.objects.filter(email=request.POST['email']).values()[0]
        user_id=userdata['uid']
        data = {   
             'email':request.POST['email'],
                    'otp1': ad_dis_extension.otp_generate()
                    }
            
        print(data)
        dataserializer = ad_dis_serializer.update_otp_serializer(data=data, instance=userdata1,partial=True)
        print(dataserializer)
        if dataserializer.is_valid():
            print("done")
            dataserializer.save()
            print("Valid Data")
            ad_dis_extension.send_mail_password(data['email'], data['otp1'])
            print("Email send")
            return Response(userdata['uid'], status=status.HTTP_200_OK)
        else:
            return Response({"serializer Issue"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({"Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)           
             
@api_view(['POST'])
def ad_dis_forget_password_otp(request, id):
    try:

            try:
                if ad_dis_extension.validate_otp1(id, int(request.data['user_otp1'])):
                    try:
                        print("userotp",request.data['user_otp1'])
                        userSpecificData = models.ad_distributor.objects.get(uid=id)
                        print(userSpecificData)
                        serializer_validate = ad_dis_serializer.OTP1Serializer(
                            instance=userSpecificData, data=request.POST, partial=True)
                        if serializer_validate.is_valid():
                            print("done")
                            serializer_validate.save()
                            print("Valid OTP")
                            if ad_dis_extension.verify_forget_otp(id):
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

# Coin Value Updation    
@api_view(['POST'])
def update_coin_value(request,id):
    allDataa = ad_dis_serializer.Create_ads.objects.get(ad_id=id)
    alldataserializer = ad_dis_serializer.list_ads_Serializer(allDataa,many=False)
    serialized_data = alldataserializer.data
    print(serialized_data['no_views'])
    no_of_views = serialized_data['no_views']

    # for i in range(0,len(no_of_views)):
    if no_of_views != None:  
            
        if int(no_of_views) >= 4:
            views=int(no_of_views) / 4
            coin=math.ceil(views)
            # commission=(coin * 10)//5
        else:
            coin=0
            # commission=0
   

        data = {'coin' : coin,
                # 'commission':commission,
                }
        
        basicdetailsserializer = ad_dis_serializer.update_coin_serializer(
        instance=allDataa, data=data, partial=True)
        if basicdetailsserializer.is_valid():
            print("valid")
            basicdetailsserializer.save()
            return Response("coin Added", status=status.HTTP_200_OK)
        else:
            return Response("no data", status=status.HTTP_404_NOT_FOUND)