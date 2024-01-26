from django.shortcuts import render
from django.http import HttpResponse,JsonResponse

from apiapp import pi_serializer,serializer
from apiapp import models
from virtualExpert import models
from apiapp.models import private_investigator
from virtualExpert import hm_serializer

# Create your views here.

from rest_framework.decorators import api_view,renderer_classes,permission_classes
from rest_framework.response import Response
from rest_framework import status,generics
from apiapp import pi_extension


from django.core.files.storage import FileSystemStorage
from django.db.models import Q
import requests
import json
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated,AllowAny
import json
import datetime
import yagmail

jsondec = json.decoder.JSONDecoder()
all_image_url = "http://127.0.0.1:3000/"
@api_view(['POST'])
def signup(request):
    try:
        try:
            if pi_extension.validate_email(request.data['email']):
                return Response("User Already Exists", status=status.HTTP_302_FOUND)
            else:
                x = datetime.datetime.now()
                datas = {
                    'email': request.data["email"],
                    'mobile': request.data["mobile"],
                    'password': request.data["password"],
                    # 'referral_code': code,
                    'uid': pi_extension.id_generate(),
                    'otp': pi_extension.otp_generate(),
                    'created_date':str(x.strftime("%d"))+" "+str(x.strftime("%B"))+","+str(x.year)
                }
                dataserializer = pi_serializer.SignupSerializer(data=datas)
                print(datas['uid'])
                
                if dataserializer.is_valid():
                    dataserializer.save()
                    print("Valid Data")
                    pi_extension.send_mail(datas['email'], datas['otp'])
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
            if pi_extension.validate_otp(id, int(request.data['user_otp'])):
                try:
                    userSpecificData = models.private_investigator.objects.get(uid=id)
                    serializer_validate = pi_serializer.OTPSerializer(
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
            if pi_extension.validate_email(request.data['email']):
                if pi_extension.verify_user(request.data['email'], request.data['password']):
                    if pi_extension.verify_user_otp(request.data['email']):
                        return Response(pi_extension.get_user_id(request.data['email']), status=status.HTTP_200_OK)
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
def profilePicture(request, id):
    try:
        userdata = pi_serializer.private_investigator.objects.get(uid=id)
        print(userdata)
        print(request.FILES['profile_picture'])

        id_card = str(request.FILES['profile_picture']).replace(" ", "_")

        fs = FileSystemStorage()
        path = fs.save(f"private_investigator/{id}/profile_picture/"+id_card,
        request.FILES['profile_picture'])
        # full_path = "http://54.159.186.219:8000"+fs.url(path)
        full_path = all_image_url+fs.url(path)
        data = {
            "profile_picture": full_path
        }
        profilepictureserializer = pi_serializer.ProfilePictureSerializer(
            instance=userdata, data=data, partial=True)
        if profilepictureserializer.is_valid():
            profilepictureserializer.save()
            print("valid data")
            return Response(id, status=status.HTTP_200_OK)
    except:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def pi_complete_account(request,id):
    try:
        # fs = FileSystemStorage()
        userdata = pi_serializer.private_investigator.objects.get(uid=id)
        # id_card = str(request.FILES['id_card']).replace(" ", "_")
        # path = fs.save(f"private_investigator/{id}/id_card/"+id_card, request.FILES['id_card'])

        # # full_path = "http://54.159.186.219:8000"+fs.url(path)
        # full_path = all_image_url+fs.url(path)
        if 'personal_city' in request.POST:
            personal_city = request.POST['personal_city']
        else:
            personal_city = "empty"
        data = {
            #  'office_name': request.POST['office_name'],
            # 'office_country': request.POST['office_country'],
            # 'office_city': request.POST['office_city'],
            # 'office_address': request.POST['office_address'],
            'first_name': request.POST['first_name'],
            'last_name': request.POST['last_name'],
            'personal_country': request.POST['personal_country'],
            'personal_city': personal_city,
            'personal_address': request.POST['personal_address'],
            'hiring_manager': request.POST['hiring_manager'],
            'tagline': request.POST['tagline'],                  
            # 'id_card': full_path
           
        }
        print(data)
        basicdetailsserializer = pi_serializer.upload_acc_Serializer(
            instance=userdata, data=data, partial=True)
        if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            userdata1 = models.hiringmanager.objects.get(uid= request.POST['hiring_manager'])
            hm_data = models.hiringmanager.objects.filter(uid= request.POST['hiring_manager']).values()[0]
            ad_pro_userdata = private_investigator.objects.filter(uid=id).values()[0]
            if hm_data['private_investigator'] == None:
                my_ad_provider = []
                print("new")
                my_ad_provider.append(ad_pro_userdata)
            else:
                print("add")
                my_ad_provider = jsondec.decode(hm_data['private_investigator'])
                # print(my_profile_add)
                my_ad_provider.append(ad_pro_userdata)
            data1={
                'private_investigator': json.dumps(my_ad_provider)
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
def pi_edit_account(request,id):
    try:
        print(request.POST)
        print(request.FILES)

        fs = FileSystemStorage()
        userdata = pi_serializer.private_investigator.objects.get(uid=id)
        userdataa = pi_serializer.private_investigator.objects.filter(uid=id).values()[0]
        print(userdataa)
#id card 
        if "id_card" in request.FILES:
            id_card = str(request.FILES['id_card']).replace(" ", "_")
            path = fs.save(f"private_investigator/{id}/id_card/"+id_card, request.FILES['id_card'])
    
            # full_path = "http://54.159.186.219:8000"+fs.url(path)
            full_path = all_image_url+fs.url(path)
        else:
            full_path = userdataa['id_card']
        print(full_path)
#profile picture
        if "profile_picture" in request.FILES:

            id_card1 = str(request.FILES['profile_picture']).replace(" ", "_")
    
            fs = FileSystemStorage()
            path1 = fs.save(f"private_investigator/{id}/profile_picture/"+id_card1,
            request.FILES['profile_picture'])
            # full_path = "http://54.159.186.219:8000"+fs.url(path)
            full_path1 = all_image_url+fs.url(path1)
        else:
            full_path1 = userdataa['profile_picture']

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
            'hiring_manager': request.POST['hiring_manager'],
            'tagline': request.POST['tagline'],                      
            'id_card': full_path,
            'profile_picture': full_path1

           
        }
        print(data)
        basicdetailsserializer = pi_serializer.edit_acc_Serializer(
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
def all_pi_data(request):
    if request.method == 'GET':
       allDataa = pi_serializer.private_investigator.objects.all()
       alldataserializer = pi_serializer.PrivateinvestigatorSerializer(allDataa,many=True)
    return Response(data=alldataserializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def pi_my_data(request,id):
    if request.method == 'GET':
       allDataa = pi_serializer.private_investigator.objects.filter(uid=id)
       alldataserializer = pi_serializer.PrivateinvestigatorSerializer(allDataa,many=True)
    return Response(data=alldataserializer.data, status=status.HTTP_200_OK)

@api_view(['GET','POST'])
def my_clients(request,id):
    try:
        if request.method == 'GET':
            alldata=pi_serializer.private_investigator.objects.filter(uid=id).values()[0]
            # gender = alldata[0]['gender']
            # requestdataa = serializer.sender_list.objects.filter(sender_uid = id)
            # requestdata = serializer.sender_list.objects.filter(sender_uid = id).values()
            # received = requestdata[0]['received_uid']
            # print(received)
            my_investigator_id = alldata['my_client']
            # print(my_investigator_id)
            
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
                received_uid_list = my_investigator_id[1:-2].replace("'","").replace(" ","").split(",")
                print(received_uid_list)
                allinvestigator_users=serializer.ProfileFinder.objects.all().values()
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
                    find_position = get_Selected['my_investigator'][1:-2].replace("'","").replace(" ","").split(",").index(id)
                    get_Selected['feedback'] = get_Selected['feedback'][1:-2].replace("'","").replace(" ","").split(",")[find_position]
                    get_Selected['rating'] = get_Selected['rating'][1:-1].replace("'","").replace(" ","").split(",")[find_position]
                    get_Selected['Questin'] = jsonDec.decode(get_Selected['Questin'])[find_position]
                    get_Selected['answer'] = jsonDec.decode(get_Selected['answer'])[find_position]
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
            userdataa =  pi_serializer.private_investigator.objects.filter(uid=request.POST['pi_id']).values()[0]
            # print(type(userdataa.my_client))
            # print(userdataa.my_client)
            userdata = pi_serializer.private_investigator.objects.get(uid=request.POST['pi_id'])
            print(userdata)
    #neww
            if userdataa["my_client"] is None:
                print("new")
                data={
                'my_client':str(request.POST["pf_id"].split()),
                'all_ratings':str("empty".split())
            }
   #replace 
            elif request.POST["pf_id"] in userdataa["my_client"]:
                print("replace")
                replace = userdataa["my_client"][1:-2].replace("'","").replace(" ","").split(",")
                position = replace.index(request.POST["pf_id"])
                print(position)
                replace[position] = request.POST["pf_id"]
                data={
                    'my_client':str(replace),
            }
    #adding
            else:
                print("Add")
                add = userdataa["my_client"][1:-2].replace("'","").replace(" ","").split(",")
                all_rate = userdataa['all_ratings'][1:-2].replace("'","").replace(" ","").split(",")
                add.append(request.POST["pf_id"])
                all_rate.append("empty")
                data={
                    'my_client':str(add),
                    'all_ratings':str(all_rate)
            }
            print(data)
            myclientserializer = pi_serializer.my_client_serializer(
                instance=userdata, data=data, partial=True)
            if myclientserializer.is_valid():
                myclientserializer.save()
                print("Valid Data")
            
                return Response(id, status=status.HTTP_200_OK)

        else:
            return Response({"sserializer issue"}, status=status.HTTP_403_FORBIDDEN)
    except:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
def total_ratings(request,id):
    my_clients = requests.get(f"http://127.0.0.1:3000/pi_my_clients/{id}").json()
    print(my_clients)
    return Response(id, status=status.HTTP_200_OK)

# email update
@api_view(['POST'])
def pi_email_update(request,id):
    try:
        userdata = pi_serializer.private_investigator.objects.get(uid=id)

        data={
            'email': request.data["email"],
        }
        basicdetailsserializer = pi_serializer.update_email_serializer(
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
        PasswordResetform : {f"http://localhost:8001/privateinvest_password_reset/{id}"}
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
def pass_privateInvestigator_update(request,id):
    print(request.POST)
    userdata = pi_serializer.private_investigator.objects.get(uid=id)
    print(userdata)
    if request.POST['password'] == request.POST['confirm_password']:
    
        data={
            'password':request.POST['password']
        }
        print(data)
        basicdetailsserializer = pi_serializer.update_password_serializer(instance=userdata, data=data, partial=True)
        if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
        else:
            return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
        


# pi forgetpassword
        
@api_view(['POST'])
def pi_forget_password(request): 
    if request.method == "POST":        
        print(request.POST)
        userdata1 = pi_serializer.private_investigator.objects.get(email=request.POST['email'])
        userdata = pi_serializer.private_investigator.objects.filter(email=request.POST['email']).values()[0]
        user_id=userdata['uid']
        data = {   
            'email':request.POST['email'],
            'otp1': pi_extension.otp_generate()
                    }
            
        print(data)
        dataserializer = pi_serializer.update_otp_serializer(data=data, instance=userdata1,partial=True)
        print(dataserializer)
        if dataserializer.is_valid():
            print("done")
            dataserializer.save()
            print("Valid Data")
            pi_extension.send_mail_password(data['email'], data['otp1'])
            print("Email send")
            return Response(userdata['uid'], status=status.HTTP_200_OK)
        else:
            return Response({"serializer Issue"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({"Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)           
      
    

@api_view(['POST'])
def pi_forget_password_otp(request, id):
    try:

            try:
                if pi_extension.validate_otp1(id, int(request.data['user_otp1'])):
                    try:
                        print("userotp",request.data['user_otp1'])
                        userSpecificData = private_investigator.objects.get(uid=id)
                        print(userSpecificData)
                        serializer_validate = pi_serializer.OTP1Serializer(
                            instance=userSpecificData, data=request.POST, partial=True)
                        if serializer_validate.is_valid():
                            print("done")
                            serializer_validate.save()
                            print("Valid OTP")
                            if pi_extension.verify_forget_otp(id):
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
