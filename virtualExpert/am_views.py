from django.shortcuts import render
from django.http import HttpResponse,JsonResponse


from virtualExpert import am_serializer,hm_serializer
from virtualExpert import models
from virtualExpert.models import affliate_marketing,hiringmanager
from virtualExpert import am_extension

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
def am_signup(request):
    try:
        try:
            if am_extension.validate_email(request.data['email']):
                return Response("User Already Exists", status=status.HTTP_302_FOUND)
            else:
                x = datetime.datetime.now()
                datas = {
                    'email': request.data["email"],
                    'mobile': request.data["mobile"],
                    'password': request.data["password"],
                    'uid': am_extension.id_generate(),
                    'otp': am_extension.otp_generate(),
                    'created_date':str(x.strftime("%d"))+" "+str(x.strftime("%B"))+","+str(x.year)
                }
                print(datas)
                dataserializer = am_serializer.SignupSerializer(data=datas)
                print(datas['uid'])
                if dataserializer.is_valid():
                    dataserializer.save()
                    print("Valid Data")
                    am_extension.send_mail(datas['email'], datas['otp'])
                    print("Email send")
                    return Response(datas['uid'], status=status.HTTP_200_OK)
                else:
                    return Response({"Bad Request"}, status=status.HTTP_403_FORBIDDEN)
        except:
            return Response({"Invalid Json Format (OR) Invalid Key"}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({"Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def am_otp(request, id):
    try:
        try:
            if am_extension.validate_otp(id, int(request.data['user_otp'])):
                try:
                    userSpecificData = models.affliate_marketing.objects.get(uid=id)
                    print(userSpecificData)
                    serializer_validate = am_serializer.OTPSerializer(
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
def am_signin(request):
    try:
        try:
            if am_extension.validate_email(request.data['email']):
                if am_extension.verify_user(request.data['email'], request.data['password']):
                    if am_extension.verify_user_otp(request.data['email']):
                        return Response(am_extension.get_user_id(request.data['email']), status=status.HTTP_200_OK)
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
def am_profile_picture(request,id):
    try:
        print(id)
        print(request.FILES['profile_picture'])
        fs = FileSystemStorage()
        userdata = am_serializer.affliate_marketing.objects.get(uid=id)
        
        id_card = str(request.FILES['profile_picture']).replace(" ", "_")
        print(id_card)
        print(id)
        path = fs.save(f"virtual_expert/affiliate_marketing/{id}/profile_picture/"+id_card, request.FILES['profile_picture'])

        # full_path = "http://54.159.186.219:8000"+fs.url(path)
        full_path = all_image_url+fs.url(path)
        print(full_path)

        data = {          
            'profile_picture': full_path
           
        }

        print(data)
        basicdetailsserializer = am_serializer.profile_picture_Serializer(
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
def am_upload_account(request,id):
    try:
        # fs = FileSystemStorage()
        userdata = am_serializer.affliate_marketing.objects.get(uid=id)
        # id_card = str(request.FILES['id_card']).replace(" ", "_")
        # path = fs.save(f"virtual_expert/affiliate_marketing/{id}/id_card/"+id_card, request.FILES['id_card'])

        # # full_path = "http://54.159.186.219:8000"+fs.url(path)
        # full_path = all_image_url+fs.url(path)

        data = {
            'full_name': request.POST['full_name'],
            'personal_country': request.POST['personal_country'],
            'personal_city': request.POST['personal_city'],
            'personal_address': request.POST['personal_address'],
            'hiring_manager': request.POST['hiring_manager'],          
            # 'id_card': full_path

           
        }

        print(data)
        basicdetailsserializer = am_serializer.upload_acc_Serializer(
            instance=userdata, data=data, partial=True)
        if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            userdata1 = models.hiringmanager.objects.get(uid= request.POST['hiring_manager'])
            hm_data = models.hiringmanager.objects.filter(uid= request.POST['hiring_manager']).values()[0]
            ad_pro_userdata = models.affliate_marketing.objects.filter(uid=id).values()[0]
            if hm_data['affiliate_marketing'] == None:
                my_ad_provider = []
                print("new")
                my_ad_provider.append(ad_pro_userdata)
            else:
                print("add")
                my_ad_provider = jsondec.decode(hm_data['affiliate_marketing'])
                # print(my_profile_add)
                my_ad_provider.append(ad_pro_userdata)
            data1={
                'affiliate_marketing': json.dumps(my_ad_provider)
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




@api_view(['GET'])
def all_aff_data(request):
    if request.method == 'GET':
       allDataa = am_serializer.affliate_marketing.objects.all()
       alldataserializer = am_serializer.am_all_serializer(allDataa,many=True)
    return Response(data=alldataserializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def my_aff_data(request,id):
    if request.method == 'GET':
       allDataa = am_serializer.affliate_marketing.objects.filter(uid=id)
       alldataserializer = am_serializer.affliatemarketingSerializer(allDataa,many=True)
    return Response(data=alldataserializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def am_edit_account(request,id):
    try:
        print(request.POST)
        print(request.FILES)
        fs = FileSystemStorage()
        userdata = am_serializer.affliate_marketing.objects.get(uid=id)
        userdataa = am_serializer.affliate_marketing.objects.filter(uid=id).values()[0]
        if "profile_picture" in request.FILES:
            profile_picture= str(request.FILES['profile_picture']).replace(" ", "_")
            path = fs.save(f"virtual_expert/affliate_marketing/{id}/profile_picture/"+profile_picture, request.FILES['profile_picture'])
    
            # full_path = "http://54.159.186.219:8000"+fs.url(path)
            full_path = all_image_url+fs.url(path)
        else:
            full_path = userdataa['profile_picture']
        print("valid")

        data = {

            'full_name': request.POST['full_name'],
            'personal_country': request.POST['personal_country'],
            'personal_city': request.POST['personal_city'],
            'personal_address': request.POST['personal_address'],
            'profile_picture': full_path
           
        }

        print(data)
        basicdetailsserializer = am_serializer.update_acc_serializer(
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
def aff_email_update(request,id):
    try:
        userdata = am_serializer.affliate_marketing.objects.get(uid=id)

        data={
            'email': request.data["email"],
        }
        basicdetailsserializer = am_serializer.update_email_serializer(
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
def password_reset(request,id):
    try:
        print(request.POST)
        # userdata = am_serializer.affliate_marketing.objects.get(uid=id)
        
        email=request.POST['pass_reset']
        sender = 'abijithmailforjob@gmail.com'
        password = 'kgqzxinytwbspurf'
        subject = "Marriyo client password"
        content = f"""
        PasswordResetform : {f"http://localhost:8001/password_reset/{id}"}
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
def pass_update(request,id):
    print(request.POST)
    userdata = am_serializer.affliate_marketing.objects.get(uid=id)
    print(userdata)
    if request.POST['password'] == request.POST['confirm_password']:
    

        data={
            'password':request.POST['password']
        }
        print(data)
        basicdetailsserializer = am_serializer.update_password_serializer(instance=userdata, data=data, partial=True)
        
        if basicdetailsserializer.is_valid():

            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
        else:
            return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
def af_my_data(request,id):
    if request.method == 'GET':
       allDataa = models.affliate_marketing.objects.filter(uid=id)
       alldataserializer = am_serializer.affliatemarketingSerializer(allDataa,many=True)
    return Response(data=alldataserializer.data, status=status.HTTP_200_OK)

