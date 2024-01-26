from django.shortcuts import render
from django.http import HttpResponse,JsonResponse


from virtualExpert import pm_serializer,hm_serializer
from apiapp.models import ProfileFinder
from virtualExpert.models import Profilemanager,hiringmanager,users
from virtualExpert import pm_extension

from rest_framework.decorators import api_view,renderer_classes,permission_classes
from rest_framework.response import Response
from rest_framework import status,generics

from django.core.files.storage import FileSystemStorage
from django.db.models import Q
import requests
import json
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated,AllowAny
import yagmail
import datetime

jsondec = json.decoder.JSONDecoder()
# Create your views here.
all_image_url = "http://127.0.0.1:3000/"
@api_view(['GET'])
def pm_myid(request,id):
    if request.method == 'GET':
        # allDataa = pm_serializer.Profilemanager.objects.all()
        allDataa = pm_serializer.Profilemanager.objects.filter(uid = id)
        alldataserializer = pm_serializer.ProfilemanagerSerializer(allDataa,many=True)
    return Response(data=alldataserializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def pm_signup(request):
    try:
        try:
            if pm_extension.validate_email(request.data['email']):
                return Response("User Already Exists", status=status.HTTP_302_FOUND)
            else:
                x = datetime.datetime.now()
                datas = {
                    'email': request.data["email"],
                    'mobile': request.data["mobile"],
                    'password': request.data["password"],
                    'uid': pm_extension.id_generate(),
                    'otp': pm_extension.otp_generate(),
                    'created_date':str(x.strftime("%d"))+" "+str(x.strftime("%B"))+","+str(x.year)
                }
                print(datas)
                
                dataserializer = pm_serializer.SignupSerializer(data=datas)
                print(datas['uid'])
                if dataserializer.is_valid():
                    dataserializer.save()
                    print("Valid Data")
                    pm_extension.send_mail(datas['email'], datas['otp'])
                    print("Email send")
                    return Response(datas['uid'], status=status.HTTP_200_OK)
                else:
                    return Response({"Bad Request"}, status=status.HTTP_403_FORBIDDEN)
        except:
            return Response({"Invalid Json Format (OR) Invalid Key"}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({"Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def pm_otp(request, id):
    try:
        try:
            if pm_extension.validate_otp(id, int(request.data['user_otp'])):
                try:
                    userSpecificData = Profilemanager.objects.get(uid=id)
                    print(userSpecificData)
                    serializer_validate = pm_serializer.OTPSerializer(
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
def pm_signin(request):
    try:
        print("hello")
        try:
            if pm_extension.validate_email(request.data['email']):
                if pm_extension.verify_user(request.data['email'], request.data['password']):
                    if pm_extension.verify_user_otp(request.data['email']):
                        if pm_extension.get_user_id(request.data['email']):
                            return Response(pm_extension.get_user_id(request.data['email']), status=status.HTTP_200_OK)
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
def pm_profile_picture(request,id):
    try:
        print(request.FILES['profile_picture'])
        fs = FileSystemStorage()
        userdata = pm_serializer.Profilemanager.objects.get(uid=id)
        id_card = str(request.FILES['profile_picture']).replace(" ", "_")
        print(id_card)
        print(id)
        path = fs.save(f"virtual_expert/profile_manager/{id}/profile_picture/"+id_card, request.FILES['profile_picture'])

        # full_path = "http://54.159.186.219:8000"+fs.url(path)
        full_path = all_image_url+fs.url(path)
        print(full_path)

        data = {          
            'profile_picture': full_path
           
        }

        print(data)
        basicdetailsserializer = pm_serializer.profile_picture_Serializer(
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
def pm_complete_account(request,id):
    try:
        print(request.POST)
        # fs = FileSystemStorage()
        userdata = pm_serializer.Profilemanager.objects.get(uid=id)
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
            'notary': request.POST['notary'],           
            # 'id_card': full_path
           
        }
        print(data)
        
        
        basicdetailsserializer = pm_serializer.upload_acc_Serializer(
            instance=userdata, data=data, partial=True)
        if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            #hiring manager
            userdata1 = hiringmanager.objects.get(uid= request.POST['notary'])
            hm_data = hiringmanager.objects.filter(uid= request.POST['notary']).values()[0]
            pm_userdata = pm_serializer.Profilemanager.objects.filter(uid=id).values()[0]
           
            if hm_data['my_profile_manager'] == None:
                my_profile_manager = []
                print("new")
                my_profile_manager.append(pm_userdata)
            else:
                print("add")
                my_profile_manager = jsondec.decode(hm_data['my_profile_manager'])
                # print(my_profile_add)
                my_profile_manager.append(pm_userdata)
            data1={
                'my_profile_manager': json.dumps(my_profile_manager)
            }
            print(data1)
            hmdetailsserializer = hm_serializer.my_profile_manager_Serializer(
            instance=userdata1, data=data1, partial=True)
            if hmdetailsserializer.is_valid():
                hmdetailsserializer.save()
                print("valid data")
                return Response(id, status=status.HTTP_200_OK)
            else:
                return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
        
        
    except:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def pm_edit_account(request,id):
    try:
        print(request.POST)
        print(request.FILES)
        fs = FileSystemStorage()
        userdata = pm_serializer.Profilemanager.objects.get(uid=id)
        userdataa = pm_serializer.Profilemanager.objects.filter(uid=id).values()[0]
        if "profile_picture" in request.FILES:
            id_card = str(request.FILES['profile_picture']).replace(" ", "_")
            path = fs.save(f"virtual_expert/profile_manager/{id}/profile_picture/"+id_card, request.FILES['profile_picture'])
    
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
            'notary': request.POST['notary'],           
            'profile_picture': full_path
           
        }

        print(data)
        basicdetailsserializer = pm_serializer.edit_acc_Serializer(
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
def all_pm_data(request):
    if request.method == 'GET':
       allDataa = pm_serializer.Profilemanager.objects.all()
       alldataserializer = pm_serializer.ProfilemanagerSerializer(allDataa,many=True)
    return Response(data=alldataserializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def pm_my_data(request,id):
    if request.method == 'GET':
       allDataa = pm_serializer.Profilemanager.objects.filter(uid = id)
       alldataserializer = pm_serializer.ProfilemanagerSerializer(allDataa,many=True)
    return Response(data=alldataserializer.data, status=status.HTTP_200_OK)

@api_view(['POST','GET'])
def my_clients(request,id):
    try:
        if request.method == 'GET':
            alldata = Profilemanager.objects.filter(uid=id).values()[0]

            # gender = alldata[0]['gender']
            # requestdataa = serializer.sender_list.objects.filter(sender_uid = id)
            # requestdata = serializer.sender_list.objects.filter(sender_uid = id).values()
            # received = requestdata[0]['received_uid']
            # print(received)
            my_investigator_id = alldata['my_client']
            print(my_investigator_id)
            
            if str(my_investigator_id) == "None":
                print("none")
                request_sent= ""
                print(request_sent)
                rec_dict = {}
                rec_dict[id] = request_sent 
                print(rec_dict)
            else:
                jsonDec = json.decoder.JSONDecoder()
                print("something else")
                received_uid_list = jsonDec.decode(my_investigator_id)
                print(received_uid_list)
                allinvestigator_users=ProfileFinder.objects.all().values()
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
                    get_Selected = allinvestigator_users[numb]
                    find_position = jsonDec.decode(get_Selected['my_manager']).index(id)
                    get_Selected['complaints'] = jsonDec.decode(get_Selected['complaints'])[find_position]
                    get_Selected['complaints_replay'] = jsonDec.decode(get_Selected['complaints_replay'])[find_position]
                    # print(get_Selected['uid'],get_Selected['rating'],get_Selected['feedback'])
                    # get_Selected['action'] = requestdata[0]['action'][1:-2].replace("'","").replace(" ","").split(",")[i]
                    request_sent.append(get_Selected)
                    # print(request_sent)
              
                rec_dict = {}
                rec_list = []
                for x in request_sent:
                    # rec = {}
                    # rec['received_uid'] = x
                    rec_list.append(x)
                rec_dict[id] = rec_list 
            print(rec_dict)
            
            

            # # print(requestdata[0]['action'][1:-2].replace("'","").replace(" ","").split(","))
            return JsonResponse(rec_dict)
            # # requestdataserializer = serializer.SenderSerializer(requestdataa,many=True)
            # # return Response(data=requestdataserializer.data, status=status.HTTP_200_OK)

        if request.method == "POST":
            print(request.POST)
            userdataa =  Profilemanager.objects.filter(uid=request.POST['pm_id']).values()[0]
            # print(type(userdataa.my_client))
            # print(userdataa.my_client)
            userdata = Profilemanager.objects.get(uid=request.POST['pm_id'])
            print(userdata)
    #neww
            if userdataa["my_client"] is None:
                print("new")
                data={
                'my_client':json.dumps(request.POST["pf_id"].split()),
            }
   #replace 
            # elif request.POST["pf_id"] in userdataa["my_client"]:
            #     print("replace")
            #     replace = userdataa["my_client"][1:-2].replace("'","").replace(" ","").split(",")
            #     position = replace.index(request.POST["pf_id"])
            #     print(position)
            #     replace[position] = request.POST["pf_id"]
            #     data={
            #         'my_client':str(replace),
            # }
    #adding
            else:
                jsonDec = json.decoder.JSONDecoder()
                print("Add")
                add =  jsonDec.decode(userdataa["my_client"])
                add.append(request.POST["pf_id"])
                data={
                    'my_client':json.dumps(add),
            }
            print(data)
            myclientserializer = pm_serializer.my_client_serializer(
                instance=userdata, data=data, partial=True)
            if myclientserializer.is_valid():
                myclientserializer.save()
                print("Valid Data")
            
                return Response(id, status=status.HTTP_200_OK)

        else:
            return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
    except:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def pf_status(request,id):
    try:
        if request.method == "POST":
            print(request.POST)
            userdata = ProfileFinder.objects.get(uid = request.POST['uid'])
            userdata.status = request.POST['status']
            userdata.reason = request.POST['reason']
            userdata.save()
            print("Valid Data")
            return Response({"valid Data"}, status=status.HTTP_200_OK)

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
                print(allData)
                data={
                    'first_name': request.POST['first_name'],
                    'last_name':request.POST['last_name'],
                        'email': request.POST['email'],
                        'mobile':request.POST['mobile'],
                            'password': request.POST['password'],
                                'access_Privileges': json.dumps(request.POST.getlist('access_Privilegess')),
                            
                }
                print(data)
                serializer_validate = pm_serializer.eedit_user_Serializer(
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
                single_Data = Profilemanager.objects.filter(uid = request.POST['creator']).values()[0]
                print(single_Data['my_client'])
                if single_Data['my_client'] == None:
                    my_client = "[]"
                else:
                    my_client = single_Data['my_client']
                data={
                    'aid':request.POST['creator'],
                    'uid':pm_extension.id_generate(),
                    'first_name': request.POST['first_name'],
                    'last_name':request.POST['last_name'],
                        'email': request.POST['email'],
                        'mobile':request.POST['mobile'],
                            'password': request.POST['password'],
                                'access_Privileges': json.dumps(request.POST.getlist('access_Privilegess')),
                                    'work': request.POST['work'],
                                    'my_client':my_client,
                                    # 'location':request.POST['location']


                }
                print(data)
                myclientserializer = pm_serializer.add_used_Serializer(data=data)
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
       alldataserializer = pm_serializer.add_used_Serializer(allDataa,many=True)
    return Response(data=alldataserializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def single_users_data(request,id):
    if request.method == 'GET':
       allDataa = users.objects.filter(uid = id)
       alldataserializer = pm_serializer.add_used_Serializer(allDataa,many=True)
    return Response(data=alldataserializer.data, status=status.HTTP_200_OK)



# //// Email Updation ////
@api_view(["POST"])
def pm_email_update(request,id):
    try:
        userdata =  pm_serializer.Profilemanager.objects.get(uid=id)

        data={
            'email': request.data["email"],
        }
        basicdetailsserializer = pm_serializer.update_email_serializer(
                    instance=userdata, data=data, partial=True)
        if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
        else:
            return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
    except:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST) 

# //// Password Reset////
@api_view(["POST"])
def pm_password_reset(request,id):
    try:
        print(request.POST)
        # userdata = ad_pro_serializer.ad_provider.objects.get(uid=id)
        
        email=request.POST['pass_reset']
        sender = 'abijithmailforjob@gmail.com'
        password = 'kgqzxinytwbspurf'
        subject = "Marriyo client password"
        content = f"""
        PasswordResetform : {f"http://localhost:8001/pm_password_reset/{id}"}
        """
        yagmail.SMTP(sender, password).send(
            to=email,
            subject=subject,
            contents=content
        )
        print("send email")

    except:
        return Response("nochange")
    
# /// new password updation////   
@api_view(["POST"])
def pm_password_update(request,id):
    try:
        userdata =  pm_serializer.Profilemanager.objects.get(uid=id)

        data={
            'password': request.POST["password"],
        }
        basicdetailsserializer = pm_serializer.update_password_serializer(
                    instance=userdata, data=data, partial=True)
        if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
        else:
            return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
    except:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)


# /// Forget password ////
@api_view(['POST'])
def pm_forget_password(request): 
    if request.method == "POST":        
        print(request.POST)
        userdata1 = pm_serializer.Profilemanager.objects.get(email=request.POST['email'])
        userdata = pm_serializer.Profilemanager.objects.filter(email=request.POST['email']).values()[0]
        user_id=userdata['uid']
        data = {   
             'email':request.POST['email'],
                    'otp1': pm_extension.otp_generate()
                    }
            
        print(data)
        dataserializer = pm_serializer.update_otp_serializer(data=data, instance=userdata1,partial=True)
        print(dataserializer)
        if dataserializer.is_valid():
            print("done")
            dataserializer.save()
            print("Valid Data")
            pm_extension.send_mail_password(data['email'], data['otp1'])
            print("Email send")
            return Response(userdata['uid'], status=status.HTTP_200_OK)
        else:
            return Response({"serializer Issue"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({"Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)           
      
@api_view(['POST'])
def pm_forget_password_otp(request, id):
    try:

            try:
                if pm_extension.validate_otp1(id, int(request.data['user_otp1'])):
                    try:
                        print("userotp",request.data['user_otp1'])
                        userSpecificData = pm_serializer.Profilemanager.objects.get(uid=id)
                        print(userSpecificData)
                        serializer_validate = pm_serializer.OTP1Serializer(
                            instance=userSpecificData, data=request.POST, partial=True)
                        if serializer_validate.is_valid():
                            print("done")
                            serializer_validate.save()
                            print("Valid OTP")
                            if pm_extension.verify_forget_otp(id):
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