from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from apiapp.models import ProfileFinder,private_investigator
from virtualExpert.models import hiringmanager,Profilemanager,salesmanager,ad_provider,ad_distributor,affliate_marketing
from superadmin.models import superadmin_data,emra_coin,subscription,commision,third_party_user,pi_performance_calculation,insentives_settings,pi_settings,external_expenses
from superadmin import serializer
from superadmin import extension
from django.core.files.storage import FileSystemStorage
from datetime import datetime
import datetime
import json
import yagmail
from virtualExpert import hm_extension
from virtualExpert import hm_serializer
# from apiapp.models import *
# from virtualExpert.models import *

from rest_framework.decorators import api_view,renderer_classes,permission_classes
from rest_framework import status,generics
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

all_image_url = "http://127.0.0.1:3000/"
# Create your views here.



@api_view(['POST'])
def signin(request):
    try:
        try:
            print(request.data)
            allData = superadmin_data.objects.all()
            print(allData)
            if extension.validate_email(request.data['email']):
                print("valid email")
                if extension.verify_user(request.data['email'], request.data['password']):
                        print("valid user")
                    # if hm_extension.verify_user_otp(request.data['email']):
                        return Response(extension.get_user_id(request.data['email']), status=status.HTTP_200_OK)
                    # else:
                    #     return Response({"Didn't Completed OTP Verification"}, status=status.HTTP_401_UNAUTHORIZED)
                else:
                    return Response({"Password Is Incorrect"}, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({"User Dosn't Exits"}, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response({"Invalid Json Format (OR) Invalid Key"}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({"Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def my_data(request,id):
    if request.method == 'GET':
       allDataa = superadmin_data.objects.filter(id=id)
       alldataserializer = serializer.superadminSerializer(allDataa,many=True)
    return Response(data=alldataserializer.data, status=status.HTTP_200_OK)

@api_view(['POST','GET'])
def emra_coin_add(request,id):
    try:
        if request.method == 'GET':
            allDataa = emra_coin.objects.all()
            print(allDataa.values())
            # alldataserializer = serializer.emra_coin_all_Serializer(allDataa,many=True)
            return Response(data=allDataa.values(), status=status.HTTP_200_OK)
        if request.method == "POST":
            if "delete" in request.POST:
                data = emra_coin.objects.get(id=id)
                data.delete()
                return Response("Delete Data", status=status.HTTP_200_OK)
            elif "edit" in request.POST:
                print(request.POST)
                data = emra_coin.objects.get(id=id)
                print(data)
                data.country = request.POST['country']
                data.currency = request.POST['currency']
                data.emra_coin_value =  request.POST['emra_coin_value']
                data.save()
                return Response("Edit Data", status=status.HTTP_200_OK)
            else:
                print(request.POST)
                data = {
                'country':request.POST['country'],
                'currency':request.POST['Currency'],
                'emra_coin_value':request.POST['emra_coin_value']
                }
                print(data)
                dataserializer = serializer.emra_coin_Serializer(data=data)
                if dataserializer.is_valid():
                    dataserializer.save()
                    print("Valid Data")
                    return Response("Valid Data", status=status.HTTP_200_OK)
                else:
                    return Response("srializer issue ", status=status.HTTP_400_BAD_REQUEST)

    except:
        return Response({"Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST','GET'])
def external_expenses_add(request,id):
    try:
        if request.method == 'GET':
            allDataa = external_expenses.objects.all().values()
            return Response(data=allDataa, status=status.HTTP_200_OK)
            # alldataserializer = serializer.emra_coin_all_Serializer(allDataa,many=True)
            # return Response(data=alldataserializer.data, status=status.HTTP_200_OK)
        if request.method == "POST":
            fs = FileSystemStorage()
            print(request.POST)
            if "delete" in request.POST: 
                data = external_expenses.objects.get(id=request.POST['delete'])
                data.delete()
                return Response("Delete Data", status=status.HTTP_200_OK)
            elif "edit" in request.POST:
                # print(request.POST)
                data = external_expenses.objects.get(id=request.POST['edit'])
                data.details = request.POST['details']
                data.to = request.POST['to']
                data.date =  request.POST['date']
                data.currency =  request.POST['currency']
                data.amount =  request.POST['amount']
                data.frequency =  request.POST['frequency']
                if "attachment" in request.FILES:
                    fs = FileSystemStorage()
                    id_card = str(request.FILES['attachment']).replace(" ", "_")
                    path = fs.save(f"superadmin/{id}/External_expenses/"+id_card, request.FILES['attachment'])
                    full_path = all_image_url+fs.url(path)
                    data.attachment = full_path
                data.save()
                return Response("Edit Data", status=status.HTTP_200_OK)
            else:
                print(request.POST)
                print(request.FILES)
                
                id_card = str(request.FILES['attachment']).replace(" ", "_")
                path = fs.save(f"superadmin/{id}/External_expenses/"+id_card, request.FILES['attachment'])
                full_path = all_image_url+fs.url(path)
                data = {
                'details':request.POST['details'],
                'to':request.POST['to'],
                'date':request.POST['date'],
                'currency':request.POST['currency'],
                'amount':request.POST['amount'],
                'frequency':request.POST['frequency'],
                'attachment':full_path

                }
                print(data)
                dataserializer = serializer.external_expenses_Serializer(data=data)
                if dataserializer.is_valid():
                    dataserializer.save()
                    print("Valid Data")
                    return Response("Valid Data", status=status.HTTP_200_OK)
                else:
                    return Response("srializer issue ", status=status.HTTP_400_BAD_REQUEST)

    except:
        return Response({"Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST','delete'])
def public_user_delete(request,id):
    try:
        if request.method == "POST":
                print(request.POST)
                data = ProfileFinder.objects.get(uid=request.POST['delete'])
                # data.delete()
                print(data)
                return Response("Delete Data", status=status.HTTP_200_OK)
        else:
            return Response("srializer issue ", status=status.HTTP_400_BAD_REQUEST)

    except:
        return Response({"Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST','delete'])
def hirirng_user_delete(request,id):
    try:
        if request.method == "POST":
                print(request.POST)
                data = hiringmanager.objects.get(uid=request.POST['delete'])
                data.delete()
                print(data)
                return Response("Delete Data", status=status.HTTP_200_OK)
        else:
            return Response("srializer issue ", status=status.HTTP_400_BAD_REQUEST)

    except:
        return Response({"Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST','delete'])
def profile_user_delete(request,id):
    try:
        if request.method == "POST":
                print(request.POST)
                data = Profilemanager.objects.get(uid=request.POST['delete'])
                # data.delete()
                print(data)
                return Response("Delete Data", status=status.HTTP_200_OK)
        else:
            return Response("srializer issue ", status=status.HTTP_400_BAD_REQUEST)

    except:
        return Response({"Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST','delete'])
def sales_user_delete(request,id):
    try:
        if request.method == "POST":
                print(request.POST)
                data = salesmanager.objects.get(uid=request.POST['delete'])
                # data.delete()
                print(data)
                return Response("Delete Data", status=status.HTTP_200_OK)
        else:
            return Response("srializer issue ", status=status.HTTP_400_BAD_REQUEST)

    except:
        return Response({"Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST','delete'])
def pi_user_delete(request,id):
    try:
        if request.method == "POST":
                print(request.POST)
                data = private_investigator.objects.get(uid=request.POST['delete'])
                # data.delete()
                print(data)
                return Response("Delete Data", status=status.HTTP_200_OK)
        else:
            return Response("srializer issue ", status=status.HTTP_400_BAD_REQUEST)

    except:
        return Response({"Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST','delete'])
def adpro_user_delete(request,id):
    try:
        if request.method == "POST":
                print(request.POST)
                data = ad_provider.objects.get(uid=request.POST['delete'])
                # data.delete()
                print(data)
                return Response("Delete Data", status=status.HTTP_200_OK)
        else:
            return Response("srializer issue ", status=status.HTTP_400_BAD_REQUEST)

    except:
        return Response({"Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST','delete'])
def addis_user_delete(request,id):
    try:
        if request.method == "POST":
                print(request.POST)
                data = ad_distributor.objects.get(uid=request.POST['delete'])
                # data.delete()
                print(data)
                return Response("Delete Data", status=status.HTTP_200_OK)
        else:
            return Response("srializer issue ", status=status.HTTP_400_BAD_REQUEST)

    except:
        return Response({"Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET','POST'])
def subscriptionN(request,id):
    try:       
        if request.method == 'GET':
                    allDataa = subscription.objects.all()
                    alldataserializer = serializer.subscription_all_Serializer(allDataa,many=True)
                    return Response(data=alldataserializer.data, status=status.HTTP_200_OK)
        if request.method == "POST":
            if "delete" in request.POST:
                data = subscription.objects.get(id=id)
                data.delete()
                return Response("Delete Data", status=status.HTTP_200_OK)
            elif "edit" in request.POST:
                print(request.POST)
                data = emra_coin.objects.get(id=id)
                print(data)
                data.country = request.POST['country']
                data.currency = request.POST['currency']
                data.emra_coin_value =  request.POST['emra_coin_value']
                data.save()
                return Response("Edit Data", status=status.HTTP_200_OK)
            else:
                print(request.POST)
                # Validity_from = request.POST['Validity_from']
                # Validity_to = request.POST['Validity_to']
                # print(Validity_from)
                # print(Validity_to)
                # Convert the date strings to datetime objects
                # date_obj1 = datetime.strptime(Validity_from, '%Y-%m-%d')
                # date_obj2 = datetime.strptime(Validity_to, '%Y-%m-%d')
                # days_difference = (date_obj2 - date_obj1).days
                # print(days_difference)
                # if days_difference <= 30:
                #     calcu = f"{int(days_difference)}"+" "+"days"
                # else:
                #     calcu = f"{int(days_difference/30)}"+ " "+"months"
                # print(calcu)
                if request.POST['Amount_with_ad'] == "":
                    Amount_with_ad = 0
                else:
                    Amount_with_ad = request.POST['Amount_with_ad']
                if request.POST['Amount_without_ad'] == "":
                    Amount_without_ad = 0
                else:
                    Amount_without_ad = request.POST['Amount_without_ad']
                if request.POST['value1'] == "":
                    value1 = "None"
                else:
                    value1 = request.POST['value1']
                if request.POST['value2'] == "":
                    value2 ="None"
                else:
                    value2 = request.POST['value2']
                if request.POST['value3'] == "":
                    value3 = "None"
                else:
                    value3 = request.POST['value3']
                data = {
                'Subscription_Country':request.POST['Subscription_Country'],
                'Title_of_the_plan':request.POST['Title_of_the_plan'],
                'Type_Of_Subscription':request.POST['Type_Of_Subscription'],
                 'Amount_with_ad':Amount_with_ad,
                'Amount_without_ad':Amount_without_ad,
                'Validity':request.POST['Validity'],
                # 'Validity_from':request.POST['Validity_from'],
                #  'Validity_to':request.POST['Validity_to'],
                'Option1':request.POST['Option1'],
                'value1':value1,
                 'Option2':request.POST['Option2'],
                'value2':value2,
                'Option3':request.POST['Option3'],
                'value3':value3,
                # 'duration':calcu,
                }
                # print(data)
                dataserializer = serializer.subscription_Serializer(data=data)
                if dataserializer.is_valid():
                    if request.POST['Amount_with_ad'] == "":
                        dataserializer.validated_data['Amount_with_ad'] =None
                    if request.POST['Amount_without_ad'] == "":
                        dataserializer.validated_data['Amount_without_ad'] =None
                    if request.POST['value1'] == "":
                        dataserializer.validated_data['value1'] =None
                    if request.POST['value2'] == "":
                        dataserializer.validated_data['value2'] =None
                    if request.POST['value3'] == "":
                        dataserializer.validated_data['value3'] =None
                    dataserializer.save()
                    print("Valid Data")
                    return Response("Valid Data", status=status.HTTP_200_OK)
        else:
            return Response("srializer issue ", status=status.HTTP_400_BAD_REQUEST)

    except:
        return Response({"Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST','GET'])
def single_subscriptionN(request,id,sid):
    try:       
        if request.method == 'GET':
                    print(sid)
                    allDataa = subscription.objects.filter(id = sid).values()
                    # print(allDataa)
                    # alldataserializer = serializer.subscription_all_Serializer(allDataa,many=True)
                    return Response(data=allDataa[0], status=status.HTTP_200_OK)
        elif request.method == "POST":
                print(request.POST)
                print(sid)
                data = subscription.objects.get(id=sid)
                print(data)
                data.Subscription_Country = request.POST['Subscription_Country']
                data.Title_of_the_plan=request.POST['Title_of_the_plan']
                data.Type_Of_Subscription=request.POST['Type_Of_Subscription']
                
                if str(request.POST['Amount_with_ad']) == "None":
                    pass
                else:
                    data.Amount_with_ad = request.POST['Amount_with_ad']
                if str(request.POST['Amount_without_ad']) == "None":
                    pass
                else:
                    data.Amount_without_ad = request.POST['Amount_with_ad']
                    
                data.Validity=request.POST['Validity']
                data.Option1=request.POST['Option1']
                if str(request.POST['value1']) == "None":
                    pass
                else:
                    data.value1 = request.POST['value1']
                data.Option2=request.POST['Option2']
                if str(request.POST['value2']) == "None":
                    pass
                else:
                    data.value2 = request.POST['value2']
                data.Option3=request.POST['Option3']
                if str(request.POST['value3']) == "None":
                    pass
                else:
                    data.value3 = request.POST['value3']
                data.save()
                print("valid data")
                return Response(" Data Edited", status=status.HTTP_200_OK)
        else:
            return Response("srializer issue ", status=status.HTTP_400_BAD_REQUEST)

    except:
        return Response({"Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET','POST'])
def commisionn(request,id):
    try:
        if request.method == 'GET':
                    allDataa = commision.objects.all()
                    alldataserializer = serializer.commision_all_Serializer(allDataa,many=True)
                    return Response(data=alldataserializer.data, status=status.HTTP_200_OK)

        if request.method == "POST":
                print(request.POST)
                if "add" in request.POST:
                    dataserializer = serializer.commision_Serializer(data=request.POST)
                    if dataserializer.is_valid():
                        dataserializer.save()
                        print("valid data")
                        return Response("Valid Data", status=status.HTTP_200_OK)
                elif "delete" in request.POST:
                    data = commision.objects.get(id = request.POST['delete'])
                    data.delete()
                    return Response(" Data Deleted", status=status.HTTP_200_OK)
                else:
                    print("edit")
                    data = commision.objects.get(id = id)
                    print(data)
                    dataserializer = serializer.commision_Serializer(data=request.POST, instance=data)
                    if dataserializer.is_valid():
                        dataserializer.save()
                        print("valid data")
                
                return Response(" Data Edited", status=status.HTTP_200_OK)
        else:
            return Response("srializer issue ", status=status.HTTP_400_BAD_REQUEST)

    except:
        return Response({"Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET','POST'])
def single_commisionn(request,id):
    try:
        if request.method == 'GET':
                    allDataa = commision.objects.filter(id = id).values()
                    print(allDataa)
                    # alldataserializer = serializer.commision_all_Serializer(allDataa,many=True)
                    return Response(data=allDataa[0], status=status.HTTP_200_OK)
    except:
        return Response({"Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET','POST'])
def third_party_userrr(request,id):
    try:
        if request.method == 'GET':
                    allDataa = third_party_user.objects.all()
                    alldataserializer = serializer.third_party_user_all_serializer(allDataa,many=True)
                    return Response(data=alldataserializer.data, status=status.HTTP_200_OK)

        if request.method == "POST":
                print(request.POST)
                if "add" in request.POST:
                    allData = third_party_user.objects.all().values()
                    print(allData)
                    for i in allData:
                        print(i['email'])
                        if request.POST['email'] == i['email']:
                            return Response({"User already Exixts"}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
                        else:
                            pass
                    data={}
                    for x in request.POST.keys():
                        data[x] = request.POST[x]
                    data.pop("access_privilage")
                    data.pop("add")
                    data.pop("csrfmiddlewaretoken")
                    data["access_privilage"] = json.dumps(request.POST.getlist('access_privilage'))
                    print(data)
                    print("ata")
                    dataserializer = serializer.third_party_user_serializer(data=data)
                    if dataserializer.is_valid():
                        dataserializer.save()
                        print("valid data")
                        return Response("Valid Data", status=status.HTTP_200_OK)
                elif "delete" in request.POST:
                    print("delete")
                    uid = request.POST['delete']
                    data = third_party_user.objects.get(id = uid)
                    print(data)
                    data.delete()
                    return Response(" Data Deleted", status=status.HTTP_200_OK)
                else:
                    print("edit")
                    print(request.POST)
                    uid = request.POST['edit']
                    print(uid)
                    data1 = third_party_user.objects.get(id = id)
                    print(data1)
                    data={}
                    for x in request.POST.keys():
                        data[x] = request.POST[x]
                    data.pop("access_privilage")
                    data.pop("edit")
                    data["access_privilage"] = json.dumps(request.POST.getlist('access_privilage'))
                    # data['creator'] = id
                    print(data)
                    dataserializer = serializer.third_party_user_serializer(data=data, instance=data1)
                    if dataserializer.is_valid():
                        dataserializer.save()
                        print("valid data")
                
                return Response(" Data Edited", status=status.HTTP_200_OK)
        else:
            return Response("srializer issue ", status=status.HTTP_400_BAD_REQUEST)

    except:
        return Response({"Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET','POST'])
def single_third_party_userrr(request,id):
        try:
            if request.method == 'GET':
                    allDataa = third_party_user.objects.filter(id = id).values()
                    # alldataserializer = serializer.third_party_user_serializer(allDataa,many=True)
                    return Response(data=allDataa[0], status=status.HTTP_200_OK)
        except:
            return Response({"Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def all_complaint_list(request,id):
    try:
            if request.method == 'GET':
                    allDataa = ProfileFinder.objects.all().values()
                    all_complaints = {}
                    for i in allDataa:
                        if i["complaints"] != None and  "empty" not in i["complaints"]:
                            list = []
                            list.append(i)
                    all_complaints['data'] = list
                    print(all_complaints)
                    return JsonResponse(all_complaints)
                    # alldataserializer = serializer.profile_manager_serializer(all_complaints,many=True)
                    # return Response(data=alldataserializer, status=status.HTTP_200_OK)
    except:
            return Response({"Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@api_view(['GET','POST'])
def incentive_settingss(request,id):
    try:
            if request.method == 'GET':
                dataa = insentives_settings.objects.filter(id = 1).values()
                return Response(data=dataa[0], status=status.HTTP_200_OK)
            if request.method == 'POST':
                data = insentives_settings.objects.get(id = 1)
                print(request.POST)
                sales_target = request.POST['sales_target']
                Incentives_Amount_INR = request.POST['Incentives_Amount_INR']
                Incentives_Amount_USD = request.POST['Incentives_Amount_USD']
                data.sales_target = sales_target
                data.Incentives_Amount_INR = Incentives_Amount_INR
                data.Incentives_Amount_USD = Incentives_Amount_USD
                data.save()
                return Response({"Valid data"}, status=status.HTTP_200_OK)
    except:
            return Response({"Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@api_view(['GET','POST'])
def pi_settingss(request,id):
    try:
            if request.method == 'GET':
                dataa = pi_settings.objects.filter(id = 1).values()
                return Response(data=dataa[0], status=status.HTTP_200_OK)
            if request.method == 'POST':
                data = pi_settings.objects.get(id = 1)
                print(request.POST)
                default_amount = request.POST['default_amount']
                to_Admin = request.POST['to_Admin']
                to_investigator = request.POST['to_investigator']
                data.default_amount = default_amount
                data.to_Admin = to_Admin
                data.to_investigator = to_investigator
                data.save()
                return Response({"Valid data"}, status=status.HTTP_200_OK)
    except:
            return Response({"Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@api_view(['GET','POST'])
def pi_performance_calculations(request,id):
    try:
            if request.method == 'GET':
                dataa = pi_performance_calculation.objects.filter(id = 1).values()
                return Response(data=dataa[0], status=status.HTTP_200_OK)
            if request.method == 'POST':
                data = pi_performance_calculation.objects.get(id = 1)
                print(request.POST)
                Calculation_Period = request.POST['Calculation_Period']
                default_amount = request.POST['default_amount']
                fifty_Good_Review = request.POST['fifty_Good_Review']
                eighty_Good_Review = request.POST['eighty_Good_Review']
                fifty_bad_Review = request.POST['fifty_bad_Review']
                eighty_bad_Review = request.POST['eighty_bad_Review']
                data.Calculation_Period = Calculation_Period
                data.default_amount = default_amount
                data.fifty_Good_Review = fifty_Good_Review
                data.eighty_Good_Review = eighty_Good_Review
                data.fifty_bad_Review = fifty_bad_Review
                data.eighty_bad_Review = eighty_bad_Review
                data.save()
                return Response({"Valid data"}, status=status.HTTP_200_OK)
    except:
            return Response({"Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@api_view(['POST'])
def super_admin_hm_signup(request):
    try:
        try:
            if hm_extension.validate_email(request.data['email']):
                return Response("User Already Exists", status=status.HTTP_302_FOUND)
            else:
                print(request.POST)
                x = datetime.datetime.now()
                datas = {
                    'email': request.POST["email"],
                    'mobile': request.POST["mobile"],
                    'password': request.POST["password"],
                    'uid': hm_extension.id_generate(),
                    'otp': hm_extension.otp_generate(),
                    'created_date':str(x.strftime("%d"))+" "+str(x.strftime("%B"))+","+str(x.year)
                }
                print(datas)
                dataserializer = serializer.hm_SignupSerializer(data=datas)
                print(datas['uid'])
                if dataserializer.is_valid():
                    dataserializer.save()
                    print("Valid Data")
                    # hm_extension.send_mail(datas['email'], datas['otp'])
                    sender = 'abijithmailforjob@gmail.com'
                    password = 'kgqzxinytwbspurf'
                    subject = "This is Marriyo Sign Up OTP"
                    content = f"""
                    hii : {request.POST['name']}  
                    your email:{datas['email']}
                    your password : {datas['password']}
                    Click Link: {f"http://127.0.0.1:8001/hiring_manager/signin/"}
                    """
                    yagmail.SMTP(sender, password).send(
                        to=datas['email'],
                        subject=subject,
                        contents=content
                    )

                    print("Email send")
                    return Response(datas['uid'], status=status.HTTP_200_OK)
                else:
                    return Response({"Bad Request"}, status=status.HTTP_403_FORBIDDEN)
        except:
            return Response({"Invalid Json Format (OR) Invalid Key"}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({"Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

