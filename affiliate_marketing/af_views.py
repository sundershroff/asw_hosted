from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
import requests
import json
from django.contrib import messages
from django.contrib.auth import logout
# Create your views here.

jsondec = json.decoder.JSONDecoder()

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

    return render(request,"af_createaccount.html",context)

def signin(request):
    value = request.COOKIES.get('afilliate')
    print(value)
    error = ""
    context = {'error':error}
    if request.method == "POST":
        print(request.POST)
        # response = requests.post("http://54.159.186.219:8000/signin/",data=request.POST)
        response = requests.post("http://127.0.0.1:3000/am_signin/",data=request.POST)
        print(response.status_code)
#        print(type(jsondec.decode(response.text)))
 #       print(jsondec.decode(response.text))
        uidd = jsondec.decode(response.text)
        global access_Privileges
        try:
            access_Privileges = uidd['access_Privileges']
            uid = uidd['uid']
        except:
            access_Privileges = ""
            uid = uidd
        if response.status_code == 200:
            mydata = requests.get(f"http://127.0.0.1:3000/my_aff_data/{uid}").json()[0]
            id_card_data = mydata.get('id_card')
            hm = mydata.get('hiring_manager')
            if id_card_data is None:
                if hm is not None: 
                    alert_message="You are under Verification Process...."
                    context['alert_message'] = alert_message
                    return render(request,"af_signin.html",context)
                    
                else:
                    return redirect(f"/affiliate_marketing/af_uploadprofile/{uid}")
                
            elif id_card_data is not None:
                response = redirect(f"/affiliate_marketing/af_marketingdashboard/{uid}")
                response.set_cookie("afilliate",uid)
                return response
                
            
        elif response.status_code == 401:
            delete_hm = requests.delete("http://127.0.0.1:3000/am_delete_data/",data=request.POST)
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
          error = "YOUR EMAILID OR PASSWORD IS INCORRECT"
    context = {'error':error}
    return render(request,"af_signin.html",context)

def signup(request):
    error = ""
    if request.method == "POST":
        print(request.POST)
        if request.POST['password'] == request.POST['confirm_password']:
            if request.POST["referral_code"] =="" :
                referral_code="empty"
                    
            else:
                referral_code=request.POST["referral_code"]

            data={
                'email': request.POST["email"],
                'mobile': request.POST["mobile"],
                'password': request.POST["password"],
                'referral_code':referral_code,
                'full_name': request.POST['first_name']+request.POST['last_name'],

            }
            print(data)
            # response = requests.post('http://54.159.186.219:8000/signup/',data=request.POST)
            response = requests.post("http://127.0.0.1:3000/am_signup/",data=data)
            print(response.status_code)
            print(response.text)
            uidd = (response.text[1:-1])
           
            if response.status_code == 200:
                return redirect(f"/affiliate_marketing/otp/{uidd}")
            elif response.status_code == 302:
                error = "User Already Exist"  
                return redirect("/affiliate_marketing/signin/")     
            else:
                pass
        else:
            print("password doesn't match")
    context = {'error':error}
    return render(request,"af_signup.html",context)

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
        response = requests.post(f"http://127.0.0.1:3000/am_otp/{id}", data=data)

       
        print(response)
        print(response.status_code)
        print(data['user_otp'])
        print(response.text)
        uidd = (response.text[1:-1])
        
        if response.status_code == 200:
        # if get["otp"] == data['user_otp']:
            # return redirect(f"/profileidcard/{uidd}")
            return redirect(f"/affiliate_marketing/profile_picture/{uidd}")
        else:
            invalid = "Invalid OTP"
            context = {'invalid':invalid}
    return render(request,"af_otpcheck.html",context)

def profile_picture(request,id):
    if request.method == "POST":
        print(request.FILES)
        # response = requests.post(f"http://54.159.186.219:8000/profileidcard/{id}",   files=request.FILES)
        response = requests.post(f"http://127.0.0.1:3000/am_profile_picture/{id}",   files=request.FILES)
        print(response)
        print(response.status_code)
        print(response.text)
        uidd = (response.text[1:-1])
        if response.status_code == 200:
        # if get["otp"] == data['user_otp']:
            return redirect(f"/affiliate_marketing/af_uploadprofile/{uidd}")
        else:
            pass
    return render(request,"af_profilepicture.html")

def upload_acc(request,id):
    try:
        hiring_manager = requests.get("http://127.0.0.1:3000/all_hm_data/").json()
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
                        'country': countryname,'states': states,'hiring_manager':hiring_manager}
        if request.method == "POST":
            uid=request.POST['hiring_manager']
            # print(request.FILES)
            dictio = dict(request.POST)
            print(dictio)
            # response = requests.post(f"http://54.159.186.219:8000/profileidcard/{id}",   files=request.FILES)
            response = requests.post(f"http://127.0.0.1:3000/am_upload_account/{id}", data = dictio,files=request.FILES)
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
                return redirect("/affiliate_marketing/signin/")
            else:
                pass
        return render(request,"af_uploadprofile.html",context)
    except:
        return render(request,"af_uploadprofile.html")

def signout(request):
    value = request.COOKIES.get('afilliate')
    print(value)
    response = redirect("/affiliate_marketing/signin/")
    # response = HttpResponse("delete cookie")
    response.delete_cookie("afilliate")
    return response
    
def admin_dashboard(request,id):
    value = request.COOKIES.get('afilliate')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/affiliate_marketing/signin/")
    try:
        access = ""
        #Notification
        if requests.get(f"http://127.0.0.1:3000/notification_data/{id}") == None:
            notification_data=""
            
        else:
            notification = requests.get(f"http://127.0.0.1:3000/notification_data/{id}")
            notification_data = json.loads(notification.text)
        if request.method == "POST":
            new=[]
            
            mydata = requests.get(f"http://127.0.0.1:3000/my_aff_data/{id}").json()[0]  
            all_profile_finder = requests.get("http://127.0.0.1:3000/alluserdata/").json()
            all_aff_details=requests.get("http://127.0.0.1:3000/all_aff_details").json()
            print("all_profilefinders",all_profile_finder)
            all_profile_data=requests.get("http://127.0.0.1:3000/my_profile_finder_data/").json()

            # all_date=requests.get(f"http://127.0.0.1:3000/date_in_range/{id}").json()
            # print(all_date)
            for p in all_profile_data:
                h=p.get("referral_code")
                if h == id:
                    # print("profile_finder",p)
                    new.append(p)

            for i in all_aff_details:    
                a=(i.get("referral_code"))
                # print(a)
                if id == a:
                    new.append(i)
            
            
            data = {
                'from_date':request.POST["from_date"],
                'to_date': request.POST["to_date"],
                    }
            print(data)
            response = requests.post(f"http://127.0.0.1:3000/date_date/{id}", data = data)

            print(response)
        
            if response.status_code == 200:

                print("Request was successful")
                response.text
                print(response.text)
                print(type(jsondec.decode(response.text)))
                all_date=jsondec.decode(response.text)
                
                
    
            else:
                print(f"Request failed with status code {response.status_code}")
            context={
                'key':mydata,
                'current_path':request.get_full_path(),
                'all_profile_finder':all_profile_finder[::-1],
                'all_data':new[::-1],
                'all_date':all_date, 
                'access' : access,
                'notification' :notification_data

            }
            
        else:
            new=[]
            mydata = requests.get(f"http://127.0.0.1:3000/my_aff_data/{id}").json()[0]  
            all_profile_finder = requests.get("http://127.0.0.1:3000/alluserdata/").json()
            all_aff_details=requests.get("http://127.0.0.1:3000/all_aff_details").json()
            all_profile_data=requests.get("http://127.0.0.1:3000/my_profile_finder_data/").json()
            #Notification
            if requests.get(f"http://127.0.0.1:3000/notification_data/{id}") == None:
                notification=""
                
            else:
                notification = requests.get(f"http://127.0.0.1:3000/notification_data/{id}")
                notification_data = json.loads(notification.text)

            for p in all_profile_data:
                h=p.get("referral_code")
                if h == id:
                    # print("profile_finder",p)
                    new.append(p)



            for i in all_aff_details:    
                a=(i.get("referral_code"))
                # print(a)
                if id == a:
                    new.append(i)
            context={
                'key':mydata,
                'current_path':request.get_full_path(),
                'all_profile_finder':all_profile_finder[::-1],
                'all_data':new[::-1],
                'access':access,
                'notification' :notification_data
                           
            }
        return render(request,"af_marketingdashboard.html",context)
    except:
        if request.method == "POST":
            new=[]
            mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]  
            all_profile_finder = requests.get("http://127.0.0.1:3000/alluserdata/").json()
            all_aff_details=requests.get("http://127.0.0.1:3000/all_aff_details").json()
            print("all_profilefinders",all_profile_finder)
            all_profile_data=requests.get("http://127.0.0.1:3000/my_profile_finder_data/").json()
            access = mydata['access_Privileges']
            #Notification
            if requests.get(f"http://127.0.0.1:3000/notification_data/{id}") == None:
                notification_data=""
                
            else:
                notification = requests.get(f"http://127.0.0.1:3000/notification_data/{id}")
                notification_data = json.loads(notification.text)
            # all_date=requests.get(f"http://127.0.0.1:3000/date_in_range/{id}").json()
            # print(all_date)
            for p in all_profile_data:
                h=p.get("referral_code")
                if h == id:
                    # print("profile_finder",p)
                    new.append(p)

            for i in all_aff_details:    
                a=(i.get("referral_code"))
                # print(a)
                if id == a:
                    new.append(i)
            
            
            data = {
                'from_date':request.POST["from_date"],
                'to_date': request.POST["to_date"],
                    }
            print(data)
            response = requests.post(f"http://127.0.0.1:3000/date_date/{id}", data = data)

            print(response)
        
            if response.status_code == 200:

                print("Request was successful")
                response.text
                print(response.text)
                print(type(jsondec.decode(response.text)))
                all_date=jsondec.decode(response.text)
                
                
    
            else:
                print(f"Request failed with status code {response.status_code}")
            context={
                'key':mydata,
                'current_path':request.get_full_path(),
                'all_profile_finder':all_profile_finder[::-1],
                'all_data':new[::-1],
                'all_date':all_date, 
                'access':access,  
                'notification' :notification_data
            }
            
        else:
            new=[]
            mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]  
            all_profile_finder = requests.get("http://127.0.0.1:3000/alluserdata/").json()
            all_aff_details=requests.get("http://127.0.0.1:3000/all_aff_details").json()
            all_profile_data=requests.get("http://127.0.0.1:3000/my_profile_finder_data/").json()
            access = mydata['access_Privileges']
            #Notification
            if requests.get(f"http://127.0.0.1:3000/notification_data/{id}") == None:
                notification_data=""
                
            else:
                notification = requests.get(f"http://127.0.0.1:3000/notification_data/{id}")
                notification_data = json.loads(notification.text)
            for p in all_profile_data:
                h=p.get("referral_code")
                if h == id:
                    # print("profile_finder",p)
                    new.append(p)



            for i in all_aff_details:    
                a=(i.get("referral_code"))
                # print(a)
                if id == a:
                    new.append(i)
            context={
                'key':mydata,
                'current_path':request.get_full_path(),
                'all_profile_finder':all_profile_finder[::-1],
                'all_data':new[::-1],
                'access':access,
                'notification' :notification_data
                            

                
            }
        return render(request,"af_marketingdashboard.html",context)

def profile(request,id):
    value = request.COOKIES.get('afilliate')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/affiliate_marketing/signin/")
    try:
        mydata = requests.get(f"http://127.0.0.1:3000/my_aff_data/{id}").json()[0] 
        education  = jsondec.decode(mydata['level_education'])
        study = jsondec.decode(mydata['field_study'])
        context={
            'key':mydata,
            'current_path':request.get_full_path(),
            'access':"",
            'education':education,
        'study':study,
        }
        return render(request,"af_profile.html",context)

    except:
        mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]  
        access = mydata['access_Privileges']

        context={
            'key':mydata,
            'current_path':request.get_full_path(),
            'access':access,
        }
        return render(request,"af_profile.html",context)
def edit_profile(request,id):
    value = request.COOKIES.get('afilliate')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/affiliate_marketing/signin/")
    try:
        mydata = requests.get(f"http://127.0.0.1:3000/my_aff_data/{id}").json()[0]       
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
            

        context = {"key":mydata,
                'current_path':request.get_full_path(),'response': response, 'region': response,'all':al,
                    'country': countryname,'states': states,'key':mydata,
                    'current_path':request.get_full_path()}
        
        if request.method=="POST":
            print(request.POST)
            response = requests.post(f"http://127.0.0.1:3000/am_edit_account/{id}", data = request.POST,files=request.FILES)
            print(response)
            print(response.status_code)
            print(response.text)
            return redirect(f"/affiliate_marketing/af_profile/{id}")
        return render(request,"af_editprofile.html",context)
        
            
    except:
        return render(request,"af_editprofile.html")


def commisions(request,id):
    value = request.COOKIES.get('afilliate')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/affiliate_marketing/signin/")
    try:
        access=""
        new=[]
        mydata = requests.get(f"http://127.0.0.1:3000/my_aff_data/{id}").json()[0]
        # print(mydata)
        all_aff_details=requests.get("http://127.0.0.1:3000/all_aff_details").json()
        all_profile_data=requests.get("http://127.0.0.1:3000/my_profile_finder_data/").json()


        for p in all_profile_data:
            h=p.get("referral_code")
            if h == id:
                # print("profile_finder",p)
                new.append(p)
        for i in all_aff_details:    
            a=(i.get("referral_code"))
            # print(a)
            if id == a:
                new.append(i)
        coin=(len(new)*1)
        data={
            "coin":coin
        }
        response=requests.post(f"http://127.0.0.1:3000/aff_coin/{id}",data=data).json()[0]
        print(response)
        
        context={
            'key':mydata,
            'current_path':request.get_full_path(),
            'all_data':new[::-1],
            'access':"",

        }
        return render(request,"af_commisions.html",context)
    except:
        new=[]
        # print(mydata)
        mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]  
        access = mydata['access_Privileges']
        all_aff_details=requests.get("http://127.0.0.1:3000/all_aff_details").json()
        all_profile_data=requests.get("http://127.0.0.1:3000/my_profile_finder_data/").json()
        idd = mydata['aid']

        for p in all_profile_data:
            h=p.get("referral_code")
            if h == idd:
                # print("profile_finder",p)
                new.append(p)
        for i in all_aff_details:    
            a=(i.get("referral_code"))
            # print(a)
            if idd == a:
                new.append(i)
        coin=(len(new)*1)
        data={
            "coin":coin
        }
        response=requests.post(f"http://127.0.0.1:3000/aff_coin/{idd}",data=data).json()[0]
        print(response)
        
        context={
            'key':mydata,
            'current_path':request.get_full_path(),
            'all_data':new[::-1],
            'access':access,

        }
        return render(request,"af_commisions.html",context)
def setting(request,id):
    value = request.COOKIES.get('afilliate')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/affiliate_marketing/signin/")
    try:
       mydata = requests.get(f"http://127.0.0.1:3000/my_aff_data/{id}").json()[0]
       access = ""
    except:
       mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]
       access = mydata['access_privileges']
    context={
        'key':mydata,
        'current_path':request.get_full_path(),
        'access' :access,
    }
    if request.method=="POST":
        print(request.POST)
        if 'pass_reset' in request.POST:
            
            a=request.POST["pass_reset"]
            print(a)
       
            response = requests.post(f"http://127.0.0.1:3000/password_aff_reset/{id}",data=request.POST )
        else:
            print(request.POST)
            response = requests.post(f"http://127.0.0.1:3000/aff_email_update/{id}", data = request.POST)
            print(response)
            print(response.status_code)
            print(response.text)
            return render(request,"af_setting.html",context)


    return render(request,"af_setting.html",context)

def password_reset(request,id):
#    value = request.COOKIES.get('afilliate')
 #   if value != None:
  #      print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
   # else:
    #    return redirect("/affiliate_marketing/signin/")
    print(id)
    if request.method=="POST":
        print(request.POST)
        if 'pass_reset' in request.POST:
            
            a=request.POST["pass_reset"]
            print(a)
        if request.POST['password'] == request.POST['confirm_password']:

            response = requests.post(f"http://127.0.0.1:3000/pass_aff_update/{id}",data=request.POST )
            messages.info(request,"Password Successfully Updated")
        else:
            messages.info(request,"Password Incorrect")
    return render(request,"password_aff_reset.html")



def users(request,id):
    value = request.COOKIES.get('afilliate')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/affiliate_marketing/signin/")
    try:
        new=[]
        error = ""
        mydata = requests.get(f"http://127.0.0.1:3000/my_aff_data/{id}").json()[0]  
        my_user = requests.get(f"http://127.0.0.1:3000/am_my_users_data/{id}").json()
        print(my_user)
        access=""
        for x in my_user:
            new.append(x)

    except:
        new=[]
        error = ""
        mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]  
        # print(mydata['aid'])
        my_user = requests.get(f"http://127.0.0.1:3000/am_my_users_data/{mydata['aid']}").json()
        print(my_user)
        access = mydata['access_Privileges']
        for x in my_user:
            new.append(x)

    if request.method== "POST":
        print(request.POST)
        if "delete" in request.POST:
           response = requests.post(f"http://127.0.0.1:3000/am_add_user/{id}",data=request.POST)
           print(response.text)
           print(response.status_code)
           return redirect(f"/affiliate_marketing/am_users/{id}")
        elif "edit" in request.POST:
            print(request.POST)
            global user_uid
            user_uid = request.POST['edit']
            return redirect(f"/affiliate_marketing/am_user_edit/{id}")
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
            response = requests.post(f"http://127.0.0.1:3000/am_add_user/{id}",data=data)
            # print(response.text)
            # print(response.status_code)
            if response.status_code == 200:
                return redirect(f"http://51.20.61.70:8001/affiliate_marketing/am_users/{id}")
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

    context={
        'key':mydata,
        'current_path':request.get_full_path(),
        'my_user':new,
        'error':error,
        'access':access,    
    }
    return render(request,"am_users.html",context)


def add_users(request,id):
    value = request.COOKIES.get('afilliate')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/affiliate_marketing/signin/")
    
    error=""
    try:
        mydata = requests.get(f"http://127.0.0.1:3000/my_aff_data/{id}").json()[0]
        access_Privileges = ""
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
                                'work':"affiliate_marketing",
                                'creator':id,
                                    # 'location':request.POST['location']
                }
            print(data)
            response = requests.post(f"http://127.0.0.1:3000/am_add_user/{id}",data=data)
            print(response.text)
            print(response.status_code)
            if response.status_code == 200:
                return redirect(f"http://127.0.0.1:3000/affiliate_marketing/am_users/{id}")
            elif response.status_code == 203:
                print("user already exist")
                error = "User Already Exixts"
        context={
            'key':mydata,
            'current_path':request.get_full_path(),
            'error':error,
            'access':access_Privileges,


        }

        return render(request,"am_addusers.html",context)
    except:
        mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]
        access_Privileges = mydata['access_Privileges']
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
                                'work':"affiliate_marketing",
                                'creator':mydata['aid'],
                                    # 'location':request.POST['location']
                }
            print(data)
            response = requests.post(f"http://127.0.0.1:3000/am_add_user/{id}",data=data)
            print(response.text)
            print(response.status_code)
            if response.status_code == 200:
                return redirect(f"http://127.0.0.1:3000/affiliate_marketing/am_users/{id}")
            elif response.status_code == 203:
                print("user already exist")
                error = "User Already Exixts"
        context={
            'key':mydata,
            'current_path':request.get_full_path(),
            'error':error,
            'access':access_Privileges,

        }
        return render(request,"am_addusers.html",context)


def am_user_edit(request,id):
    value = request.COOKIES.get('afilliate')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/affiliate_marketing/signin/")
    users(request,id)
    print(user_uid)
    error=""
    try:
        mydata = requests.get(f"http://127.0.0.1:3000/my_aff_data/{id}").json()[0]
        am_my_users_data   = requests.get(f"http://127.0.0.1:3000/single_users_data/{user_uid}").json()[0]
        print(am_my_users_data)
    except:
        mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]
        am_my_users_data   = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]

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
           response = requests.post(f"http://127.0.0.1:3000/am_add_user/{id}",data=data)
           print(response.text)
           print(response.status_code)
           if response.status_code == 200:
              return redirect(f"http://127.0.0.1:3000/affiliate_marketing/am_users/{id}")
           elif response.status_code == 203:
              print("user already exist")
              error = "User Already Exixts"
    context={
        'key':mydata,
        'current_path':request.get_full_path(),
        'error':error,
        'am_my_users_data':am_my_users_data,

    }

    return render(request,"am_user_edit.html",context)



def aff_forget_password(request):
#    value = request.COOKIES.get('afilliate')
 #   if value != None:
  #      print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
   # else:
    #    return redirect("/affiliate_marketing/signin/")
    error=""
    if request.method == "POST":
        print(request.POST)
        response = requests.post("http://127.0.0.1:3000/aff_forget_password/",data=request.POST)
        print(response)
        print(response.status_code)
        print(type(jsondec.decode(response.text)))
        print(jsondec.decode(response.text))
        uidd = jsondec.decode(response.text)
        
        if response.status_code == 200:
            return redirect(f"/aff_forgetpassword_otpp/{uidd}")
        elif response.status_code == 403:
            error = "User Doesn't Exist"

    context = {'error':error}
    return render(request,"aff_email.html",context)


def aff_forgetpassword_otp(request,id):
#    value = request.COOKIES.get('afilliate')
 #   if value != None:
  #      print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
   # else:
    #    return redirect("/affiliate_marketing/signin/")
    mydata = requests.get(f"http://127.0.0.1:3000/my_aff_data/{id}").json()[0]
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
        response = requests.post(f"http://127.0.0.1:3000/aff_forget_password_otp/{id}", data=data)
       
        print(response)
        print(response.status_code)
        print(data['user_otp1'])
        print(response.text)
        uidd = (response.text[1:-1])
        
        if response.status_code == 200:
            return redirect(f"/aff_forgetpassword_resett/{uidd}")
        else:
            invalid = "Invalid OTP"
            context = {'invalid':invalid}
    return render(request,"af_otpcheck.html",context)


def aff_forgetpassword_reset(request,id):
#    value = request.COOKIES.get('afilliate')
 #   if value != None:
  #      print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
   # else:
    #    return redirect("/affiliate_marketing/signin/")
    error=""
    mydata = requests.get(f"http://127.0.0.1:3000/my_aff_data/{id}").json()[0]
    print(id)
    if request.method=="POST":
        print(request.POST)
        if request.POST['password'] == request.POST['confirm_password']:
            response = requests.post(f"http://127.0.0.1:3000/pass_aff_update/{id}",data=request.POST )
            print(response)
            return redirect(f"/affiliate_marketing/signin/")

        else:
            print(response)
            error="password mismatch"
    context = {'invalid':"invalid",
                'key':mydata,
                'error':error}
    return render(request,"aff_forgetpassword.html",context)





