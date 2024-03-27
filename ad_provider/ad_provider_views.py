from django.shortcuts import render,redirect
from django.contrib.auth import logout
from django.http import JsonResponse,HttpResponse
from collections import Counter
import requests
from datetime import datetime,date
from django.contrib import messages
import json
import math

jsondec = json.decoder.JSONDecoder()
# Create your views here.
def dashboard(request):
    return render(request,"dashboard.html")

def createaccount(request):
    neww=[]
    response = requests.get('https://api.first.org/data/v1/countries').json()
    all = requests.get('https://countriesnow.space/api/v0.1/countries/states').json()
    states = json.dumps(all["data"])
    al = (all["data"])
    for x in al:
        name = (x.get("name"))
        neww.append(name)
    countryname = json.dumps(neww)

    context = {'response': response, 'region': response,'all':al,
                                            'country': countryname,'states': states,}

    return render(request,"ad_pro_createaccount.html",context)

def signup(request):
    error = ""
    if request.method == "POST":
        if request.POST['password'] == request.POST['confirm_password']:
            # response = requests.post('http://54.159.186.219:8000/signup/',data=request.POST)
            response = requests.post("http://127.0.0.1:3000/ad_pro_signup/",data=request.POST)
            print(response.status_code)
            print(response.text)
            uidd = (response.text[1:-1])
            print(uidd)
            if response.status_code == 200:
                return redirect(f"/ad_provider/otp/{uidd}")
            elif response.status_code == 302:
                error = "User Already Exist"                
                return redirect("/ad_provider/signin/")                    
            else:
                pass
        else:
            print("password doesn't match")
    context = {'error':error}
    return render(request,"ad_provider_signup.html",context)

def signin(request):
    value = request.COOKIES.get('ad_provider')
    print(value)
    error = ""
    context = {'error':error}
    if request.method == "POST":
        print(request.POST)
        # response = requests.post("http://54.159.186.219:8000/signin/",data=request.POST)
        response = requests.post("http://127.0.0.1:3000/ad_pro_signin/",data=request.POST)
        print(response.status_code)
#        print(type(jsondec.decode(response.text)))
 #       print(jsondec.decode(response.text))
        uidd =jsondec.decode( response.text)
        global access_Privileges
        try:
            access_Privileges = uidd['access_Privileges']
            uid = uidd['uid']
        except:
            access_Privileges = ""
            uid = uidd
        print(access_Privileges)
        print("main/user")
        if response.status_code == 200:
            mydata = requests.get(f"http://127.0.0.1:3000/ad_pro_my_data/{uid}").json()[0]
            user_otp = mydata.get('user_otp')
            if user_otp is not None:
                id_card_data = mydata.get('id_card')
                hm=mydata.get('hiring_manager')
                if id_card_data is None:
                    if hm is not None:
                        alert_message="You are under Verification Process...."
                        context['alert_message'] = alert_message
                        return render(request,"ad_provider_signin.html",context)
                        
                    else:
                        return redirect(f"/ad_provider/upload_acc/{uid}")
                
                elif id_card_data is not None:
                    res = redirect(f"/ad_provider/ad_provider_admin_dashboard/{uid}")
                    res.set_cookie("Ad_Provider",uid)
                    return res
                
            elif user_otp is None:
                delete_hm = requests.delete("http://127.0.0.1:3000/ad_pro_delete/",data=request.POST)
                if delete_hm.status_code == 204:
                    print("Data deleted successfully")
                elif delete_hm.status_code == 404:
                    print("Data not found")
                else:
                    print("Error occurred:")

            else:
                pass
            # return redirect(f"/hiring_manager/hm_admin_dashboard/{uid}")
        elif response.status_code == 401:
            delete_hm = requests.delete("http://127.0.0.1:3000/ad_pro_delete/",data=request.POST)
            if delete_hm.status_code == 204:
                print("Data deleted")
                error="Not Registered...Please click Create an Account"
            elif delete_hm.status_code == 404:
                print("Data not found")
            else:
                print("Error occurred:", delete_hm.status_code)
        elif response.status_code == 404:
            error="User Doesn't Exists"
        else:
          error = "YOUR EMAILID OR PASSWORD IS INCORRECT"
    context = {'error':error}
    return render(request,"ad_provider_signin.html",context)

def otp(request,id):
    context = {'invalid':"invalid"}
    new=[]
    if request.method == "POST":
        new.append(request.POST["otp1"])
        new.append(request.POST["otp2"])
        new.append(request.POST["otp3"])
        new.append(request.POST["otp4"])
        data = {
            'user_otp':int(''.join(new).strip())
           
        }
        print(data)
        # response = requests.post(f"http://54.159.186.219:8000/otp/{id}",   data=data)
        response = requests.post(f"http://127.0.0.1:3000/ad_pro_otp/{id}", data=data)

       
        print(response)
        print(response.status_code)
        print(data['user_otp'])
        print(response.text)
        uidd = (response.text[1:-1])
        
        if response.status_code == 200:
        # if get["otp"] == data['user_otp']:
            # return redirect(f"/profileidcard/{uidd}")
            return redirect(f"/ad_provider/profile_picture/{uidd}")
        else:
            invalid = "Invalid OTP"
            context = {'invalid':invalid}
    return render(request,"ad_provider_otpcheck.html",context)

def profile_picture(request,id):
    if request.method == "POST":
        print(request.FILES)
        # response = requests.post(f"http://54.159.186.219:8000/profileidcard/{id}",   files=request.FILES)
        response = requests.post(f"http://127.0.0.1:3000/ad_pro_profile_picture/{id}",  files=request.FILES)
        print(response)
        print(response.status_code)
        print(response.text)
        uidd = (response.text[1:-1])
        if response.status_code == 200:
        # if get["otp"] == data['user_otp']:
            return redirect(f"/ad_provider/upload_acc/{uidd}")
        else:
            return HttpResponse("INVALId")
    return render(request,"ad_provider_profilepicture.html")

def upload_acc(request,id):
    try:
        #hiring manager list
        hiring_manager = requests.get("http://127.0.0.1:3000/all_hm_data/").json()
        sales_manager = requests.get("http://127.0.0.1:3000/all_sm_data/").json()
        neww=[]
        response = requests.get('https://api.first.org/data/v1/countries').json()
        all = requests.get('https://countriesnow.space/api/v0.1/countries/states').json()
        states = json.dumps(all["data"])
        al = (all["data"])
        for x in al:
            name = (x.get("name"))
            neww.append(name)
        countryname = json.dumps(neww)

        context = {'response': response, 'region': response,'all':al,
                    'country': countryname,'states': states,'hiring_manager':hiring_manager,
                    'sales_manager' : sales_manager}

        if request.method == "POST":
            uid=request.POST['hiring_manager']
            # print(request.FILES)
            dictio = dict(request.POST)
            print(dictio)
            # response = requests.post(f"http://54.159.186.219:8000/profileidcard/{id}",   files=request.FILES)
            response = requests.post(f"http://127.0.0.1:3000/ad_pro_upload_account/{id}",   data = dictio,files=request.FILES)
            print(response)
            print(response.status_code)
            print(response.text)
            uidd = (response.text[1:-1])
            if response.status_code == 200:
                data={
                        'noter_id':id,
                        'not_message':"{id} selected you as his/her Hiring Manager",
                        'notify_id': uid,
                    }
                notify=requests.post("http://127.0.0.1:3000/notification_update/",data=data)
                if notify.status_code == 200:
                    status_up=requests.post(f"http://127.0.0.1:3000/pm_notify_status_true/{uid}")
                    print(status_up.status_code)
            # if get["otp"] == data['user_otp']:

                return redirect("/ad_provider/signin/")
            else:
                pass
        return render(request,"ad_ptovider_upload_acc.html",context)
    except:
        return render(request,"ad_ptovider_upload_acc.html")

def logout_view(request):
    value = request.COOKIES.get('ad_provider')
    print(value)
    response = redirect("/ad_provider/signin/")
    # response = HttpResponse("delete cookie")
    response.delete_cookie("ad_provider")
    return response
# //// Ad_pro DashBoard //////
def admin_dashboard(request,id):
    value = request.COOKIES.get('ad_provider')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/ad_provider/signin/")
    jsondec=json.decoder.JSONDecoder()
    new=[]
    type=[]
    try:
        mydata = requests.get(f"http://127.0.0.1:3000/ad_pro_my_data/{id}").json()[0]
        idd = id
        access = ""
    except:  
        mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]
        access = mydata['access_Privileges']
        print(mydata['aid'])
        idd = mydata['aid']

    #Notification
    if requests.get(f"http://127.0.0.1:3000/notification_data/{idd}") == None:
        notification=""
        
    else:
        notification = requests.get(f"http://127.0.0.1:3000/notification_data/{idd}")
        notification_data = json.loads(notification.text)

    all_profile_finder = requests.get("http://127.0.0.1:3000/alluserdata/").json()
    all_data=requests.get("http://127.0.0.1:3000/all_pro_ads_data/").json()

    for i in all_data:
        uid=jsondec.decode(i.get("ad_pro"))
        id_value = uid['uid']
        if id_value == idd:
            new.append(i)
            
    for j in new:
        ad_type=j.get("ad_type")
        type.append(ad_type)
    
    print(type)
    word_counts = Counter(type)
    result = [{'word': word, 'count': count} for word, count in word_counts.items()]

    context={
        'key':mydata,
        'current_path':request.get_full_path(),
        'all_profile_finder':all_profile_finder[::-1],
        'all_data':new,
        'result': result,
        'user_access': "",
        'notification' : notification_data
    }
    
    for dict_data in all_data:
        status=dict_data['status']
        if status == 'Active':
            end_date=dict_data['days_required']
            ads_id=dict_data['ad_id']
            last_date= datetime.strptime(end_date, "%Y-%m-%d")
            if last_date <= datetime.today():
                print(ads_id)
                response = requests.post(f"http://127.0.0.1:3000/ad_pro_deactive_update/{ads_id}",data=request.POST )
                print(response)

    return render(request,"ad_provider_admin_dashboard.html",context)

# //// Profile/Account Details/////
def account(request,id):
    value = request.COOKIES.get('ad_provider')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/ad_provider/signin/")
    try:
        signin(request)
    #     access_Privileges = access_Privileges
    # except:
    #     access_Privileges=""
    finally:

        new=[]
        mydata = requests.get(f"http://127.0.0.1:3000/ad_pro_my_data/{id}").json()[0]
        all_data=requests.get("http://127.0.0.1:3000/all_pro_ads_data/").json() 
        print(id)
        education  = jsondec.decode(mydata['level_education'])
        study = jsondec.decode(mydata['field_study'])
        for i in all_data:
            uid=jsondec.decode(i.get("ad_pro")) 
            id_value = uid['uid']
            if id_value == id:
                new.append(i)
        
        # total_coin = sum(int(item.get('coin', 0)) for item in new) 

        context={
            'key':mydata,
            'education':education,
        'study':study,
            'current_path':request.get_full_path(),
            'user_access' : "",
            'all_data':new,
            # 'total_coin':total_coin,
            'user_access':""
        }

    return render(request,"ad_pro_account.html",context)

def edit_account(request,id):
    value = request.COOKIES.get('ad_provider')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/ad_provider/signin/")
    try:
        mydata = requests.get(f"http://127.0.0.1:3000/ad_pro_my_data/{id}").json()[0]  
        
        neww=[]
        response = requests.get('https://api.first.org/data/v1/countries').json()

        
        all = requests.get('https://countriesnow.space/api/v0.1/countries/states').json()
        # statess = requests.get('https://countriesnow.space/api/v0.1/countries/states').json()
        states = json.dumps(all["data"])
        al = (all["data"])
        for x in al:
           name = (x.get("name"))
           neww.append(name)
        countryname = json.dumps(neww)
    
        context = {'key':mydata,'current_path':request.get_full_path(),
                   'response': response, 'region': response,'all':al,
                    'country': countryname,'states': states,'key':mydata,
                    'current_path':request.get_full_path()}
        
        if request.method == "POST":
            print(request.POST)
            response = requests.post(f"http://127.0.0.1:3000/ad_pro_edit_account/{id}", data = request.POST,files=request.FILES)
            print(response)
            # print(response.status_code)
            # print(response.text)
            return redirect(f"/ad_provider/ad_pro_account/{id}")
    
        return render(request,"ad_pro_editAccount.html",context)
    except:
        return render(request,"ad_pro_editAccount.html")

# /// Ad_provider Account Balance/////
def acc_balance(request,id):
    value = request.COOKIES.get('ad_provider')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/ad_provider/signin/")
    new=[]
    mydata = requests.get(f"http://127.0.0.1:3000/ad_pro_my_data/{id}").json()[0]
    all_data=requests.get("http://127.0.0.1:3000/all_pro_ads_data/").json() 
    print(id)
    for i in all_data:
        uid=jsondec.decode(i.get("ad_pro")) 
        id_value = uid['uid']
        if id_value == id:
            new.append(i)
    for item in new:
        if item['commission'] != None and item['coin'] != None:
            item['amount'] = int(item['coin']) * ((int(item['commission']))/100)
        else:
            item['amount'] = 0
            
          
    # total_coin = sum(int(item.get('coin', 0)) for item in new)

    context={
        'key':mydata,
        'current_path':request.get_full_path(),
        'all_data' : new,
       

    }
    return render(request,"ad_pro_accntBalance.html",context)

def add_funds(request,id):
    value = request.COOKIES.get('ad_provider')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/ad_provider/signin/")
    try:
        mydata = requests.get(f"http://127.0.0.1:3000/ad_pro_my_data/{id}").json()[0]
        idd = id
        access = ""
    except:  
        mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]
        access = mydata['access_Privileges']
        print(mydata['aid'])
        idd = mydata['aid']
    mydata = requests.get(f"http://127.0.0.1:3000/ad_pro_my_data/{id}").json()[0] 
    context={
        'key':mydata,
        'current_path':request.get_full_path(),
         'user_access':access,
        
    }
    return render(request,"ad_pro_adFunds.html",context)

# ///// AD_ Pro Coins/////
def ad_pro_coins(request,id):
    value = request.COOKIES.get('ad_provider')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/ad_provider/signin/")
    try:
        mydata = requests.get(f"http://127.0.0.1:3000/ad_pro_my_data/{id}").json()[0]
        idd = id
        access = ""
    except:  
        mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]
        access = mydata['access_Privileges']
        print(mydata['aid'])
        idd = mydata['aid']
    new=[]
    mydata = requests.get(f"http://127.0.0.1:3000/ad_pro_my_data/{id}").json()[0]
    all_data=requests.get("http://127.0.0.1:3000/all_pro_ads_data/").json() 
    print(id)
    for i in all_data:
        uid=jsondec.decode(i.get("ad_pro")) 
        id_value = uid['uid']
        if id_value == id:
            new.append(i)
    
    total_coin=0
    for item in new:
            if item['coin'] != None:
                total_coin += int(item['coin'])

    print(total_coin)

    context={
        'key':mydata,
        'current_path':request.get_full_path(),
        'all_data' : new,
        'total_coin' : total_coin,
        'user access': access
        
    }

    return render(request,"ad_pro_coins.html",context)

# //// Ad_pro Ads /////
def ads_list_all(request,id):
    value = request.COOKIES.get('ad_provider')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/ad_provider/signin/")
    try:
        mydata = requests.get(f"http://127.0.0.1:3000/ad_pro_my_data/{id}").json()[0]
        idd = id
        access = ""
    except:  
        mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]
        access = mydata['access_Privileges']
        print(mydata['aid'])
        idd = mydata['aid']
    jsondec=json.decoder.JSONDecoder()
    new=[]
    
    all_data=requests.get("http://127.0.0.1:3000/all_pro_ads_data/").json()
    # response= requests.post(f"http://127.0.0.1:3000/update_coin_value/")
    emra_data=requests.get(f"http://127.0.0.1:3000/superadmin/emra_coin/{idd}").json()
    for x in emra_data:
        emra_value=x.get('emra_coin_value')


# append ads_data to new list
    for i in all_data:
        uid=jsondec.decode(i.get("ad_pro"))
        id_value = uid['uid']
        if id_value == idd:
            new.append(i)

#  Emera coin value 
    for item in new:
        if item['coin'] != None:
            item['amount'] = int(item['coin']) * int(emra_value)
        else:
            item['amount'] = 0
        
    
    if request.method == "POST":
        if "detail" in request.POST:
            print(request.POST)
            global ads_id
            ads_id=request.POST['detail']
            print(ads_id)
            return redirect(f"/ad_provider/ad_pro_adDetails/{id}")
        
        elif "edi_ad" in request.POST:
            print(request.POST)
            global dis_id
            dis_id = request.POST['edi_ad']
            print(dis_id)
            return redirect(f"/ad_provider/ad_pro_editAd/{id}")
        
        elif "ad_id" in request.POST:
            print(request.POST)
            filter={
                'f_ad_id': request.POST['ad_id'].strip(),
                'f_ad_name': request.POST['ad_name'].strip().lower(),
                'f_ad_type': request.POST['ad_type'].strip().lower(),
                'f_ad_status': request.POST['ad_status'].strip().lower(),
    
            }
            
            p = set()

            for x in new:
                if (filter['f_ad_id'] == x['ad_id'] or not filter['f_ad_id']) and \
                (filter['f_ad_name'] == x['ad_name'].lower() or not filter['f_ad_name']) and \
                (filter['f_ad_type'] == x['ad_type'].lower() or not filter['f_ad_type']) and \
                (filter['f_ad_status'] == x['status'].lower() or not filter['f_ad_status']):
                    p.add(x['ad_id'])

            new = [ad for ad in all_data if ad['ad_id'] in p]
            print(new)

        else:
            print(request.POST)
            response=requests.post(f"http://127.0.0.1:3000/status_deactive_to_active/{idd}",data = request.POST)
            print(response)
            return redirect(f"/ad_provider/ad_pro_list/{id}")
        
    context={
        'key':mydata,
        'current_path':request.get_full_path(),
        'all_data':new[::-1],
        'user_access':access,
        }
    return render(request,"ad_pro_list.html",context)

def ads_active(request,id):
    value = request.COOKIES.get('ad_provider')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/ad_provider/signin/")
    try:
        mydata = requests.get(f"http://127.0.0.1:3000/ad_pro_my_data/{id}").json()[0]
        idd = id
        access = ""
    except:  
        mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]
        access = mydata['access_Privileges']
        print(mydata['aid'])
        idd = mydata['aid']
    jsondec=json.decoder.JSONDecoder()
    new=[]
    a=[]
    all_data=requests.get("http://127.0.0.1:3000/all_pro_ads_data/").json()
    emra_data=requests.get(f"http://127.0.0.1:3000/superadmin/emra_coin/{idd}").json()
    for x in emra_data:
        emra_value=x.get('emra_coin_value')

    for i in all_data:
        uid=jsondec.decode(i.get("ad_pro"))
        id_value = uid['uid']
        if id_value == idd:
            new.append(i)
    
    for j in new:
        status=j.get("status")
        a.append(status)
       
    status_count=a.count("Active")
    
    #  Emera coin value 
    for item in new:
        if item['coin'] != None:
            item['amount'] = int(item['coin']) * int(emra_value)
        else:
            item['amount'] = 0

    

    if "detail" in request.POST:
        print(request.POST)
        global ads_id
        ads_id=request.POST['detail']
        print(ads_id)
        return redirect(f"/ad_provider/ad_pro_adDetails/{id}")
    elif "ad_id" in request.POST:
            print(request.POST)
            filter={
                'f_ad_id': request.POST['ad_id'].strip(),
                'f_ad_name': request.POST['ad_name'].strip().lower(),
                'f_ad_type': request.POST['ad_type'].strip().lower(),
                
    
            }
            
            p = set()

            for x in new:
                if (filter['f_ad_id'] == x['ad_id'] or not filter['f_ad_id']) and \
                (filter['f_ad_name'] == x['ad_name'].lower() or not filter['f_ad_name']) and \
                (filter['f_ad_type'] == x['ad_type'].lower() or not filter['f_ad_type']):
                    p.add(x['ad_id'])

            new = [ad for ad in all_data if ad['ad_id'] in p]
            print(new)

    else:
        print(" ")

    context={
        'key':mydata,
        'current_path':request.get_full_path(),
        'all_data':new[::-1],
        'user_access':access,
        'count':status_count }
    

    return render(request,"ad_pro_active.html",context)


def ads_pending(request,id):
    value = request.COOKIES.get('ad_provider')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/ad_provider/signin/")
    try:
        mydata = requests.get(f"http://127.0.0.1:3000/ad_pro_my_data/{id}").json()[0]
        idd = id
        access = ""
    except:  
        mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]
        access = mydata['access_Privileges']
        print(mydata['aid'])
        idd = mydata['aid']
    jsondec=json.decoder.JSONDecoder()
    new=[]
    a=[]
    all_data=requests.get("http://127.0.0.1:3000/all_pro_ads_data/").json()
    emra_data=requests.get(f"http://127.0.0.1:3000/superadmin/emra_coin/{idd}").json()
    for x in emra_data:
        emra_value=x.get('emra_coin_value')

    for i in all_data:
        uid=jsondec.decode(i.get("ad_pro"))
        id_value = uid['uid']
        if id_value == idd:
            new.append(i)

    for j in new:
        status=j.get("status")
        a.append(status)
       
    status_count=a.count("Pending")
    
    #  Emera coin value 
    for item in new:
        if item['coin'] != None:
            item['amount'] = int(item['coin']) * int(emra_value)
        else:
            item['amount'] = 0

    
    
    if "detail" in request.POST:
        print(request.POST)
        global ads_id
        ads_id=request.POST['detail']
        print(ads_id)
        return redirect(f"/ad_provider/ad_pro_adDetails/{id}")
    
    elif "ad_id" in request.POST:
            print(request.POST)
            filter={
                'f_ad_id': request.POST['ad_id'].strip(),
                'f_ad_name': request.POST['ad_name'].strip().lower(),
                'f_ad_type': request.POST['ad_type'].strip().lower(),
               
            }
            
            p = set()

            for x in new:
                if (filter['f_ad_id'] == x['ad_id'] or not filter['f_ad_id']) and \
                (filter['f_ad_name'] == x['ad_name'].lower() or not filter['f_ad_name']) and \
                (filter['f_ad_type'] == x['ad_type'].lower() or not filter['f_ad_type']):
                    p.add(x['ad_id'])

            new = [ad for ad in all_data if ad['ad_id'] in p]
            print(new)
    else:
        print(" ")

    context={
        'key':mydata,
        'current_path':request.get_full_path(),
        'all_data':new[::-1],
        'user_access':access,
        'count':status_count }
    return render(request,"ad_pro_pending.html",context)

def ads_deactive(request,id):
    value = request.COOKIES.get('ad_provider')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/ad_provider/signin/")
    try:
        mydata = requests.get(f"http://127.0.0.1:3000/ad_pro_my_data/{id}").json()[0]
        idd = id
        access = ""
    except:  
        mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]
        access = mydata['access_Privileges']
        print(mydata['aid'])
        idd = mydata['aid']
    jsondec=json.decoder.JSONDecoder()
    new=[]
    a=[]
    all_data=requests.get("http://127.0.0.1:3000/all_pro_ads_data/").json()
    emra_data=requests.get(f"http://127.0.0.1:3000/superadmin/emra_coin/{idd}").json()
    for x in emra_data:
        emra_value=x.get('emra_coin_value')

    for i in all_data:
        uid=jsondec.decode(i.get("ad_pro"))
        id_value = uid['uid']
        if id_value == idd:
            new.append(i)

    for j in new:
        status=j.get("status")
        a.append(status)
       
    status_count=a.count("Deactive")
    
    #  Emera coin value 
    for item in new:
        if item['coin'] != None:
            item['amount'] = int(item['coin']) * int(emra_value)
        else:
            item['amount'] = 0

   
    
    if "detail" in request.POST:
        print(request.POST)
        global ads_id
        ads_id=request.POST['detail']
        print(ads_id)
        return redirect(f"/ad_provider/ad_pro_adDetails/{id}") 
    elif "ad_id" in request.POST:
            print(request.POST)
            filter={
                'f_ad_id': request.POST['ad_id'].strip(),
                'f_ad_name': request.POST['ad_name'].strip().lower(),
                'f_ad_type': request.POST['ad_type'].strip().lower(),
                
    
            }
            
            p = set()

            for x in new:
                if (filter['f_ad_id'] == x['ad_id'] or not filter['f_ad_id']) and \
                (filter['f_ad_name'] == x['ad_name'].lower() or not filter['f_ad_name']) and \
                (filter['f_ad_type'] == x['ad_type'].lower() or not filter['f_ad_type']):
                    p.add(x['ad_id'])

            new = [ad for ad in all_data if ad['ad_id'] in p]
            print(new)
    
    else:
        print(" ")


    context={
        'key':mydata,
        'current_path':request.get_full_path(),
        'all_data':new[::-1],
        'user_access':access,
        'count':status_count }
    
    return render(request,"ad_pro_deactive.html",context)

def ads_closed(request,id):
    value = request.COOKIES.get('ad_provider')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/ad_provider/signin/")
    try:
        mydata = requests.get(f"http://127.0.0.1:3000/ad_pro_my_data/{id}").json()[0]
        idd = id
        access = ""
    except:  
        mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]
        access = mydata['access_Privileges']
        print(mydata['aid'])
        idd = mydata['aid']
    jsondec=json.decoder.JSONDecoder()
    new=[]
    a=[]
    all_data=requests.get("http://127.0.0.1:3000/all_pro_ads_data/").json()
    emra_data=requests.get(f"http://127.0.0.1:3000/superadmin/emra_coin/{idd}").json()
    for x in emra_data:
        emra_value=x.get('emra_coin_value')

    for i in all_data:
        uid=jsondec.decode(i.get("ad_pro"))
        id_value = uid['uid']
        if id_value == idd:
            new.append(i)
    print(new)

    for j in new:
        status=j.get("status")
        a.append(status)
       
    status_count=a.count("Closed")
    
    #  Emera coin value 
    for item in new:
        if item['coin'] != None:
            item['amount'] = int(item['coin']) * int(emra_value)
        else:
            item['amount'] = 0

    
    if "detail" in request.POST:
        print(request.POST)
        global ads_id
        ads_id=request.POST['detail']
        print(ads_id)
        return redirect(f"/ad_provider/ad_pro_adDetails/{id}")

    elif "ad_id" in request.POST:
            print(request.POST)
            filter={
                'f_ad_id': request.POST['ad_id'].strip(),
                'f_ad_name': request.POST['ad_name'].strip().lower(),
                'f_ad_type': request.POST['ad_type'].strip().lower(),
            }
            
            p = set()

            for x in new:
                if (filter['f_ad_id'] == x['ad_id'] or not filter['f_ad_id']) and \
                (filter['f_ad_name'] == x['ad_name'].lower() or not filter['f_ad_name']) and \
                (filter['f_ad_type'] == x['ad_type'].lower() or not filter['f_ad_type']):
                    p.add(x['ad_id'])

            new = [ad for ad in all_data if ad['ad_id'] in p]
            print(new)
            
    else:
        print("no data")

    context={
        'key':mydata,
        'current_path':request.get_full_path(),
        'all_data':new[::-1],
        'user_access':access,
        'count':status_count
          }
    return render(request,"ad_pro_closed.html",context)
    

# /// Ad_pro Ads Creation//////
def ad_pro_createAd(request,id):
    value = request.COOKIES.get('ad_provider')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/ad_provider/signin/")
    try:
        mydata = requests.get(f"http://127.0.0.1:3000/ad_pro_my_data/{id}").json()[0]
        idd = id
        access = ""
    except:  
        mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]
        access = mydata['access_Privileges']
        print(mydata['aid'])
        idd = mydata['aid']

    jsondec=json.decoder.JSONDecoder()
    # all_data=requests.get("http://127.0.0.1:3000/all_ads_data/").json()
    neww=[]
    new=[]
    response = requests.get('https://api.first.org/data/v1/countries').json()
    
    all = requests.get('https://countriesnow.space/api/v0.1/countries/states').json()

    # dist=requests.get('https://countriesnow.space/api/v0.1/countries/capital').json()
    # statess = requests.get('https://countriesnow.space/api/v0.1/countries/states').json()
    # for i in all_data:
    #     uid=jsondec.decode(i.get("ad_dis"))
    #     id_value = uid['uid']
    #     if id_value == uid:
    #         new.append(i)

    states = json.dumps(all["data"])
    
    al = (all["data"])
    for x in al:
        name = (x.get("name"))
        neww.append(name)
    countryname = json.dumps(neww)

    context = {'key':mydata,'current_path':request.get_full_path(),
                'response': response, 'region': response,'all':al,'user_access':access,
                'country': countryname,'states': states,   'all_data': new,
                'user_access':access}
    if "office_state" in request.POST:
        city = request.POST['office_state']
    else:
        city = "None"
    
    # if "no_views" in request.POST:    
    #     if int(request.POST['no_views']) >= 10 :
    #         views=int(request.POST['no_views']) / 10
    #         coin=math.ceil(views)
    #         commission=(coin* 10)//5
    #         print(commission)
    #     else:
    #         coin="0"
    #         commission="0"

    if request.method == "POST":
        print("Posted values",request.POST)
        dic_values=dict(request.POST)
        print(request.FILES)
        response = requests.post(f"http://127.0.0.1:3000/create_new_ads/{id}", data = dic_values,files=request.FILES)
        print(response)
        # print(response.status_code)
        # print(response.text)
        return redirect(f"/ad_provider/ad_pro_list/{id}")
    return render(request,"ad_pro_createAd.html",context)

def ad_pro_editAd(request,id):
    value = request.COOKIES.get('ad_provider')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/ad_provider/signin/")
    try:
        mydata = requests.get(f"http://127.0.0.1:3000/ad_pro_my_data/{id}").json()[0]
        idd = id
        access = ""
    except:  
        mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]
        access = mydata['access_Privileges']
        print(mydata['aid'])
        idd = mydata['aid']

    ads_list_all(request,id)
    # print(dis_id)
    ads_data=requests.get(f"http://127.0.0.1:3000/ad_pro_ad_details/{dis_id}").json()
    
    #Ads_list details
    languages_value=[]
    office_country_value=[]
    office_state_value=[]
    office_district_value=[]
    gender_value=[]
    age_range_value=[]
    age_to_value=[]
    languages = ads_data['languages'][1:-1].split(", ")
    office_country = ads_data['office_country'][1:-1].split(", ")
    office_state = ads_data['office_state'][1:-1].split(", ")
    office_district = ads_data['office_district'][1:-1].split(", ")
    gender = ads_data['gender'][1:-1].split(", ")
    age_range = ads_data['age_range'][1:-1].split(", ")
    age_to = ads_data['age_to'][1:-1].split(", ")
    for office_country_x in office_country:
        office_country_value.append(office_country_x[1:-1])
    for office_state_x in office_state:
        office_state_value.append(office_state_x[1:-1])
    for languages_x in languages:
        languages_value.append(languages_x[1:-1])
    for gender_x in gender:
        gender_value.append(gender_x[1:-1])
    for age_range_x in age_range:
        age_range_value.append(age_range_x[1:-1])
    for age_to_x in age_to:
        age_to_value.append(age_to_x[1:-1])
    for office_district_x in office_district:
        office_district_value.append(office_district_x[1:-1])
    ad_data1={}
    sib = [ad_data1]
    for i, office_country_data in enumerate(office_country_value):
        key = f'office_country_{i}'
        if key not in ad_data1:
            ad_data1[key] = office_country_data
    for i, languages_data in enumerate(languages_value):
        key = f'languages_{i}'
        if key not in ad_data1:
            ad_data1[key] = languages_data
    for i, office_district_data in enumerate(office_district_value):
            key = f'office_district_{i}'
            if key not in ad_data1:
                ad_data1[key] = office_district_data
    for i, office_state_data in enumerate(office_state_value):
            key = f'office_state_{i}'
            if key not in ad_data1:
                ad_data1[key] = office_state_data
    for i, gender_data in enumerate(gender_value):
            key=f'gender_{i}'
            if key not in ad_data1:
                ad_data1[key] = gender_data
    for i, age_range_data in enumerate(age_range_value):
            key=f'age_range_{i}'
            if key not in ad_data1:
                ad_data1[key] = age_range_data
    for i, age_to_data in enumerate(age_to_value):
            key=f'age_to_{i}' 
            if key not in ad_data1:
                ad_data1[key] = age_to_data        
    
    print(sib)
    context={
        'key':mydata,
        'current_path':request.get_full_path(),
        'ad_data':ads_data,
        'user_access':access,
        'ad_list_data':sib,
        }
    
    if request.method == "POST":
        dic_values=dict(request.POST)
        response = requests.post(f"http://127.0.0.1:3000/ad_pro_edit_ads/{dis_id}", data = dic_values,files=request.FILES)
        print(response)
        # print(response.status_code)
        # print(response.text)
        return redirect(f"/ad_provider/ad_pro_list/{id}")
    return render(request,"ad_pro_editad.html",context)

# //// Ad_pro Single Ads Details/////
def ad_pro_adDetails(request,id):
    value = request.COOKIES.get('ad_provider')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/ad_provider/signin/")
    try:
        mydata = requests.get(f"http://127.0.0.1:3000/ad_pro_my_data/{id}").json()[0]
        idd = id
        access = ""
    except:  
        mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]
        access = mydata['access_Privileges']
        print(mydata['aid'])
        idd = mydata['aid']  
    ads_list_all(request,id)
    print(ads_id)
    ads_data=requests.get(f"http://127.0.0.1:3000/ad_pro_ad_details/{ads_id}").json()
    emra_data=requests.get(f"http://127.0.0.1:3000/superadmin/emra_coin/{idd}").json()
    for x in emra_data:
        emra_value=x.get('emra_coin_value')
    if ads_data.get('coin')!=None:
        amount=int(ads_data.get('coin'))* int(emra_value)
    else:
        amount=0
    context={
        'key':mydata,
        'current_path':request.get_full_path(),
        'ad_data':ads_data,
        'user_access' : access,
        'amount':amount,
        }

    if request.method == "POST":
        print(request.POST)

        if "submit" in request.POST:
            response = requests.post(f"http://127.0.0.1:3000/ad_status_close/{ads_id}", data = request.POST)
            print(response)
            return redirect(f"/ad_provider/ad_pro_closed/{id}")

        elif "reset" in request.POST:
            print("reset")
            return redirect(f"/ad_provider/ad_pro_adDetails/{id}")
        
        else:
            print("---")
    return render(request,"ad_pro_adDetails.html",context)

# //// Ad_pro Payments////
def ad_pro_payment(request,id):
    value = request.COOKIES.get('ad_provider')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/ad_provider/signin/")
    try:
        mydata = requests.get(f"http://127.0.0.1:3000/ad_pro_my_data/{id}").json()[0]
        idd = id
        access = ""
    except:  
        mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]
        access = mydata['access_Privileges']
        print(mydata['aid'])
        idd = mydata['aid']
    context={
        'key':mydata,
        'current_path':request.get_full_path(),
        'user_access' : access

    }

    return render(request,"ad_pro_payment.html",context)

# //// Ad_providers Users////
def ad_pro_users(request,id):
    value = request.COOKIES.get('ad_provider')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/ad_provider/signin/")
    try:
        mydata = requests.get(f"http://127.0.0.1:3000/ad_pro_my_data/{id}").json()[0]
        idd = id
        access = ""
    except:  
        mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]
        access = mydata['access_Privileges']
        print(mydata['aid'])
        idd = mydata['aid']
    error = ""
    my_user = requests.get(f"http://127.0.0.1:3000/ad_pro_my_users_data/{idd}").json()
    new=[]
    for x in my_user:
        new.append(x)
    print(my_user)
    if request.method== "POST":
        print(request.POST)

        if "delete" in request.POST:
            response = requests.post(f"http://127.0.0.1:3000/ad_pro_add_user/{idd}",data=request.POST)
            print(response.text)
            print(response.status_code)

        elif "edit" in request.POST:
            global user_uid
            user_uid = request.POST['edit']
            return redirect(f"/ad_provider/ad_pro_user_edit/{id}")
        
        elif "edit_user" in request.POST:
            print(request.POST)
            if request.POST['password'] == request.POST['confirm_password']:
                data={
                    'first_name': request.POST['first_name'],
                    'last_name':request.POST['last_name'],
                        'email': request.POST['email'],
                        'mobile':request.POST['mobile'],
                            'password': request.POST['password'],
                                'access_Privileges':  request.POST.getlist('access_Privileges'),
                                'edit':request.POST['edit_user'],
                }
            print(data)
            response = requests.post(f"http://127.0.0.1:3000/ad_pro_add_user/{idd}",data=data)
            # print(response.text)
            # print(response.status_code)
            if response.status_code == 200:
                return redirect(f"http://51.20.61.70:8001/ad_provider/ad_pro_users/{id}")
            elif response.status_code == 203:
                print("user already exist")
                error = "User Already Exixts"

        elif "user_id" in request.POST:

            filter = {
            'f_u_id': request.POST['user_id'],
            'f_u_name': request.POST['user_name'].lower(),
            'f_u_email': request.POST['user_email'].lower(),
            'f_u_phone': request.POST['user_phone'],
            }

            p = set()

            for x in new:
                if (filter['f_u_id'] == x['uid'] or not filter['f_u_id']) and \
                (filter['f_u_name'] == x['first_name'].lower() or not filter['f_u_name']) and \
                (filter['f_u_email'] == x['email'].lower() or not filter['f_u_email']) and \
                (filter['f_u_phone'] == x['mobile'] or not filter['f_u_phone']):
                    p.add(x['uid'])

            new = [ad for ad in my_user if ad['uid'] in p]
            print(new)

        else:
            print("no data")

    context={
        'key':mydata,
        'current_path':request.get_full_path(),
        'my_user':new,
        'error':error,
        'user_access' : access,
    
    }
    return render(request,"ad_pro_users.html",context)


def ad_pro_addusers(request,id):
    value = request.COOKIES.get('ad_provider')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/ad_provider/signin/")
    try:
        mydata = requests.get(f"http://127.0.0.1:3000/ad_pro_my_data/{id}").json()[0]
        idd = id
        access = ""
    except:  
        mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]
        access = mydata['access_Privileges']
        print(mydata['aid'])
        idd = mydata['aid']
    error=""
    mydata = requests.get(f"http://127.0.0.1:3000/ad_pro_my_data/{id}").json()[0]  
    if request.method=="POST":
        print(request.POST)
        if request.POST['password'] == request.POST['confirm_password']:
            data={
                'first_name': request.POST['first_name'],
                'last_name':request.POST['last_name'],
                    'email': request.POST['email'],
                    'mobile':request.POST['mobile'],
                        'password': request.POST['password'],
                            'access_Privileges':  request.POST.getlist('access_Privileges'),
                            'work':"ad_provider",
                            'creator':id
            }
        print(data)
        response = requests.post(f"http://127.0.0.1:3000/ad_pro_add_user/{id}",data=data)
        print(response.text)
        print(response.status_code)
        if response.status_code == 200:
            return redirect(f"http://127.0.0.1:3000/ad_provider/ad_pro_users/{id}")
        elif response.status_code == 203:
            print("user already exist")
            error = "User Already Exixts"
    context={
        'key':mydata,
        'current_path':request.get_full_path(),
        'error':error,
        'user_access':""
    }
    return render(request,"ad_pro_addusers.html",context)

def ad_pro_user_edit(request,id):
    value = request.COOKIES.get('ad_provider')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/ad_provider/signin/")
    try:
        mydata = requests.get(f"http://127.0.0.1:3000/ad_pro_my_data/{id}").json()[0]
        idd = id
        access = ""
    except:  
        mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]
        access = mydata['access_Privileges']
        print(mydata['aid'])
        idd = mydata['aid']
    ad_pro_users(request,id)
    print(user_uid)
    error=""
    
    users_data   = requests.get(f"http://127.0.0.1:3000/ad_pro_single_users_data/{user_uid}").json()[0]
    print(users_data)
    if request.method=="POST":
        print(request.POST)
        if request.POST['password'] == request.POST['confirm_password']:
            data={
                'first_name': request.POST['first_name'],
                'last_name':request.POST['last_name'],
                    'email': request.POST['email'],
                    'mobile':request.POST['mobile'],
                        'password': request.POST['password'],
                            'access_Privileges':  request.POST.getlist('access_Privileges'),
                            'edit':request.POST['edit_user'],
            }
        print(data)
        response = requests.post(f"http://127.0.0.1:3000/ad_pro_add_user/{idd}",data=data)
        print(response.text)
        print(response.status_code)
        if response.status_code == 200:
            return redirect(f"http://127.0.0.1:3000/ad_provider/ad_pro_users/{id}")
        elif response.status_code == 203:
            print("user already exist")
            error = "User Already Exixts"
    context={
        'key':mydata,
        'current_path':request.get_full_path(),
        'error':error,
        'users_data':users_data,
        'user_access':access
    }

    return render(request,"ad_pro_user_edit.html",context)

# /// Ad_pr Account Settings/////
def ad_pro_settings(request,id):
    value = request.COOKIES.get('ad_provider')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/ad_provider/signin/")
    try:
        mydata = requests.get(f"http://127.0.0.1:3000/ad_pro_my_data/{id}").json()[0]
        idd = id
        access = ""
    except:  
        mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]
        access = mydata['access_Privileges']
        print(mydata['aid'])
        idd = mydata['aid']
    mydata = requests.get(f"http://127.0.0.1:3000/ad_pro_my_data/{id}").json()[0] 
    
    if request.method=="POST":
        print(request.POST)
        if 'pass_reset' in request.POST:
            a=request.POST["pass_reset"]
            print(a)
            response = requests.post(f"http://127.0.0.1:3000/ad_pro_password_reset/{id}",data=request.POST )
        else:
            print(request.POST)
            response = requests.post(f"http://127.0.0.1:3000/ad_pro_email_update/{id}", data = request.POST)
            print(response)
            print(response.status_code)
            print(response.text)
            return render(request,"ad_pro_settings.html",context)
        
    context={
        'key':mydata,
        'current_path':request.get_full_path(),
        'user_access' : access
    }
    return render(request,"ad_pro_settings.html",context)

# //// Password Reset////
def ad_pro_password_reset(request,id):
#    value = request.COOKIES.get('ad_provider')
 #   if value != None:
  #      print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
   # else:
    #    return redirect("/ad_provider/signin/")
    print(id)
    if request.method=="POST":
        print(request.POST)
        if 'pass_reset' in request.POST:
            a=request.POST["pass_reset"]
            print(a)

        if request.POST['password'] == request.POST['confirm_password']:
            response = requests.post(f"http://127.0.0.1:3000/ad_pro_password_update/{id}",data=request.POST )
            messages.info(request,"Password Successfully Updated")
        else:
            messages.info(request,"Password Incorrect")
    return render(request,"ad_pro_password_rest.html")

# /// Forget password////
def ad_pro_forget_password(request):
  #  value = request.COOKIES.get('ad_provider')
   # if value != None:
    #    print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
   # else:
    #    return redirect("/ad_provider/signin/")
    error=""
    if request.method == "POST":
        
        print(request.POST)
        response = requests.post("http://127.0.0.1:3000/ad_pro_forget_password/",data=request.POST)
        print(response)
        print(response.status_code)
        print(type(jsondec.decode(response.text)))
        print(jsondec.decode(response.text))
        uidd = jsondec.decode(response.text)
        
        if response.status_code == 200:
            return redirect(f"/ad_pro_forgetpassword_otpp/{uidd}")
        elif response.status_code == 403:
            error = "User Doesn't Exist"

    context = {'error':error}
    return render(request,"ad_pro_email.html",context)
    

def ad_pro_forgetpassword_otp(request,id):
 #   value = request.COOKIES.get('ad_provider')
  #  if value != None:
   #     print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
   # else:
    #    return redirect("/ad_provider/signin/")
    mydata = requests.get(f"http://127.0.0.1:3000/ad_pro_my_data/{id}").json()[0]
    context = {'invalid':"invalid",
                'key':mydata}
    new=[]
    if request.method == "POST":
        new.append(request.POST["otp1"]) 
        new.append(request.POST["otp2"])
        new.append(request.POST["otp3"])
        new.append(request.POST["otp4"])
        data = {
            'user_otp1':int(''.join(new).strip())
           
        }
        print(data)
        response = requests.post(f"http://127.0.0.1:3000/ad_pro_forget_password_otp/{id}", data=data)
       
        print(response)
        print(response.status_code)
        print(data['user_otp1'])
        print(response.text)
        uidd = (response.text[1:-1])
        
        if response.status_code == 200:
            return redirect(f"/ad_pro_forgetpassword_resett/{uidd}")
        else:
            invalid = "Invalid OTP"
            context = {'invalid':invalid}
    return render(request,"ad_provider_otpcheck.html",context)


def ad_pro_forgetpassword_reset(request,id):
 #   value = request.COOKIES.get('ad_provider')
  #  if value != None:
   #     print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
   # else:
    #    return redirect("/ad_provider/signin/")
    error=""
    mydata = requests.get(f"http://127.0.0.1:3000/ad_pro_my_data/{id}").json()[0]
    print(id)
    if request.method=="POST":
        print(request.POST)
        if request.POST['password'] == request.POST['confirm_password']:
            response = requests.post(f"http://127.0.0.1:3000/ad_pro_password_update/{id}",data=request.POST )
            print(response)
            return redirect(f"/ad_provider/signin/")

        else:
            print(response)
            error="password mismatch"
    context = {'invalid':"invalid",
                'key':mydata,
                'error':error}
    return render(request,"ad_pro_forgetpassword.html",context)


