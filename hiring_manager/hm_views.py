from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
import requests
import json
from django.contrib import messages
from collections import Counter
from django.contrib.auth import logout,authenticate
from hiring_manager.process_to_pdf import html_to_pdf 
# Create your views here.
jsondec = json.decoder.JSONDecoder()
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

    return render(request,"createaccount.html",context)

def signup(request):
    error = ""
    if request.method == "POST":
        if request.POST['password'] == request.POST['confirm_password']:
                # response = requests.post('http://54.159.186.219:8000/signup/',data=request.POST)
                response = requests.post("http://127.0.0.1:3000/hm_signup/",data=request.POST)
                print(response.status_code)
                print(response.text)
                uidd = (response.text[1:-1])
                print(uidd)
                if response.status_code == 200:
                   return redirect(f"/hiring_manager/otp/{uidd}")
                elif response.status_code == 302:
                    error = "User Already Exist" 
                    return redirect("/hiring_manager/signin/")
                       
                else:
                    pass

        else:
            print("password doesn't match")
    context = {'error':error}
    return render(request,"hm_signup.html",context)

def signin(request):
    jsondec = json.decoder.JSONDecoder()
    value = request.COOKIES.get('hiringmanager')
    print(value)
    error = ""
    context = {'error':error}
    if request.method == "POST":
        print(request.POST)
        # response = requests.post("http://54.159.186.219:8000/signin/",data=request.POST)
        response = requests.post("http://127.0.0.1:3000/hm_signin/",data=request.POST)
        print(response.status_code)
        #print(type(jsondec.decode(response.text)))
        #print(jsondec.decode(response.text))
        uidd = jsondec.decode(response.text)
        global access_Privileges
        try:
            access_Privileges = uidd['access_Privileges']
            uid = uidd['uid']
            
        except:
            access_Privileges = ""
            uid = uidd
        # print(uid)
        if response.status_code == 200:
            mydata = requests.get(f"http://127.0.0.1:3000/hm_my_data/{uid}").json()[0]
            print(mydata.get('my_hiring_manager'))
            print("hiring manager :",mydata)

            user_otp = mydata.get('user_otp')
            if user_otp is not None:
                print("otp")
                id_card_data = mydata.get('id_card')
                hm=mydata.get('my_hiring_manager')
                if id_card_data is None:
                    print("idcard")
                    if hm is not None:
                        print("hm")
                        alert_message="You are under Verification Process...."
                        context['alert_message'] = alert_message
                        return render(request,"hm_signin.html",context)
                    
                    elif hm is None:
                        print("no hm")
                        return redirect(f"/hiring_manager/hm_upload_acc/{uid}")
                    
                    else:
                        return redirect(f"/hiring_manager/profile_picture/{uid}")
                
                elif id_card_data is not None:
                    print("no idcard")
                    res = redirect(f"/hiring_manager/hm_admin_dashboard/{uid}")
                    res.set_cookie("hiringmanager",uid)
                    return res
                    
                
            elif user_otp is None:
                delete_hm = requests.delete("http://127.0.0.1:3000/hm_delete_data/",data=request.POST)
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
            delete_hm = requests.delete("http://127.0.0.1:3000/hm_delete_data/",data=request.POST)
            if delete_hm.status_code == 204:
                print("Data deleted successfully")
                error="Not Registered...Please click Create an Account"
            elif delete_hm.status_code == 404:
                print("Data not found")
            else:
                print("Error occurred:", delete_hm.status_code)
        elif response.status_code == 404:
            error="User Doesn't Exists"
        else:
          error = "YOUR EMAIL-ID OR PASSWORD IS INCORRECT"
    context = {'error':error}
    return render(request,"hm_signin.html",context)

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
        response = requests.post(f"http://127.0.0.1:3000/hm_otp/{id}", data=data)

       
        print(response)
        print(response.status_code)
        print(data['user_otp'])
        print(response.text)
        uidd = (response.text[1:-1])
        
        if response.status_code == 200:
        # if get["otp"] == data['user_otp']:
            # return redirect(f"/profileidcard/{uidd}")
            return redirect(f"/hiring_manager/profile_picture/{uidd}")
        else:
            invalid = "Invalid OTP"
            context = {'invalid':invalid}
    return render(request,"hm_otpcheck.html",context)

def profile_picture(request,id):
    if request.method == "POST":
        print(request.FILES)
        # response = requests.post(f"http://54.159.186.219:8000/profileidcard/{id}",   files=request.FILES)
        response = requests.post(f"http://127.0.0.1:3000/hm_profile_picture/{id}",   files=request.FILES)
        print(response)
        print(response.status_code)
        print(response.text)
        uidd = (response.text[1:-1])
        if response.status_code == 200:
        # if get["otp"] == data['user_otp']:
            return redirect(f"/hiring_manager/hm_upload_acc/{uidd}")
        else:
            return HttpResponse("INVALId")
    return render(request,"hm_profilepicture.html")

def upload_acc(request,id):
    try:
        #hiring manager list
        hiring_manager = requests.get("http://127.0.0.1:3000/all_hm_data/").json()
        mydata = requests.get(f"http://127.0.0.1:3000/hm_my_data/{id}").json()[0]
        neww=[]
        response = requests.get('https://api.first.org/data/v1/countries').json()
        all = requests.get('https://countriesnow.space/api/v0.1/countries/states').json()
        states = json.dumps(all["data"])
        al = (all["data"])
        for x in al:
           name = (x.get("name"))
           neww.append(name)
        countryname = json.dumps(neww)
        # alert_message="Please Fill Your Basic Informations"
        context = {'response': response, 'region': response,'all':al,'key':mydata,
                    'country': countryname,'states': states,'hiring_manager':hiring_manager}
        if request.method == "POST":
            # print("hai")
            major = request.POST.get('old_yn', '')
            previous = request.POST.get('applied_yn', '')
            court = request.POST.get('judgment_yn', '')
            govt = request.POST.get('govt_yn', '')
            nota = request.POST.get('notary_yn', '')
            english = request.POST.get('english_yn', '')

            # Converting Yes/No values to boolean
            major_bool = major.lower() == 'yes'
            previous_bool = previous.lower() == 'yes'
            court_bool = court.lower() == 'yes'
            govt_bool = govt.lower() == 'yes'
            nota_bool = nota.lower() == 'yes'
            english_bool = english.lower() == 'yes'
            
            if major_bool and not previous_bool and not court_bool and not govt_bool and nota_bool and english_bool:
                
                print(dict(request.POST))
                # print(request.FILES)
                dictio = dict(request.POST)
                # dictio['level_education'] = request.POST.getlist('level_education')
                print("front data",dictio)
                # response = requests.post(f"http://54.159.186.219:8000/profileidcard/{id}",   files=request.FILES)
                response = requests.post(f"http://127.0.0.1:3000/hm_upload_account/{id}",   data = dictio,files=request.FILES)
                # print(response)
                # print(response.status_code)
                # print(response.text)
                # uidd = (response.text[1:-1])
                uid=request.POST['my_hiring_manager']
                if response.status_code == 200:
                    alert_message = 'Congratulations! You are eligible to meet the hiring criteria. Application submitted successfully.'
                    data={
                        'noter_id':id,
                        'not_message':"{id} selected you as his/her Hiring Manager",
                        'notify_id': uid,
                    }
                    notify=requests.post("http://127.0.0.1:3000/notification_update/",data=data)
                    if notify.status_code == 200:
                        status_up=requests.post(f"http://127.0.0.1:3000/hm_notify_status_true/{uid}")
                        print(status_up.status_code)
                    return redirect(f"/hiring_manager/signin/")
                else:
                    alert_message = 'Sorry! Server Issue, Cannot Update Your Data'
                    print(alert_message)

            else:
              
                print(dict(request.POST))
                alert_message = 'Sorry, you are not eligible to meet the hiring criteria. Application cannot be submitted.'
                print(alert_message)
                # print(request.FILES)
                # dictio = dict(request.POST)
                # # dictio['level_education'] = request.POST.getlist('level_education')
                # # print(dictio)
                # # response = requests.post(f"http://54.159.186.219:8000/profileidcard/{id}",   files=request.FILES)
                # response = requests.post(f"http://127.0.0.1:3000/hm_upload_account/{id}",   data = dictio,files=request.FILES)
                # # print(response)
                # # print(response.status_code)
                # # print(response.text)
                # uidd = (response.text[1:-1])
                # if response.status_code != 200:
                #     alert_message = 'Sorry, you are not eligible to meet the hiring criteria. Application cannot be submitted.'

                # # if get["otp"] == data['user_otp']:
                context['alert_message'] = alert_message
                return render(request,"hm_upload_acc.html",context)
                
        else:
            pass
            
        # context = {'response': response, 'region': response,'all':al,'key':mydata,
        #             'country': countryname,'states': states,'hiring_manager':hiring_manager,
        #             'alert_message': alert_message}
        return render(request,"hm_upload_acc.html",context)
    except:
        return render(request,"hm_upload_acc.html")

def logout_view(request):
    print("logout")
    value = request.COOKIES.get('hiringmanager')
    print(value)
    response = redirect("/hiring_manager/signin/")
    # response = HttpResponse("delete cookie")
    response.delete_cookie("hiringmanager")
    return response

def admin_dashboard(request,id):
    value = request.COOKIES.get('hiringmanager')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/hiring_manager/signin")
    try:
        mydata = requests.get(f"http://127.0.0.1:3000/hm_my_data/{id}").json()[0] 
        access = "" 
        idd = id
    except:
        mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]
        access = mydata['access_Privileges']  
        idd = mydata['aid']

    #Notification
    if requests.get(f"http://127.0.0.1:3000/notification_data/{idd}") == None:
        notification=""
        
    else:
        notification = requests.get(f"http://127.0.0.1:3000/notification_data/{idd}")
        notification_data = json.loads(notification.text)
        

    #hiring manager
    if requests.get(f"http://127.0.0.1:3000/hm_my_data/{idd}").json()[0]['hiring_manager'] == None:
        hm_data =""
    else:
        hm_data = jsondec.decode(requests.get(f"http://127.0.0.1:3000/hm_my_data/{idd}").json()[0]['hiring_manager'])    

    #profile manager
    if requests.get(f"http://127.0.0.1:3000/hm_my_data/{idd}").json()[0]['my_profile_manager'] == None:
        pm_data =""
    else:
        pm_data = jsondec.decode(requests.get(f"http://127.0.0.1:3000/hm_my_data/{idd}").json()[0]['my_profile_manager'])    

    #ad provider
    if requests.get(f"http://127.0.0.1:3000/hm_my_data/{idd}").json()[0]['ad_provider'] == None:
        ad_pro_data =""
    else:
        ad_pro_data = jsondec.decode(requests.get(f"http://127.0.0.1:3000/hm_my_data/{idd}").json()[0]['ad_provider']) 

    #ad distributor
    if requests.get(f"http://127.0.0.1:3000/hm_my_data/{idd}").json()[0]['ad_distributor'] == None:
        ad_dis_data =""
    else:
        ad_dis_data = jsondec.decode(requests.get(f"http://127.0.0.1:3000/hm_my_data/{idd}").json()[0]['ad_distributor']) 


    #sales
    if requests.get(f"http://127.0.0.1:3000/hm_my_data/{idd}").json()[0]['sales_manager'] == None:
        sales_data =""
    else:
        sales_data = jsondec.decode(requests.get(f"http://127.0.0.1:3000/hm_my_data/{idd}").json()[0]['sales_manager'])

    # affiliate_marketing
    if requests.get(f"http://127.0.0.1:3000/hm_my_data/{idd}").json()[0]['affiliate_marketing'] == None:
        aff_data =""
    else:
        aff_data = jsondec.decode(requests.get(f"http://127.0.0.1:3000/hm_my_data/{idd}").json()[0]['affiliate_marketing'])
    

    context={
        'key':mydata,
        'current_path':request.get_full_path(),
        'hm_data':hm_data,
        'pm_data':pm_data,
        'ad_pro_data':ad_pro_data,
        'ad_dis_data':ad_dis_data,
        'sales_data':sales_data,
        'aff_data':aff_data,
        'access':access,
        'notification' : notification_data,
    }
    return render(request,"hm_admin_dashboard.html",context)


def profile(request,id):
    value = request.COOKIES.get('hiringmanager')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/hiring_manager/signin")
    try:
        mydata = requests.get(f"http://127.0.0.1:3000/hm_my_data/{id}").json()[0] 
        my_user = requests.get(f"http://127.0.0.1:3000/hm_my_users_data/{id}").json()
        access = "" 
        idd = id
        education  = jsondec.decode(mydata['level_education'])
        study = jsondec.decode(mydata['field_study'])
    except:
        mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]
        access = mydata['access_Privileges']  
        print(access)
        idd = mydata['aid']

    context={
        'key':mydata,
        'education':education,
        'study':study,
        'current_path':request.get_full_path(),
        'access':access,
        
    }
   
    return render(request,"hm_profile.html",context)

def edit_acc(request,id):
    value = request.COOKIES.get('hiringmanager')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/hiring_manager/signin")
    mydata = requests.get(f"http://127.0.0.1:3000/hm_my_data/{id}").json()[0]
    try:
       neww=[]
       response = requests.get('https://api.first.org/data/v1/countries').json()
       all = requests.get('https://countriesnow.space/api/v0.1/countries/states').json()
       states = json.dumps(all["data"])
       al = (all["data"])
       for x in al:
          name = (x.get("name"))
          neww.append(name)
       countryname = json.dumps(neww)
   
       context={
           'key':mydata,
           'current_path':request.get_full_path(),
           'response': response, 
           'region': response,'all':al,
           'country': countryname,'states': states
       }
       if request.method == "POST":
           print(request.POST)
           response = requests.post(f"http://127.0.0.1:3000/hm_edit_account/{id}",data=request.POST,files = request.FILES)
           print(response)
           print(response.status_code)
           print(response.text)
       return render(request,"hm_edit_acc.html",context)
    except:
        context={
           'key':mydata,
           'current_path':request.get_full_path(),
       }
        return render(request,"hm_edit_acc.html",context)


def local_admin(request,id):
    value = request.COOKIES.get('hiringmanager')
    new=[]
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/hiring_manager/signin")
    try:
        mydata = requests.get(f"http://127.0.0.1:3000/hm_my_data/{id}").json()[0] 
        my_user = requests.get(f"http://127.0.0.1:3000/hm_my_users_data/{id}").json()
        access = "" 
        idd = id
    except:
        mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]
        access = mydata['access_Privileges']  
        print(access)
        idd = mydata['aid']
    if requests.get(f"http://127.0.0.1:3000/hm_my_data/{idd}").json()[0]['my_profile_manager'] == None:
        pm_data =""
    else:
        pm_data = jsondec.decode(requests.get(f"http://127.0.0.1:3000/hm_my_data/{idd}").json()[0]['my_profile_manager'])
        for i in pm_data:
            id_value=i['id_card']
            if id_value == None:
                i['status']="pending"
                new.append(i)
            else:
                i['status']="verified"
                new.append(i)    
    if request.method=="POST":
        print("hello")
        if 'uid' in request.POST:
            print(request.POST)
            global uid 
            uid = request.POST['uid']
            return redirect(f"/hiring_manager/hm_local_admin_upload/{idd}")
        elif "user_id" in request.POST:
            print("filter")
            filter = {
            'f_u_id': request.POST['user_id'].strip(),
            'f_u_name': request.POST['name'].strip().lower(),
            'f_u_email': request.POST['email'].strip(),
            'f_u_phone': request.POST['mobile'].strip(),
            'f_u_status' : request.POST['status'].strip(),
            'f_location' : request.POST['location'].strip(),
            
            }

            p = set()

            for x in new:
                if (filter['f_u_id'] == x['uid'] or not filter['f_u_id']) and \
                (filter['f_u_name'] == x['first_name'].lower() or not filter['f_u_name']) and \
                (filter['f_u_email'] == x['email'] or not filter['f_u_email']) and \
                (filter['f_u_phone'] == x['mobile'] or not filter['f_u_phone']) and \
                (filter['f_u_status'] == x['status'] or not filter['f_u_status']) and \
                (filter['f_location'] == x['personal_country'] or not filter['f_location']):
                    p.add(x['uid'])

            new = [ad for ad in pm_data if ad['uid'] in p]
            print(new)
        else:
            print(request.POST)
            print(request.FILES)

    context={
        'key':mydata,
        'current_path':request.get_full_path(),
        'pm_data':new,
        'access':access,
    }
    return render(request,"hm_localadmin.html",context)

def local_admin_upload(request,id,uid):
    value = request.COOKIES.get('hiringmanager')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/hiring_manager/signin")
    try:
        mydata = requests.get(f"http://127.0.0.1:3000/hm_my_data/{id}").json()[0] 
        my_user = requests.get(f"http://127.0.0.1:3000/hm_my_users_data/{id}").json()
        access = "" 
        idd = id
    except:
        mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]
        access = mydata['access_Privileges']  
        print(access)
        idd = mydata['aid']
    # mydata = requests.get(f"http://127.0.0.1:3000/hm_my_data/{id}").json()[0]  
    # local_admin(request,id)
    pm_data = requests.get(f"http://127.0.0.1:3000/pm_myid/{uid}").json()[0] 
   
    education  = jsondec.decode(pm_data['level_education'])
   
    study = jsondec.decode(pm_data['field_study']) 
    #country api 
    neww=[]
    response = requests.get('https://api.first.org/data/v1/countries').json()
    all = requests.get('https://countriesnow.space/api/v0.1/countries/states').json()
    states = json.dumps(all["data"])
    al = (all["data"])
    for x in al:
       name = (x.get("name"))
       neww.append(name)
    countryname = json.dumps(neww)

    context={
        'key':mydata,
        'current_path':request.get_full_path(),
        'pm_data':pm_data,
        'education':education,
        'study':study,
        'response': response,
        'region': response,
        'all':al,
        'access':access,
        'country': countryname,'states': states
    }

    if request.method == "POST":
        response = requests.post(f"http://127.0.0.1:3000/profile_manager_upload_account/{request.POST['uid']}",data=request.POST,files = request.FILES)
        print(response.status_code)
        if response.status_code == 200:
            data={
                'noter_id':id,
                'not_message':"Hiring Manager Verified Your Account",
                'notify_id': uid,
            }
            notify=requests.post("http://127.0.0.1:3000/notification_update/",data=data)
            if notify.status_code == 200:
                status_up=requests.post(f"http://127.0.0.1:3000/pm_notify_status_true/{uid}")
                print(status_up.status_code)

            return redirect(f"/hiring_manager/hm_local_admin/{id}")
        else:
            pass
    return render(request,"hm_LocaladminDoc.html",context)

def ad_provider(request,id):
    value = request.COOKIES.get('hiringmanager')
    new=[]
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/hiring_manager/signin")
    try:
        mydata = requests.get(f"http://127.0.0.1:3000/hm_my_data/{id}").json()[0] 
        my_user = requests.get(f"http://127.0.0.1:3000/hm_my_users_data/{id}").json()
        access = "" 
        idd = id
    except:
        mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]
        access = mydata['access_Privileges']  
        print(access)
        idd = mydata['aid']
    #ad provider
    if requests.get(f"http://127.0.0.1:3000/hm_my_data/{idd}").json()[0]['ad_provider'] == None:
        ad_pro_data =""
    else:
        ad_pro_data = jsondec.decode(requests.get(f"http://127.0.0.1:3000/hm_my_data/{idd}").json() [0]['ad_provider']) 
        for i in ad_pro_data:
            id_value=i['id_card']
            if id_value == None:
                i['status']="pending"
                new.append(i)
            else:
                i['status']="verified"
                new.append(i)
    if request.method=="POST":
        if 'uid' in request.POST:
            print(request.POST)
            global uid 
            uid = request.POST['uid']
            return redirect(f"/hiring_manager/hm_adprovider_upload/{idd}")
        elif "user_id" in request.POST:
            print("filter")
            filter = {
            'f_u_id': request.POST['user_id'].strip(),
            'f_u_name': request.POST['pro_name'].strip().lower(),
            'f_u_email': request.POST['email'].strip(),
            'f_u_phone': request.POST['mobile'].strip(),
            'f_u_status': request.POST['status'].strip(),
            'f_location' : request.POST['location'].strip()

            }

            p = set()

            for x in new:
                if (filter['f_u_id'] == x['uid'] or not filter['f_u_id']) and \
                (filter['f_u_name'] == x['first_name'].lower or not filter['f_u_name']) and \
                (filter['f_u_email'] == x['email'] or not filter['f_u_email']) and \
                (filter['f_u_phone'] == x['mobile'] or not filter['f_u_phone']) and \
                (filter['f_u_status'] == x['status'] or not filter['f_u_status']) and \
                (filter['f_location'] == x['personal_country'] or not filter['f_location']):
                    p.add(x['uid'])

            new = [ad for ad in ad_pro_data if ad['uid'] in p]
            print(new)
        else:
            print(request.POST)
            print(request.FILES)
        
    context={
        'key':mydata,
        'current_path':request.get_full_path(),
        'ad_pro_data':new,
        "access":access,
    }
    return render(request,"hm_ad_provider.html",context)

def ad_provider_doc(request,id):
    value = request.COOKIES.get('hiringmanager')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/hiring_manager/signin")
    mydata = requests.get(f"http://127.0.0.1:3000/hm_my_data/{id}").json()[0]  
   
    ad_provider(request,id)
    print(uid)
    ad_pro_my_data = requests.get(f"http://127.0.0.1:3000/ad_pro_my_data/{uid}").json()[0] 
    education  = jsondec.decode(ad_pro_my_data['level_education'])
    study = jsondec.decode(ad_pro_my_data['field_study']) 
    #country api
    neww=[]
    response = requests.get('https://api.first.org/data/v1/countries').json()
    all = requests.get('https://countriesnow.space/api/v0.1/countries/states').json()
    states = json.dumps(all["data"])
    al = (all["data"])
    for x in al:
       name = (x.get("name"))
       neww.append(name)
    countryname = json.dumps(neww)
   
  
    context={
        'key':mydata,
        'education':education,
        'study':study,
        'current_path':request.get_full_path(),
        'ad_pro_my_data':ad_pro_my_data,
        'response': response,
        'region': response,
        'all':al,
        'country': countryname,'states': states,
       
    }
    
    if request.method == "POST":
        if "get_document" in request.POST:
             # getting the template
            pdf = html_to_pdf('pdf.html',context_dict={'ad_pro_my_data':ad_pro_my_data})
            
            # rendering the template
            return HttpResponse(pdf, content_type='application/pdf')
        else:
            response = requests.post(f"http://127.0.0.1:3000/ad_provider_upload_account/{request.POST['uid']}",data=request.POST,files = request.FILES)
            print(response.status_code)
            if response.status_code == 200:
                data={
                'noter_id':id,
                'not_message':"Hiring Manager Verified Your Account",
                'notify_id': uid,
                }
                notify=requests.post("http://127.0.0.1:3000/notification_update/",data=data)
                if notify.status_code == 200:
                    status_up=requests.post(f"http://127.0.0.1:3000/ad_pro_notify_status_true/{uid}")
                    print(status_up.status_code)
                    return redirect(f"/hiring_manager/hm_ad_provider/{id}")

    return render(request,"hm_adproviderdoc.html",context)

def ad_distributor(request,id):
    value = request.COOKIES.get('hiringmanager')
    new=[]
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/hiring_manager/signin")
    try:
        mydata = requests.get(f"http://127.0.0.1:3000/hm_my_data/{id}").json()[0] 
        my_user = requests.get(f"http://127.0.0.1:3000/hm_my_users_data/{id}").json()
        access = "" 
        idd = id
    except:
        mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]
        access = mydata['access_Privileges']  
        print(access)
        idd = mydata['aid']
    print(mydata) 
    #ad provider
    if requests.get(f"http://127.0.0.1:3000/hm_my_data/{idd}").json()[0]['ad_distributor'] == None:
        ad_pro_data =""
    else:
        ad_pro_data = jsondec.decode(requests.get(f"http://127.0.0.1:3000/hm_my_data/{idd}").json() [0]['ad_distributor'])
        for i in ad_pro_data:
            id_value=i['id_card']
            if id_value == None:
                i['status']="pending"
                new.append(i)
            else:
                i['status']="verified"
                new.append(i) 
    if request.method=="POST":
        if 'uid' in request.POST:
            print(request.POST)
            global uid 
            uid = request.POST['uid']
            return redirect(f"/hiring_manager/hm_ad_distributor_upload/{idd}")
        elif "user_id" in request.POST:
            print("filter")
            filter = {
            'f_u_id': request.POST['user_id'].strip(),
            'f_u_name': request.POST['dis_name'].strip().lower(),
            'f_u_email': request.POST['email'].strip(),
            'f_u_phone': request.POST['mobile'].strip(),
            'f_u_status': request.POST['status'].strip(),
            'f_location' : request.POST['location'].strip()
            
            }

            p = set()

            for x in new:
                if (filter['f_u_id'] == x['uid'] or not filter['f_u_id']) and \
                (filter['f_u_name'] == x['first_name'].lower() or not filter['f_u_name']) and \
                (filter['f_u_email'] == x['email'] or not filter['f_u_email']) and \
                (filter['f_u_phone'] == x['mobile'] or not filter['f_u_phone']) and \
                (filter['f_u_status'] == x['status'] or not filter['f_u_status']) and \
                (filter['f_location'] == x['personal_country'] or not filter['f_location']):
                    p.add(x['uid'])

            new = [ad for ad in ad_pro_data if ad['uid'] in p]
            print(new)
        else:
            print(request.POST)
            print(request.FILES)
        
    context={
        'key':mydata,
        'current_path':request.get_full_path(),
        'ad_pro_data':new,
        'access':access,
    }
    return render(request,"hm_ad_distributor.html",context)

def ad_distributor_doc(request,id):
    value = request.COOKIES.get('hiringmanager')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/hiring_manager/signin")
    mydata = requests.get(f"http://127.0.0.1:3000/hm_my_data/{id}").json()[0]  
    ad_distributor(request,id)
    print(uid)
    ad_pro_my_data = requests.get(f"http://127.0.0.1:3000/ad_dis_my_data/{uid}").json()[0]  
    education  = jsondec.decode(ad_pro_my_data['level_education'])
    study = jsondec.decode(ad_pro_my_data['field_study']) 
    #country api
    neww=[]
    response = requests.get('https://api.first.org/data/v1/countries').json()
    all = requests.get('https://countriesnow.space/api/v0.1/countries/states').json()
    states = json.dumps(all["data"])
    al = (all["data"])
    for x in al:
       name = (x.get("name"))
       neww.append(name)
    countryname = json.dumps(neww)

    context={
        'key':mydata,
        'current_path':request.get_full_path(),
        'ad_pro_my_data':ad_pro_my_data,
        'education':education,
        'study':study,
        'response': response,
        'region': response,
        'all':al,
        'country': countryname,'states': states,
       
    }
    
    if request.method == "POST":
        print(request.POST)
        response = requests.post(f"http://127.0.0.1:3000/ad_distributor_upload_account/{request.POST['uid']}",data=request.POST,files = request.FILES)
        print(response.status_code)
        if response.status_code == 200:
            data={
                'noter_id':id,
                'not_message':"Hiring Manager Verified Your Account",
                'notify_id': uid,
            }
            notify=requests.post("http://127.0.0.1:3000/notification_update/",data=data)
            if notify.status_code == 200:
                status_up=requests.post(f"http://127.0.0.1:3000/ad_dis_notify_status_true/{uid}")
                print(status_up.status_code)
                return redirect(f"/hiring_manager/hm_ad_distributor/{id}")

    return render(request,"hm_addistributordoc.html",context)


def sales(request,id):
    value = request.COOKIES.get('hiringmanager')
    new=[]
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/hiring_manager/signin")
    try:
        mydata = requests.get(f"http://127.0.0.1:3000/hm_my_data/{id}").json()[0] 
        my_user = requests.get(f"http://127.0.0.1:3000/hm_my_users_data/{id}").json()
        access = "" 
        idd = id
    except:
        mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]
        access = mydata['access_Privileges']  
        print(access)
        idd = mydata['aid']
    if requests.get(f"http://127.0.0.1:3000/hm_my_data/{idd}").json()[0]['sales_manager'] == None:
        sales_data =""
    else:
        sales_data = jsondec.decode(requests.get(f"http://127.0.0.1:3000/hm_my_data/{idd}").json()[0]['sales_manager'])
        for i in sales_data:
            id_value=i['id_card']
            if id_value == None:
                i['status']="pending"
                new.append(i)
            else:
                i['status']="verified"
                new.append(i)
    if request.method=="POST":
        if 'uid' in request.POST:
            global uid 
            uid = request.POST['uid']
            return redirect(f"/hiring_manager/hm_sales_person_doc/{idd}")
        elif "user_id" in request.POST:
            print("filter")
            filter = {
            'f_u_id': request.POST['user_id'].strip(),
            'f_u_name': request.POST['name'].strip().lower(),
            'f_u_email': request.POST['email'].strip(),
            'f_u_phone': request.POST['mobile'].strip(),
            'f_u_status' : request.POST['status'].strip(),
            'f_location' : request.POST['location'].strip()
            }

            p = set()

            for x in new:
                if (filter['f_u_id'] == x['uid'] or not filter['f_u_id']) and \
                (filter['f_u_name'] == x['full_name'].lower() or not filter['f_u_name']) and \
                (filter['f_u_email'] == x['email'] or not filter['f_u_email']) and \
                (filter['f_u_phone'] == x['mobile'] or not filter['f_u_phone']) and \
                (filter['f_u_status'] == x['status'] or not filter['f_u_status']) and \
                (filter['f_location'] == x['personal_country'] or not filter['f_location']):
                    p.add(x['uid'])

            new = [ad for ad in sales_data if ad['uid'] in p]
            print(new)
        else:
            pass

    context={
        'key':mydata,
        'current_path':request.get_full_path(),
        'sales_data':new,
        'access':access
    }
    
    return render(request,"hm_sales_person.html",context)

def sales_doc(request,id):
    value = request.COOKIES.get('hiringmanager')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/hiring_manager/signin")
    mydata = requests.get(f"http://127.0.0.1:3000/hm_my_data/{id}").json()[0] 
    sales(request,id)
    sales_my_data = requests.get(f"http://127.0.0.1:3000/sm_my_data/{uid}").json()[0]  
    education  = jsondec.decode(sales_my_data['level_education'])
    study = jsondec.decode(sales_my_data['field_study']) 
    #country api
    neww=[]
    response = requests.get('https://api.first.org/data/v1/countries').json()
    all = requests.get('https://countriesnow.space/api/v0.1/countries/states').json()
    states = json.dumps(all["data"])
    al = (all["data"])
    for x in al:
       name = (x.get("name"))
       neww.append(name)
    countryname = json.dumps(neww)
    context={
        'key':mydata,
        'current_path':request.get_full_path(),
        'sales_my_data':sales_my_data,
         'education':education,
        'study':study,
        'response': response,
        'region': response,
        'all':al,
        'country': countryname,'states': states,
        
    } 
    if request.method == "POST":
        print(request.POST)
        print(request.FILES)
        response = requests.post(f"http://127.0.0.1:3000/sales_upload_account/{request.POST['uid']}",data=request.POST,files = request.FILES)
        print(response.status_code)
        if response.status_code == 200:
            data={
                'noter_id':id,
                'not_message':"Hiring Manager Verified Your Account",
                'notify_id': uid,
            }
            notify=requests.post("http://127.0.0.1:3000/notification_update/",data=data)
            if notify.status_code == 200:
                status_up=requests.post(f"http://127.0.0.1:3000/sm_notify_status_true/{uid}")
                print(status_up.status_code)
                return redirect(f"/hiring_manager/hm_sales_person/{id}")

    return render(request,"hm_sales_person_doc.html",context)

def affiliate_marketing(request,id):
    value = request.COOKIES.get('hiringmanager')
    new=[]
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/hiring_manager/signin")
    try:
        mydata = requests.get(f"http://127.0.0.1:3000/hm_my_data/{id}").json()[0] 
        my_user = requests.get(f"http://127.0.0.1:3000/hm_my_users_data/{id}").json()
        access = "" 
        idd = id
    except:
        mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]
        access = mydata['access_Privileges']  
        print(access)
        idd = mydata['aid']
    if requests.get(f"http://127.0.0.1:3000/hm_my_data/{idd}").json()[0]['affiliate_marketing'] == None:
        af_data =""
    else:
        af_data = jsondec.decode(requests.get(f"http://127.0.0.1:3000/hm_my_data/{idd}").json()[0]['affiliate_marketing'])
        for i in af_data:
            id_value=i['id_card']
            if id_value == None:
                i['status']="pending"
                new.append(i)
            else:
                i['status']="verified"
                new.append(i)
            
    if request.method=="POST":
        if 'uid' in request.POST:
            global uid 
            uid = request.POST['uid']
            return redirect(f"/hiring_manager/hm_affiliate_marketing_upload/{idd}")
        
        elif "user_id" in request.POST:

            filter = {
            'f_u_id': request.POST['user_id'].strip(),
            'f_u_name': request.POST['name'].strip().lower(),
            'f_u_email': request.POST['email'].strip(),
            'f_u_phone': request.POST['mobile'].strip(),
            'f_u_status':request.POST['status'].strip(),
            'f_location' : request.POST["location"].strip()
            }

            p = set()

            for x in new:
                if (filter['f_u_id'] == x['uid'] or not filter['f_u_id']) and \
                (filter['f_u_name'] == x['first_name'].lower() or not filter['f_u_name']) and \
                (filter['f_u_email'] == x['email'] or not filter['f_u_email']) and \
                (filter['f_u_phone'] == x['mobile'] or not filter['f_u_phone']) and \
                (filter['f_u_status'] == x['status'] or not filter['f_u_status']) and \
                (filter['f_location'] == x['personal_country'] or not filter['f_location']):
                    p.add(x['uid'])

            new = [ad for ad in af_data if ad['uid'] in p]
            print(new)
        else:
            pass
        
    context={
        'key':mydata,
        'current_path':request.get_full_path(),
        'af_data':new,
        'access':access,
    }
    
    return render(request,"hm_affiliate_marketing.html",context)

def affiliate_marketing_doc(request,id):
    value = request.COOKIES.get('hiringmanager')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/hiring_manager/signin")
    try:
        mydata = requests.get(f"http://127.0.0.1:3000/hm_my_data/{id}").json()[0] 
        affiliate_marketing(request,id)
        print(uid)
        af_my_data = requests.get(f"http://127.0.0.1:3000/af_my_data/{uid}").json()[0]  
        education  = jsondec.decode(af_my_data['level_education'])
        study = jsondec.decode(af_my_data['field_study']) 
        #country api
        neww=[]
        response = requests.get('https://api.first.org/data/v1/countries').json()
        all = requests.get('https://countriesnow.space/api/v0.1/countries/states').json()
        states = json.dumps(all["data"])
        al = (all["data"])
        for x in al:
            name = (x.get("name"))
            neww.append(name)
        countryname = json.dumps(neww)
        context={
            'key':mydata,
            'current_path':request.get_full_path(),
            'af_my_data':af_my_data,
            'education':education,
            'study':study,
            'response': response,
            'region': response,
            'all':al,
            'country': countryname,'states': states,
        
        } 
        if request.method == "POST":
            print(request.POST)
            print(request.FILES)
            response = requests.post(f"http://127.0.0.1:3000/affiliate_upload_account/{request.POST['uid']}",data=request.POST,files = request.FILES)
            print(response.status_code)
            if response.status_code == 200:
                data={
                'noter_id':id,
                'not_message':"Hiring Manager Verified Your Account",
                'notify_id': uid,
            }
                notify=requests.post("http://127.0.0.1:3000/notification_update/",data=data)
                if notify.status_code == 200:
                    status_up=requests.post(f"http://127.0.0.1:3000/am_notify_status_true/{uid}")
                    print(status_up.status_code)
                return redirect(f"/hiring_manager/hm_affiliate_marketing/{id}")

        return render(request,"hm_affiliate_marketing_upload.html",context)
    except:
        return render(request,"hm_affiliate_marketing_upload.html")

def private_investigator(request,id):
    value = request.COOKIES.get('hiringmanager')
    new=[]
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/hiring_manager/signin")
    try:
        mydata = requests.get(f"http://127.0.0.1:3000/hm_my_data/{id}").json()[0] 
        my_user = requests.get(f"http://127.0.0.1:3000/hm_my_users_data/{id}").json()
        access = "" 
        idd = id
    except:
        mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]
        access = mydata['access_Privileges']  
        print(access)
        idd = mydata['aid']
    if requests.get(f"http://127.0.0.1:3000/hm_my_data/{idd}").json()[0]['private_investigator'] == None:
        pm_data =""
    else:
        pm_data = jsondec.decode(requests.get(f"http://127.0.0.1:3000/hm_my_data/{idd}").json()[0]['private_investigator'])
        for i in pm_data:
            id_value=i['id_card']
            if id_value == None:
                i['status']="pending"
                new.append(i)
            else:
                i['status']="verified"
                new.append(i)
           
    if request.method=="POST":
        if 'uid' in request.POST:
            global uid 
            uid = request.POST['uid']
            return redirect(f"/hiring_manager/hm_private_investigator_upload/{idd}")
        elif "user_id" in request.POST:
            filter = {
            'f_u_id': request.POST['user_id'].strip(),
            'f_u_name': request.POST['name'].strip().lower(),
            'f_u_email': request.POST['email'].strip(),
            'f_u_phone': request.POST['mobile'].strip(),
            'f_u_status':request.POST['status'].strip(),
            'f_location' : request.POST['location'].strip()
            }

            p = set()

            for x in new:
                if (filter['f_u_id'] == x['uid'] or not filter['f_u_id']) and \
                (filter['f_u_name'] == x['first_name'].lower() or not filter['f_u_name']) and \
                (filter['f_u_email'] == x['email'] or not filter['f_u_email']) and \
                (filter['f_u_phone'] == x['mobile'] or not filter['f_u_phone']) and \
                (filter['f_u_status'] == x['status'] or not filter['f_u_status'] ) and \
                (filter['f_location'] == x['personal_country'] or not filter['f_location']):
                    p.add(x['uid'])

            new = [ad for ad in pm_data if ad['uid'] in p]
            print(new)
        else:
            pass
    context={
        'key':mydata,
        'current_path':request.get_full_path(),
        'pm_data':new,
        'access':access,
    }
    
    return render(request,"hm_private_investigator.html",context)

def private_investigator_doc(request,id):
    value = request.COOKIES.get('hiringmanager')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/hiring_manager/signin")
    mydata = requests.get(f"http://127.0.0.1:3000/hm_my_data/{id}").json()[0] 
    private_investigator(request,id)
    pi_my_data = requests.get(f"http://127.0.0.1:3000/pi_my_data/{uid}").json()[0]
    education  = jsondec.decode(pi_my_data['level_education'])
    study = jsondec.decode(pi_my_data['field_study'])   
    #country api
    neww=[]
    response = requests.get('https://api.first.org/data/v1/countries').json()
    all = requests.get('https://countriesnow.space/api/v0.1/countries/states').json()
    states = json.dumps(all["data"])
    al = (all["data"])
    for x in al:
       name = (x.get("name"))
       neww.append(name)
    countryname = json.dumps(neww)
    context={
        'key':mydata,
        'current_path':request.get_full_path(),
        'pi_my_data':pi_my_data,
        'education':education,
        'study':study,
        'response': response,
        'region': response,
        'all':al,
        'country': countryname,'states': states
    } 
    if request.method == "POST":
        print(request.POST)
        print(request.FILES)
        response = requests.post(f"http://127.0.0.1:3000/private_investigator_upload_account/{request.POST['uid']}",data=request.POST,files = request.FILES)
        print(response.status_code)
        if response.status_code == 200:
            data={
                'noter_id':id,
                'not_message':"Hiring Manager Verified Your Account",
                'notify_id': uid,
            }
            notify=requests.post("http://127.0.0.1:3000/notification_update/",data=data)
            if notify.status_code == 200:
                status_up=requests.post(f"http://127.0.0.1:3000/pi_notify_status_true/{uid}")
                print(status_up.status_code)
            return redirect(f"/hiring_manager/hm_private_investigator/{id}")

    return render(request,"hm_private_investigator_upload.html",context)


def hiring_manager(request,id):
    value = request.COOKIES.get('hiringmanager')
    new=[]
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/hiring_manager/signin")
    try:
        mydata = requests.get(f"http://127.0.0.1:3000/hm_my_data/{id}").json()[0] 
        my_user = requests.get(f"http://127.0.0.1:3000/hm_my_users_data/{id}").json()
        access = "" 
        idd = id
    except:
        mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]
        access = mydata['access_Privileges']  
        print(access)
        idd = mydata['aid']
    if requests.get(f"http://127.0.0.1:3000/hm_my_data/{idd}").json()[0]['hiring_manager'] == None:
        hirinng_data =""
    else:
        hirinng_data = jsondec.decode(requests.get(f"http://127.0.0.1:3000/hm_my_data/{idd}").json()[0]['hiring_manager'])
        for i in hirinng_data:
            id_value=i['id_card']
            if id_value == None:
                i['status']="pending"
                new.append(i)
            else:
                i['status']="verified"
                new.append(i)
            
        
    if request.method=="POST":
        if "uid" in request.POST:
            print(request.POST)
            global uid 
            uid = request.POST['uid']
            return redirect(f"/hiring_manager/hm_hiring_manager_doc/{idd}")
        elif "user_id" in request.POST:
            filter = {
            'f_u_id': request.POST['user_id'].strip(),
            'f_u_name': request.POST['name'].strip().lower(),
            'f_u_email': request.POST['email'].strip(),
            'f_u_phone': request.POST['mobile'].strip(),
            'f_u_status':request.POST['status'].strip(),
            'f_location': request.POST['location'].strip()           
            }

            p = set()

            for x in new:
                if (filter['f_u_id'] == x['uid'] or not filter['f_u_id']) and \
                (filter['f_u_name'] == x['first_name'].lower() or not filter['f_u_name']) and \
                (filter['f_u_email'] == x['email'] or not filter['f_u_email']) and \
                (filter['f_u_phone'] == x['mobile'] or not filter['f_u_phone'])and \
                (filter['f_u_status'] == x['status'] or not filter['f_u_status']) and \
                (filter['f_location'] == x['personal_country'] or not filter['f_location']):
                    p.add(x['uid'])

            new = [ad for ad in hirinng_data if ad['uid'] in p]
            print(new)
    context={
        'key':mydata,
        'current_path':request.get_full_path(),
        'hirinng_data':new[::-1],
        'access':access,
    } 
    return render(request,"hm_hiring_manager.html",context)

def hiring_manager_doc(request,id):
    value = request.COOKIES.get('hiringmanager')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/hiring_manager/signin")
    mydata = requests.get(f"http://127.0.0.1:3000/hm_my_data/{id}").json()[0]  
    hiring_manager(request,id)
    hiring_my_data = requests.get(f"http://127.0.0.1:3000/hm_my_data/{uid}").json()[0]  
    education  = jsondec.decode(hiring_my_data['level_education'])
    study = jsondec.decode(hiring_my_data['field_study'])
    #country api
    neww=[]
    response = requests.get('https://api.first.org/data/v1/countries').json()
    all = requests.get('https://countriesnow.space/api/v0.1/countries/states').json()
    states = json.dumps(all["data"])
    al = (all["data"])
    for x in al:
       name = (x.get("name"))
       neww.append(name)
    countryname = json.dumps(neww)
    context={
        'key':mydata,
        'current_path':request.get_full_path(),
        'hiring_my_data':hiring_my_data,
        'education':education,
        'study':study,
        'response': response,
        'region': response,
        'all':al,
        'country': countryname,'states': states,
        
    } 
    if request.method == "POST":
        # print(request.POST)
        print(request.FILES)
        response = requests.post(f"http://127.0.0.1:3000/hiring_upload_account/{request.POST['uid']}",data=request.POST,files = request.FILES)
        print(response.status_code)
        if response.status_code == 200:
            data={
                'noter_id':id,
                'not_message':"Hiring Manager Verified Your Account",
                'notify_id': uid,
            }
            notify=requests.post("http://127.0.0.1:3000/notification_update/",data=data)
            if notify.status_code == 200:
                status_up=requests.post(f"http://127.0.0.1:3000/hm_notify_status_true/{uid}")
                print(status_up.status_code)
            return redirect(f"/hiring_manager/hm_hiring_manager/{id}")
        
    return render(request,"hm_hiring_manager_doc.html",context)

def users(request,id):
    value = request.COOKIES.get('hiringmanager')
    new=[]
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/hiring_manager/signin")
    error = ""
    try:
        mydata = requests.get(f"http://127.0.0.1:3000/hm_my_data/{id}").json()[0] 
        my_user = requests.get(f"http://127.0.0.1:3000/hm_my_users_data/{id}").json()
        access = "" 
        idd = id
        for x in my_user:
            new.append(x)
    except:
        mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]
        access = mydata['access_Privileges']  
        print(access)
        idd = mydata['aid']
        my_user = requests.get(f"http://127.0.0.1:3000/hm_my_users_data/{idd}").json()
        for x in my_user:
            new.append(x)
    print(my_user)
    signin(request)
    if request.method== "POST":
        print(request.POST)
        if "delete" in request.POST:
           response = requests.post(f"http://127.0.0.1:3000/add_user/{id}",data=request.POST)
           print(response.text)
           print(response.status_code)
           return redirect(f"http://127.0.0.1:8001/hiring_manager/hm_users/{id}")
        elif "edit" in request.POST:
            print(request.POST)
            global user_uid
            user_uid = request.POST['edit']
            return redirect(f"/hiring_manager/hm_user_edit/{id}")
        elif "edit_user" in request.POST:
            print(request.POST)
            if request.POST['password'] == request.POST['confirm_password']:
                data={
                    'first_name': request.POST['first_name'],
                    'last_name':request.POST['last_name'],
                        'email': request.POST['email'],
                        'mobile':request.POST['mobile'],
                        'password': request.POST['password'],
                                'access_Privileges':  access,
                                'edit':request.POST['edit_user'],
                }
            # print(data)
            response = requests.post(f"http://127.0.0.1:3000/add_user/{id}",data=data)
            # print(response.text)
            # print(response.status_code)
            if response.status_code == 200:
                return redirect(f"http://127.0.0.1:3000/hiring_manager/hm_users/{id}")
            elif response.status_code == 203:
                print("user already exist")
                error = "User Already Exixts"

        elif "user_id" in request.POST:
            filter = {
            'f_u_id': request.POST['user_id'],
            'f_u_name': request.POST['user_name'].lower(),
            'f_u_email': request.POST['user_email'],
            'f_u_phone': request.POST['user_phone'],
            
            }

            p = set()

            for x in new:
                if (filter['f_u_id'] == x['uid'] or not filter['f_u_id']) and \
                (filter['f_u_name'] == x['first_name'].lower() or not filter['f_u_name']) and \
                (filter['f_u_email'] == x['email'] or not filter['f_u_email']) and \
                (filter['f_u_phone'] == x['mobile'] or not filter['f_u_phone']) :
                    p.add(x['uid'])

            new = [ad for ad in my_user if ad['uid'] in p]
            print(new)

    context={
        'key':mydata,
        'current_path':request.get_full_path(),
        'my_user':new[::-1],
        'error':error,
        'access':access,

    
    }
    return render(request,"hm_users.html",context)


def add_users(request,id):
    value = request.COOKIES.get('hiringmanager')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/hiring_manager/signin")
    error=""
    mydata = requests.get(f"http://127.0.0.1:3000/hm_my_data/{id}").json()[0]
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
                             'work':"hiring_manager",
                             'creator':id,
                                # 'location':request.POST['location']
            }
           print(data)
           response = requests.post(f"http://127.0.0.1:3000/hm_add_user/{id}",data=data)
           print(response.text)
           print(response.status_code)
           if response.status_code == 200:
              return redirect(f"http://127.0.0.1:3000/hiring_manager/hm_users/{id}")
           elif response.status_code == 203:
              print("user already exist")
              error = "User Already Exixts"
    context={
        'key':mydata,
        'current_path':request.get_full_path(),
        'error':error,

    }

    return render(request,"hm_addusers.html",context)


def hm_user_edit(request,id):
    value = request.COOKIES.get('hiringmanager')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/hiring_manager/signin")
    users(request,id)
    print(user_uid)
    try:
        mydata = requests.get(f"http://127.0.0.1:3000/hm_my_data/{id}").json()[0] 
        my_user = requests.get(f"http://127.0.0.1:3000/hm_my_users_data/{id}").json()
        access = "" 
        idd = id
    except:
        mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]
        access = mydata['access_Privileges']  
        print(access)
        idd = mydata['aid']
    error=""
    hm_my_users_data   = requests.get(f"http://127.0.0.1:3000/single_users_data/{user_uid}").json()[0]
    print(hm_my_users_data)
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
           response = requests.post(f"http://127.0.0.1:3000/hm_add_user/{id}",data=data)
           print(response.text)
           print(response.status_code)
           if response.status_code == 200:
              return redirect(f"http://127.0.0.1:3000/hiring_manager/hm_users/{id}")
           elif response.status_code == 203:
              print("user already exist")
              error = "User Already Exixts"
    context={
        'key':mydata,
        'current_path':request.get_full_path(),
        'error':error,
        'hm_my_users_data':hm_my_users_data,

    }

    return render(request,"hm_user_edit.html",context)


def setting(request,id):
    value = request.COOKIES.get('hiringmanager')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/hiring_manager/signin")
    try:
        mydata = requests.get(f"http://127.0.0.1:3000/hm_my_data/{id}").json()[0] 
        my_user = requests.get(f"http://127.0.0.1:3000/hm_my_users_data/{id}").json()
        access = "" 
        idd = id
    except:
        mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]
        access = mydata['access_Privileges']  
        print(access)
        idd = mydata['aid']
    mydata = requests.get(f"http://127.0.0.1:3000/hm_my_data/{id}").json()[0]  
    context={
        'key':mydata,
        'current_path':request.get_full_path(),
        'access' : access
    }
    if request.method=="POST":
        print(request.POST)
        if 'pass_reset' in request.POST:
            a=request.POST["pass_reset"]
            print(a)
            response = requests.post(f"http://127.0.0.1:3000/hm_password_reset/{id}",data=request.POST )
        else:
            print(request.POST)
            response = requests.post(f"http://127.0.0.1:3000/hm_email_update/{id}", data = request.POST)
            print(response)
            return render(request,"hm_acc_setting.html",context)
    return render(request,"hm_acc_setting.html",context)


# //// HM Settings Password Reset////
def hm_password_reset(request,id):
 #   value = request.COOKIES.get('hiringmanager')
  #  if value != None:
   #     print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    #else:
     #   return redirect("/hiring_manager/signin")
    print(id)
    if request.method=="POST":
        print(request.POST)
        if 'pass_reset' in request.POST:
            
            a=request.POST["pass_reset"]
            print(a)
        if request.POST['password'] == request.POST['confirm_password']:

            response = requests.post(f"http://127.0.0.1:3000/hm_password_update/{id}",data=request.POST )
            messages.info(request,"Password Successfully Updated")
        else:
            messages.info(request,"Password Incorrect")
    return render(request,"ad_dis_password_reset.html")

# //// Forget Password/////
def hm_forget_password(request):
#    value = request.COOKIES.get('hiringmanager')
 #   if value != None:
  #      print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
   # else:
    #    return redirect("/hiring_manager/signin")
    error=""
    if request.method == "POST":
        
        print(request.POST)
        response = requests.post("http://127.0.0.1:3000/hm_forget_password/",data=request.POST)
        print(response)
        print(response.status_code)
        print(type(jsondec.decode(response.text)))
        print(jsondec.decode(response.text))
        uidd = jsondec.decode(response.text)
        
        if response.status_code == 200:
            return redirect(f"/hm_forgetpassword_otpp/{uidd}")
        elif response.status_code == 403:
            error = "User Doesn't Exist"

    context = {'error':error}
    return render(request,"hm_email.html",context)
    

def hm_forgetpassword_otp(request,id):
#    value = request.COOKIES.get('hiringmanager')
 #   if value != None:
  #      print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
   # else:
    #    return redirect("/hiring_manager/signin")
    mydata = requests.get(f"http://127.0.0.1:3000/hm_my_data/{id}").json()[0]
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
        response = requests.post(f"http://127.0.0.1:3000/hm_forget_password_otp/{id}", data=data)
       
        print(response)
        print(response.status_code)
        print(data['user_otp1'])
        print(response.text)
        uidd = (response.text[1:-1])
        
        if response.status_code == 200:
            return redirect(f"/hm_forgetpassword_resett/{uidd}")
        else:
            invalid = "Invalid OTP"
            context = {'invalid':invalid}
    return render(request,"hm_otpcheck.html",context)


def hm_forgetpassword_reset(request,id):
    #value = request.COOKIES.get('hiringmanager')
   # if value != None:
  #      print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
 #   else:
#        return redirect("/hiring_manager/signin")
    error=""
    mydata = requests.get(f"http://127.0.0.1:3000/hm_my_data/{id}").json()[0]
    print(id)
    if request.method=="POST":
        print(request.POST)
        if request.POST['password'] == request.POST['confirm_password']:
            response = requests.post(f"http://127.0.0.1:3000/hm_password_update/{id}",data=request.POST )
            print(response)
            return redirect(f"/hiring_manager/signin/")

        else:
            print(response)
            error="password mismatch"
    context = {'invalid':"invalid",
                'key':mydata,
                'error':error
                }
    return render(request,"hm_forgetpassword.html",context)

def get(request,id,type, *args, **kwargs):
        data = requests.get(f"http://127.0.0.1:3000/{type}/{id}").json()[0] 
        education  = jsondec.decode(data['level_education'])
        study = jsondec.decode(data['field_study'])
        img = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/da/Cup_and_Saucer_LACMA_47.35.6a-b_%281_of_3%29.jpg/640px-Cup_and_Saucer_LACMA_47.35.6a-b_%281_of_3%29.jpg" 
        # getting the template
        pdf = html_to_pdf('pdf.html',context_dict={'pdf':data,'education':education,'study':study,'img':img})
        
        # rendering the template
        return HttpResponse(pdf, content_type='application/pdf')
        # return render(request,"pdf.html" ,{'pdf':data,'education':education,'study':study,'img':img})

