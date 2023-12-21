from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,JsonResponse


from virtualExpert import sm_serializer,hm_serializer
from virtualExpert import models
from virtualExpert.models import salesmanager
from virtualExpert import sm_extension

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


# Create your views here.
all_image_url = "http://127.0.0.1:3000/"
@api_view(['POST'])
def sm_signup(request):
    try:
        try:
            if sm_extension.validate_email(request.data['email']):
                return Response("User Already Exists", status=status.HTTP_302_FOUND)
            else:
                x = datetime.datetime.now()
                datas = {
                    'email': request.data["email"],
                    'mobile': request.data["mobile"],
                    'password': request.data["password"],
                    'uid': sm_extension.id_generate(),
                    'otp': sm_extension.otp_generate(),
                    'created_date':str(x.strftime("%d"))+" "+str(x.strftime("%B"))+","+str(x.year)
                }
                print(datas)
                dataserializer = sm_serializer.SignupSerializer(data=datas)
                print(datas['uid'])
                if dataserializer.is_valid():
                    dataserializer.save()
                    print("Valid Data")
                    sm_extension.send_mail(datas['email'], datas['otp'])
                    print("Email send")
                    return Response(datas['uid'], status=status.HTTP_200_OK)
                else:
                    return Response({"Bad Request"}, status=status.HTTP_403_FORBIDDEN)
        except:
            return Response({"Invalid Json Format (OR) Invalid Key"}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({"Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def sm_otp(request, id):
    try:
        try:
            if sm_extension.validate_otp(id, int(request.data['user_otp'])):
                try:
                    userSpecificData = models.salesmanager.objects.get(uid=id)
                    print(userSpecificData) 
                    serializer_validate = sm_serializer.OTPSerializer(
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
def sm_signin(request):

    try:
        try:
            if sm_extension.validate_email(request.data['email']):
                if sm_extension.verify_user(request.data['email'], request.data['password']):
                    if sm_extension.verify_user_otp(request.data['email']):
                        return Response(sm_extension.get_user_id(request.data['email']), status=status.HTTP_200_OK)
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
def sm_profile_picture(request,id):
    try:
        print(request.FILES['profile_picture'])
        fs = FileSystemStorage()
        userdata = sm_serializer.salesmanager.objects.get(uid=id)
        profile_picture = str(request.FILES['profile_picture']).replace(" ", "_")
        print(profile_picture)
        print(id)
        path = fs.save(f"virtual_expert/sales_manager/{id}/profile_picture/"+profile_picture, request.FILES['profile_picture'])

        # full_path = "http://54.159.186.219:8000"+fs.url(path)
        full_path = all_image_url+fs.url(path)
        print(full_path)

        data = {          
            'profile_picture': full_path
           
        }

        print(data)
        basicdetailsserializer = sm_serializer.profile_picture_Serializer(
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
def sm_upload_account(request,id):
    
    try:
        jsondec = json.decoder.JSONDecoder()
        # fs = FileSystemStorage()
        userdata = sm_serializer.salesmanager.objects.get(uid=id)
        # id_card = str(request.FILES['id_card']).replace(" ", "_")
        # path = fs.save(f"virtual_expert/sales_manager/{id}/id_card/"+id_card, request.FILES['id_card'])

        # # full_path = "http://54.159.186.219:8000"+fs.url(path)
        # full_path = all_image_url+fs.url(path)

        data = {
            'full_name': request.POST['full_name'],
            'personal_country': request.POST['personal_country'],
            'personal_city': request.POST['personal_city'],
            'personal_address': request.POST['personal_address'],
            'hiring_manager': request.POST['hiring_manager']          
            # 'id_card': full_path
           
        }

        print(data)
        basicdetailsserializer = sm_serializer.upload_acc_Serializer(
            instance=userdata, data=data, partial=True)
        if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            #hiring manager
            userdata1 = models.hiringmanager.objects.get(uid= request.POST['hiring_manager'])
            hm_data = models.hiringmanager.objects.filter(uid= request.POST['hiring_manager']).values()[0]
            sm_userdata = models.salesmanager.objects.filter(uid=id).values()[0]
            print(sm_userdata)
            if hm_data['sales_manager'] == None:
                sales_manager = [] = []
                print("new")
                sales_manager.append(sm_userdata)
            else:
                print("add")
                sales_manager = jsondec.decode(hm_data['sales_manager'])
                # print(my_profile_add)
                sales_manager.append(sm_userdata)
            data1={
                'sales_manager': json.dumps(sales_manager)
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

@api_view(['GET'])
def all_sm_data(request):
    if request.method == 'GET':
       allDataa = sm_serializer.salesmanager.objects.all()
       alldataserializer = sm_serializer.salesmanagerSerializer(allDataa,many=True)
    return Response(data=alldataserializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def sm_my_data(request,id):
    if request.method == 'GET':
       allDataa = sm_serializer.salesmanager.objects.filter(uid=id)
       alldataserializer = sm_serializer.salesmanagerSerializer(allDataa,many=True)
    return Response(data=alldataserializer.data, status=status.HTTP_200_OK)
   

@api_view(['POST'])
def sm_edit_data(request,id):
    try:
        print(request.POST)
        print(request.FILES)
        fs = FileSystemStorage()
        userdata = sm_serializer.salesmanager.objects.get(uid=id)
        userdataa = sm_serializer.salesmanager.objects.filter(uid=id).values()[0]
        if "profile_picture" in request.FILES:
            id_card= str(request.FILES['profile_picture']).replace(" ", "_")
            path = fs.save(f"virtual_expert/sales_manager/{id}/profile_picture/"+id_card, request.FILES['profile_picture'])
    
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
        basicdetailsserializer = sm_serializer.update_acc_serializer(
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
def add_client_data(request,id):
    try:
        if 'client_type' in request.POST:
            print(request.POST)
            print(request.FILES)
            fs = FileSystemStorage()
            picture= str(request.FILES['picture']).replace(" ", "_")
            path = fs.save(f"virtual_expert/ad_client/{id}/picture/"+picture, request.FILES['picture'])
            full_path = all_image_url+fs.url(path)
            sales=salesmanager.objects.filter(uid=id).values()[0]
            print(sales)
            
            data = {

                'uid': sm_extension.id_generate(),
                'sales_id':json.dumps(sales),
                'client_type': request.POST['client_type'],
                'client_name': request.POST['client_name'],
                'client_location': request.POST['client_location'],
                'category': request.POST['category'] ,
                'google_map': request.POST['google_map'] ,
                'phone_number': request.POST['phone_number'],
                'email': request.POST['email'],
                'picture':full_path,
                'otp': sm_extension.otp_client_generate(),


                
            }
            print(data)
            basicdetailsserializer = sm_serializer.add_client_serializer(data=data)

            print("done")
            if basicdetailsserializer.is_valid():
                basicdetailsserializer.save()
                sm_extension.send_mail(data['email'], data['otp'])
                print("Email send")
                print("Valid Data")
                return Response(id, status=status.HTTP_200_OK)
            else:
                print("serializers")
                return Response({"sserializer issue"}, status=status.HTTP_403_FORBIDDEN)
        else:
            
            print(request.POST)   

            otp = sm_extension.otp_client_generate()
            print(otp)
            email=request.POST['active']
            sender = 'abijithmailforjob@gmail.com'
            password = 'kgqzxinytwbspurf'
            subject = "Marriyo client OTP"
            content = f"""
            OTP : {otp}
            """
            yagmail.SMTP(sender, password).send(
                to=email,
                subject=subject,
                contents=content
            )
            print("send email")
            # data={
            #     'otp': sm_extension.otp_client_generate(),
            #     'email':request.POST['email']
            # }
            # print(data)
            otp_client=request.POST['user_otp']
            if otp == otp_client:
                # otp_client=request.POST['user_otp']
                print(otp_client)
                basicdetailsserializer = sm_serializer.add_client_serializer(otp=otp)
                print("valid")
                if basicdetailsserializer.is_valid():
                    basicdetailsserializer.save()
                    print("done")
            


    except:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def all_client_data(request):
    if request.method == 'GET':
        allDataa = sm_serializer.ad_client.objects.all()
        alldataserializer = sm_serializer.sm_add_client_serializer(allDataa,many=True)
    return Response(data=alldataserializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def add_client_activities(request,id):
    try:
        # print(request.POST)
        print('hii')
        # print(request.POST)
        
        data = {
            'types_of_activities': request.POST['types_of_activities'],
            'date': request.POST['date'] ,
            'time': request.POST['time'] ,
            'notes': request.POST['notes'],
            
        
        }
        print(data)
        userdata=models.ad_client.objects.get(uid=id)
        # print(userdata)
        basicdetailsserializer = sm_serializer.client_activities_serializer(data=data,instance=userdata, partial=True)
        print("done")
        if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
        else:
            print("serializers")
            return Response({"sserializer issue"}, status=status.HTTP_403_FORBIDDEN)
    except:
        return Response({"invalid"}, status=status.HTTP_403_FORBIDDEN)





@api_view(['POST'])
def client_otp(request, id):
    try:
        try:
            if sm_extension.validate_otp(id, int(request.data['user_otp'])):
                try:
                    userSpecificData = models.ad_client.objects.get(uid=id)
                    print(userSpecificData) 
                    serializer_validate = sm_serializer.OTPclientSerializer(
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





@api_view(['GET'])
def all_activities(request):
    if request.method == 'GET':
        allDataa = sm_serializer.ad_client.objects.all()
        alldataserializer = sm_serializer.all_activities_serializer(allDataa,many=True)
    return Response(data=alldataserializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def view_client_id(request,id):
    if request.method=="GET":
        view_id = sm_serializer.ad_client.objects.filter(uid=id).values()[0]
        alldataserializer = sm_serializer.sm_add_client_serializer(view_id,many=False)
    return Response(data=alldataserializer.data, status=status.HTTP_200_OK)



@api_view(["POST"])
def sendmail(request,id):
    try:
        user=get_object_or_404(models.ad_client,uid=id)
        print(user)
        user.status=True
        user.save()
        return Response("success")
    except:
        return Response("nostatus")


@api_view(['POST'])
def sm_email_update(request,id):
    try:
        userdata = sm_serializer.salesmanager.objects.get(uid=id)

        data={
            'email': request.data["email"],
        }
        basicdetailsserializer = sm_serializer.update_email_serializer(
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
    userdata = sm_serializer.salesmanager.objects.get(uid=id)
    print(userdata)
    if request.POST['password'] == request.POST['confirm_password']:
    

        data={
            'password':request.POST['password']
        }
        print(data)
        basicdetailsserializer = sm_serializer.update_password_serializer(instance=userdata, data=data, partial=True)
        
        if basicdetailsserializer.is_valid():

            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
        else:
            return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)