from django.shortcuts import render
from django.http import HttpResponse,JsonResponse


from virtualExpert import am_serializer,hm_serializer
from virtualExpert import models
from virtualExpert.models import affliate_marketing,hiringmanager,users
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
from django.db.models import F
# from datetime import datetime
from apiapp import serializer
from apiapp.models import ProfileFinder

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
                print(request.POST)
                x = datetime.datetime.now()
                if "referral_code" in request.POST:
                    referral_code=request.POST["referral_code"]
                else:
                    referral_code="empty"

                datas = {
                    'email': request.POST["email"],
                    'mobile': request.POST["mobile"],
                    'password': request.POST["password"],
                    'uid': am_extension.id_generate(),
                    'otp': am_extension.otp_generate(),
                    'created_time':str(x.strftime("%I:%M %p")),
                    'referral_code':referral_code
                    
                }
                print("data: ",datas)
                dataserializer = am_serializer.SignupSerializer(data=datas)
                print(datas['uid'])
                
                if dataserializer.is_valid():
                    print("done")
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
        print(request.data['user_otp'])
        try:
            if am_extension.validate_otp(id, int(request.data['user_otp'])):
                print("valid")
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
                        if am_extension.get_user_id(request.data['email']):
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
        jsondec = json.decoder.JSONDecoder()

        fs = FileSystemStorage()
        userdata = models.affliate_marketing.objects.get(uid=id)
       
        # id_card = str(request.FILES['id_card']).replace(" ", "_")
        # path = fs.save(f"virtual_expert/affiliate_marketing/{id}/id_card/"+id_card, request.FILES['id_card'])

        # # full_path = "http://54.159.186.219:8000"+fs.url(path)
        # full_path = all_image_url+fs.url(path)
        #degree certificate
        degree_certificate_1 = str(request.FILES['degree_cer']).replace(" ", "_")
        path_deg = fs.save(f"virtual_expert/affiliate_marketing/{id}/degree_certificate/"+degree_certificate_1, request.FILES['degree_cer'])
        full_path_degree = all_image_url+fs.url(path_deg)
         #experience certificate
        if 'ex_cer' in request.FILES:
            ex_certificate_1 = str(request.FILES['ex_cer']).replace(" ", "_")
            path_ex = fs.save(f"virtual_expert/affiliate_marketing/{id}/experience_certificate/"+ex_certificate_1, request.FILES['ex_cer'])
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
            path = fs.save(f"virtual_expert/affiliate_marketing/{id}/gst_certificate/"+gst_certificate_1, request.FILES['gst_certificate'])
            full_path_gst = all_image_url+fs.url(path)
            #pan card
            pan_card_1 = str(request.FILES['pan_card']).replace(" ", "_")
            path1 = fs.save(f"virtual_expert/affiliate_marketing/{id}/pan_card/"+pan_card_1, request.FILES['pan_card'])
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
            'full_name': request.POST['full_name'],
            'personal_country': request.POST['personal_country'],
            'personal_city': request.POST['personal_city'],
            'personal_address': request.POST['personal_address'],
            'hiring_manager': request.POST['hiring_manager'],           
            'hiring_manager': request.POST['hiring_manager'],
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
        basicdetailsserializer = am_serializer.upload_acc_Serializer(
            instance=userdata, data=data, partial=True)
        print(basicdetailsserializer)
        if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            userdata1 = models.hiringmanager.objects.get(uid= request.POST['hiring_manager'])
            hm_data = models.hiringmanager.objects.filter(uid= request.POST['hiring_manager']).values()[0]
            aff_userdata = models.affliate_marketing.objects.filter(uid=id).values()[0]
            aff_userdata.pop('created_date')
            print(aff_userdata)
            if hm_data['affiliate_marketing'] == None:
                affiliate_marketing = []
                print("new")
                affiliate_marketing.append(aff_userdata)
                
            else:
                print("add")
                affiliate_marketing = jsondec.decode(hm_data['affiliate_marketing'])
                # print(my_profile_add)
                affiliate_marketing.append(aff_userdata)
            print(affiliate_marketing)
            data1={
                'affiliate_marketing' : json.dumps(affiliate_marketing)
            }
            print(data1)
            hmdetailsserializer = hm_serializer.affiliate_markting_Serializer(
            instance=userdata1, data=data1, partial=True)
            print(hmdetailsserializer)
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
def all_aff_details(request):
    if request.method == 'GET':
       allDataa = am_serializer.affliate_marketing.objects.all()
       alldataserializer = am_serializer.affliatemarketingSerializer(allDataa,many=True)
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
        PasswordResetform : {f"http://127.0.0.1:3000/password_aff_resett/{id}"}
        """
        yagmail.SMTP(sender, password).send(
            to=email,
            subject=subject,
            contents=content
        )
        print("send email")
        return Response("success",status=status.HTTP_200_OK)
    except:
        return Response("nochange",status=status.HTTP_400_BAD_REQUEST)
 

@api_view(["POST"])
def pass_aff_update(request,id):
    print(request.POST)
    userdata = am_serializer.affliate_marketing.objects.get(uid=id)
    print(userdata)
    if request.POST['password'] == request.POST['confirm_password']:
    

        data={
            'password':request.POST['password']
        }
        print(data)
        basicdetailsserializer = am_serializer.update_pass_aff_serializer(instance=userdata, data=data, partial=True)
        
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
                serializer_validate = am_serializer.affedit_user_Serializer(
                        instance=allData, data=data, partial=True)
                if serializer_validate.is_valid():
                    serializer_validate.save()
                    print("Valid Data")

                    return Response({"edited Data"}, status=status.HTTP_200_OK)

            else:
                allData = users.objects.all().values()  
                for i in allData:
                    if request.POST['email'] == i['email']:
                        return Response({"User already Exixts"}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
                    else:
                        pass

                data={
                    'uid':am_extension.id_generate(),
                    'aid':request.POST['creator'],
                    'first_name': request.POST['first_name'],
                    'last_name':request.POST['last_name'],
                        'email': request.POST['email'],
                        'mobile':request.POST['mobile'],
                            'password': request.POST['password'],
                                'access_Privileges': json.dumps(request.POST.getlist('access_Privileges')),
                                    'work': request.POST['work'],
                                    # 'creator':request.POST['creator'],
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                


                }
                print(data)
                myclientserializer = am_serializer.add_used_Serializer( data=data)
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
       alldataserializer = am_serializer.add_used_Serializer(allDataa,many=True)
    return Response(data=alldataserializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def single_users_data(request,id):
    if request.method == 'GET':
       allDataa = users.objects.filter(uid = id)
       alldataserializer = am_serializer.add_used_Serializer(allDataa,many=True)
    return Response(data=alldataserializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def aff_coin(request,id):
    userdata = am_serializer.affliate_marketing.objects.get(uid=id)
    if request.method == 'POST':
        data={
            'coin':request.POST['coin']
        }
        basicdetailsserializer = am_serializer.aff_coin_serializer(data=data,instance=userdata, partial=True)
        
        if basicdetailsserializer.is_valid():

            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
        else:
            return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
        

@api_view(["POST"])
def aff_forget_password(request):
    if request.method == "POST":        
        print(request.POST)
        userdata1 = am_serializer.affliate_marketing.objects.get(email=request.POST['email'])
        userdata = am_serializer.affliate_marketing.objects.filter(email=request.POST['email']).values()[0]
        user_id=userdata['uid']
        data = {   
            'email':request.POST['email'],
            'otp1': am_extension.otp_generate()
                    }
            
        print(data)
        dataserializer = am_serializer.update_otp_serializer(data=data, instance=userdata1,partial=True)
        print(dataserializer)
        if dataserializer.is_valid():
            print("done")
            dataserializer.save()
            print("Valid Data")
            am_extension.send_mail_password(data['email'], data['otp1'])
            print("Email send")
            return Response(userdata['uid'], status=status.HTTP_200_OK)
        else:
            return Response({"serializer Issue"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({"Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)           
      


@api_view(['POST'])
def aff_forget_password_otp(request,id):
    try:

            try:
                if am_extension.validate_otp1(id, int(request.data['user_otp1'])):
                    try:
                        print("userotp",request.data['user_otp1'])
                        userSpecificData = models.affliate_marketing.objects.get(uid=id)
                        print(userSpecificData)
                        serializer_validate = am_serializer.OTP1Serializer(
                            instance=userSpecificData, data=request.POST, partial=True)
                        if serializer_validate.is_valid():
                            print("done")
                            serializer_validate.save()
                            print("Valid OTP")
                            if am_extension.verify_forget_otp(id):
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

    

# filter w r to  date
@api_view(["POST"])
def date_date(request,id):
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        user = models.affliate_marketing.objects.get(uid=id)

        pf_user=ProfileFinder.objects.filter(referral_code=id).values()
        print(pf_user)
        try:
            pfuser=pf_user[0]['referral_code']
        except:
            pass
        
        referral_code = user.uid
        print(referral_code,"refcode")
        # from_date = datetime.strptime(from_date, "%Y-%m-%d").date()
        # to_date = datetime.strptime(to_date, "%Y-%m-%d").date()
        # pfdata=serializer.ProfileFinder.objects.filter(created_date__range=[from_date,to_date],referral_code=pfuser).values()
        # print(pfdata)
        data=am_serializer.affliate_marketing.objects.filter(created_date__range=[from_date,to_date],referral_code=referral_code).values()
        print(data)
        # date_data={
        #     'data':data,
        #     # 'pfdata':pfdata,
            
        # }
        return Response((data),status=status.HTTP_200_OK)
    

@api_view(['GET'])
def my_profile_finder_data(request):
    if request.method == 'GET':
       allDataa = serializer.ProfileFinder.objects.all()
       alldataserializer = serializer.ProfileFinderSerializer(allDataa,many=True)
    return Response(data=alldataserializer.data, status=status.HTTP_200_OK)
