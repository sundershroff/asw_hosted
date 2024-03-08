from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
import requests
import json
from rest_framework.response import Response
from django.contrib import messages
from collections import Counter
from django.contrib.auth import logout,authenticate


# Create your views here.
jsondec = json.decoder.JSONDecoder()
global access_Privileges
access_Privileges = ""


def dashboard(request):
    return render(request,"dashboard.html")

def signup(request):
    error = ""
    if request.method == "POST":
        if request.POST['password'] == request.POST['confirm_password']:
                # response = requests.post('http://54.159.186.219:8000/signup/',data=request.POST)
                response = requests.post("http://127.0.0.1:3000/sm_signup/",data=request.POST)
                print(response.status_code)
                print(response.text)
                uidd = (response.text[1:-1])
                print(uidd)
                if response.status_code == 200:
                   return redirect(f"/sales_manager/otp/{uidd}")
                elif response.status_code == 302:
                    error = "User Already Exist"
        else:
            print("password doesn't match")
    context = {'error':error}
    return render(request,"sm_signup.html",context)

def signin(request):
    value = request.COOKIES.get('ad_provider')
    print(value)
    error = ""
    if request.method == "POST":
        print(request.POST)
        # response = requests.post("http://54.159.186.219:8000/signin/",data=request.POST)
        response = requests.post("http://127.0.0.1:3000/sm_signin/",data=request.POST)
#        print(response.status_code)
 #       print(type(jsondec.decode(response.text)))
  #      print(jsondec.decode(response.text))
        uidd = jsondec.decode(response.text)
        global access_Privileges
        try:
            access_Privileges = uidd['access_Privileges']
            uid = uidd['uid']

        except:
            access_Privileges = ""
            uid = uidd
        if response.status_code == 200:
            response = redirect(f"/sales_manager/sm_salesdashboard/{uid}")
            response.set_cookie("sales_manager",uid)
            return response
        else:
          error = "YOUR EMAILID OR PASSWORD IS INCORRECT"
    context = {'error':error}
    return render(request,"sm_signin.html",context)

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
        response = requests.post(f"http://127.0.0.1:3000/sm_otp/{id}", data=data)

       
        print(response)
        print(response.status_code)
        print(data['user_otp'])
        print(response.text)
        uidd = (response.text[1:-1])
        
        if response.status_code == 200:
        # if get["otp"] == data['user_otp']:
            # return redirect(f"/profileidcard/{uidd}")
            return redirect(f"/sales_manager/profile_picture/{uidd}")
        else:
            invalid = "Invalid OTP"
            context = {'invalid':invalid}
    return render(request,"sm_otpcheck.html",context)

def profile_picture(request,id):
    if request.method == "POST":
        print(request.FILES)
        # response = requests.post(f"http://54.159.186.219:8000/profileidcard/{id}",   files=request.FILES)
        response = requests.post(f"http://127.0.0.1:3000/sm_profile_picture/{id}",   files=request.FILES)
        print(response)
        print(response.status_code)
        print(response.text)
        uidd = (response.text[1:-1])
        if response.status_code == 200:
        # if get["otp"] == data['user_otp']:
            return redirect(f"/sales_manager/sm_upload_profile/{uidd}")
        else:
            return HttpResponse("INVALId")
    return render(request,"sm_profilepicture.html")

def upload_acc(request,id):
    try:
        #hiring manager list
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
            # print(request.POST)
            # print(request.FILES)
            dictio = dict(request.POST)
            print(dictio)
            # response = requests.post(f"http://54.159.186.219:8000/profileidcard/{id}",   files=request.FILES)
            response = requests.post(f"http://127.0.0.1:3000/sm_upload_account/{id}",   data = dictio,files=request.FILES)
            print(response)
            print(response.status_code)
            print(response.text)
            uidd = (response.text[1:-1])
            if response.status_code == 200:
            # if get["otp"] == data['user_otp']:
                # return redirect(f"/sales_manager/sm_salesdashboard/{uidd}")
                return redirect(f"/sales_manager/sm_verification_fee/{uidd}")

            else:
                pass
        return render(request,"sm_upload_profile.html",context)
    except:
        return render(request,"sm_upload_profile.html")

def signout(request):
    value = request.COOKIES.get('sales_manager')
    print(value)
    response = redirect("/sales_manager/signin/")
    # response = HttpResponse("delete cookie")
    response.delete_cookie("sales_manager")
    return response



def admin_dashboard(request,id):
    value = request.COOKIES.get('sales_manager')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/sales_manager/signin/")
    jsondec = json.decoder.JSONDecoder()
    try:
        c=[]
        sm_ads=[]
        access=""

        mydata = requests.get(f"http://127.0.0.1:3000/sm_my_data/{id}").json()[0]
        print(mydata)
        all_profile_finder = requests.get("http://127.0.0.1:3000/alluserdata/").json()
        all_client_data=requests.get("http://127.0.0.1:3000/all_client_data/").json()

        allads=requests.get("http://127.0.0.1:3000/adprovider_ads/").json()
        # addistributor
        alldis_ads=requests.get("http://127.0.0.1:3000/addistributor_ads/").json()
        sm_adss=[]
        new1=[]
        new=[]
        ads_count=[]
        for j in alldis_ads:
            addis=jsondec.decode(j["ad_dis"])
            new.append(addis)
            for adis in new:
                d=(adis.get("sales_manager"))
                if id == d:
                    sm_ads.append(j)
                    ads_count.append(j)
                    break
        totalcoin= 0
        for item in sm_ads:
            if item['coin'] != None:
                totalcoin+=int(item['coin'])

        # adprovider displaying
        for i in allads:
            b=jsondec.decode(i['ad_pro'])
            new1.append(b)
            for l in new1:    
                a=(l.get("sales_manager"))
                if id == a:
                    sm_adss.append(i)
                    ads_count.append(i)
                    break

        for item in sm_adss:
            if item['commission']!=None:
                item['amount'] = int(item['commission']) * 10
            
        totalcommission=sum(int(item.get("amount",0))for item in sm_adss)
            
        # client displaying
        
        for i in all_client_data:
            uid=jsondec.decode(i.get("sales_id"))
            id_value = uid["uid"]
            if id_value==id:
                c.append(i)
        
        totalclient=len(c)+len(sm_ads)

        # adtype displaying
        wordtype=[]
        for k in ads_count:
            adtype=(k.get("ad_type"))
            wordtype.append(adtype)
        wordcount=Counter(wordtype)
        result=[{"word":word , "count":count } for word,count in wordcount.items()]
        # sales_incentives
        target=2
        incent_amount=0
        incentive=[]

        for i in all_client_data:
            if i.get("active_status") == True:
                incentive.append(i)
            if len(incentive) >= target:
                len(incentive) % target == 0
                incent_amount=incent_amount + 100
                incentive.clear()
        # print(incent_amount)
        
                        
        context={
            'key':mydata,
            'current_path':request.get_full_path(),
            'all_profile_finder':all_profile_finder[::-1],
            'all_client_data':c[::-1],
            'access':access,
            'ads_data':sm_ads[::-1],
            'totalcoin':totalcoin,
            'totalclient':totalclient,
            'result':result,
            'total_commission':totalcommission,
            'incent_amount':incent_amount,
        }
        return render(request,"sm_salesdashboard.html",context)

                
    except:
        c=[]
        mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]
        print(mydata)
        access = mydata['access_Privileges']
        all_profile_finder = requests.get("http://127.0.0.1:3000/alluserdata/").json()
        all_client_data=requests.get("http://127.0.0.1:3000/all_client_data/").json()
        allads=requests.get("http://127.0.0.1:3000/adprovider_ads/").json()
        # addistributor
        alldis_ads=requests.get("http://127.0.0.1:3000/addistributor_ads/").json()
        sm_ads=[]
        sm_adss=[]
        new1=[]
        new=[]
        ads_count=[]
        for j in alldis_ads:
            addis=jsondec.decode(j["ad_dis"])
            new.append(addis)
            for adis in new:
                d=(adis.get("sales_manager"))
                if id == d:
                    sm_ads.append(j)
                    ads_count.append(j)
                    break
        totalcoin= 0
        for item in sm_ads:
            if item['coin'] != None:
                totalcoin += int(item['coin'])
        # adprovider displaying
        for i in allads:
            b=jsondec.decode(i['ad_pro'])
            new1.append(b)
            for l in new1:    
                a=(l.get("sales_manager"))
                if id == a:
                    sm_adss.append(i)
                    ads_count.append(i)
                    break
        for item in sm_adss:
            if item['commission']!=None:
                item['amount'] = int(item['commission']) * 10
            
        totalcommission=sum(int(item.get("amount",0))for item in sm_adss)
            
        # client displaying
        
        for i in all_client_data:
            uid=jsondec.decode(i.get("sales_id"))
            id_value = uid["uid"]
            if id_value==id:
                c.append(i)
        
        totalclient=len(c)+len(sm_ads)
        
        # adtype displaying
        wordtype=[]
        for k in ads_count:
            adtype=(k.get("ad_type"))
            wordtype.append(adtype)
        wordcount=Counter(wordtype)
        result=[{"word":word , "count":count } for word,count in wordcount.items()]
        # sales_incentives
        target=2
        incent_amount=0
        incentive=[]

        for i in all_client_data:
            if i.get("active_status") == True:
                incentive.append(i)
            if len(incentive) >= target:
                len(incentive) % target == 0
                incent_amount=incent_amount + 100
                incentive.clear()
        # print(incent_amount)
        
                        
        context={
            'key':mydata,
            'current_path':request.get_full_path(),
            'all_profile_finder':all_profile_finder[::-1],
            'all_client_data':c[::-1],
            'access':access,
            'ads_data':sm_ads[::-1],
            'totalcoin':totalcoin,
            'totalclient':totalclient,
            'result':result,
            'total_commission':totalcommission,
            'incent_amount':incent_amount,
        }
    return render(request,"sm_salesdashboard.html",context)


def profile(request,id):
    value = request.COOKIES.get('sales_manager')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/sales_manager/signin/")
    try:
    
        mydata = requests.get(f"http://127.0.0.1:3000/sm_my_data/{id}").json()[0]
        print(mydata)
        access=""
        education  = jsondec.decode(mydata['level_education'])
        study = jsondec.decode(mydata['field_study'])
        allads=requests.get("http://127.0.0.1:3000/adprovider_ads/").json()
        # addistributor
        alldis_ads=requests.get("http://127.0.0.1:3000/addistributor_ads/").json()
        sm_ads=[]
        sm_adss=[]
        new1=[]
        new=[]
        for j in alldis_ads:
            addis=jsondec.decode(j["ad_dis"])
            new.append(addis)
            for adis in new:
                d=(adis.get("sales_manager"))
                if id == d:
                    sm_ads.append(j)
                    break

        totalcoin = 0
        for item in sm_ads:
            if item['coin'] != None:
                totalcoin+=int(item['coin'])

        for i in allads:
            # print(i)
            b=jsondec.decode(i['ad_pro'])
            # print(type(b))
            new1.append(b)
            for l in new1:    
                a=(l.get("sales_manager"))
                if id == a:
                    sm_adss.append(i)
                    break
        for item in sm_adss:
            if item["commission"]!=None:
                item['amount'] = int(item['commission']) * 10
            
        totalcommission=sum(int(item.get("amount",0))for item in sm_adss)
        
        context={
            'key':mydata,
            'current_path':request.get_full_path(),
            'access':access,
            'totalcoin':totalcoin,
            'totalcommission':totalcommission,
             'education':education,
        'study':study,
        }
        return render(request,"sm_sales_profile.html",context)
    except:
        mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]
        print(mydata)
        access = mydata['access_Privileges']
        
        allads=requests.get("http://127.0.0.1:3000/adprovider_ads/").json()
        # addistributor
        alldis_ads=requests.get("http://127.0.0.1:3000/addistributor_ads/").json()
        sm_ads=[]
        sm_adss=[]
        new1=[]
        new=[]
        for j in alldis_ads:
            addis=jsondec.decode(j["ad_dis"])
            new.append(addis)
            for adis in new:
                d=(adis.get("sales_manager"))
                if id == d:
                    sm_ads.append(j)
                    break

        totalcoin = 0
        for item in sm_ads:
            if item['coin'] != None:
                totalcoin+=int(item['coin'])

        for i in allads:
            # print(i)
            b=jsondec.decode(i['ad_pro'])
            # print(type(b))
            new1.append(b)
            for l in new1:    
                a=(l.get("sales_manager"))
                if id == a:
                    sm_adss.append(i)
                    break
        for item in sm_adss:
            if item["commission"]!=None:
                item['amount'] = int(item['commission']) * 10
            
        totalcommission=sum(int(item.get("amount",0))for item in sm_adss)
        
        context={
            'key':mydata,
            'current_path':request.get_full_path(),
            'access':access,
            'totalcoin':totalcoin,
            'totalcommission':totalcommission,
        }
        return render(request,"sm_sales_profile.html",context)
def edit_profile(request,id):
        value = request.COOKIES.get('sales_manager')
        if value != None:
            print(value)
            # return redirect("/Dashboard_profile_finder/{value}")
        else:
            return redirect("/sales_manager/signin/")
        try:
            mydata = requests.get(f"http://127.0.0.1:3000/sm_my_data/{id}").json()[0] 
           
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
                        'current_path':request.get_full_path(),}
            
            if request.method=="POST":
                print(request.POST)
                response = requests.post(f"http://127.0.0.1:3000/sm_edit_data/{id}", data = request.POST,files=request.FILES)
                print(response)
                print(response.status_code)
                print(response.text)
                return render(request,"sm_sales_profile.html",context)
            return render(request,"sm_editprofile.html",context)
        
            
        except:
            return render(request,"sm_editprofile.html")

def account_balance(request,id):
    value = request.COOKIES.get('sales_manager')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/sales_manager/signin/")
    try:
        mydata = requests.get(f"http://127.0.0.1:3000/sm_my_data/{id}").json()[0]
        allads=requests.get("http://127.0.0.1:3000/adprovider_ads/").json()
        new1=[]
        sm_ads=[]
        for i in allads:
            # print(i)
            b=jsondec.decode(i['ad_pro'])
            # print(type(b))
            new1.append(b)
            for l in new1:    
                a=(l.get("sales_manager"))
                if id == a:
                    sm_ads.append(i)
                    break
        for item in sm_ads:
            if item["commission"]!=None:
                item['amount'] = int(item['commission']) * 10
        
        totalcommission=sum(int(item.get("amount",0))for item in sm_ads)
        print(totalcommission)    
        context={
            'key':mydata,
            'current_path':request.get_full_path(),
            'all_commissions':sm_ads[::-1],
            'total_commission':totalcommission,
            
        }
        return render(request,"sm_accountbalance.html",context)
    except:
        mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]
        print(mydata)
        access = mydata['access_Privileges']
        allads=requests.get("http://127.0.0.1:3000/adprovider_ads/").json()
        new1=[]
        sm_ads=[]
        for i in allads:
            # print(i)
            b=jsondec.decode(i['ad_pro'])
            # print(type(b))
            new1.append(b)
            for l in new1:    
                a=(l.get("sales_manager"))
                if id == a:
                    sm_ads.append(i)
                    break
        for item in sm_ads:
            if item["commission"]!=None:
                item['amount'] = int(item['commission']) * 10
        
        totalcommission=sum(int(item.get("amount",0))for item in sm_ads)
        print(totalcommission)    
        context={
            'key':mydata,
            'current_path':request.get_full_path(),
            'all_commissions':sm_ads[::-1],
            'total_commission':totalcommission,
            'access':access,
            
        }
        return render(request,"sm_accountbalance.html",context)



def coin_details(request,id):
    value = request.COOKIES.get('sales_manager')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/sales_manager/signin/")
    try:
        new=[]
        mydata = requests.get(f"http://127.0.0.1:3000/sm_my_data/{id}").json()[0]
        # adprovider
        allads=requests.get("http://127.0.0.1:3000/adprovider_ads/").json()
        # addistributor
        alldis_ads=requests.get("http://127.0.0.1:3000/addistributor_ads/").json()
        sm_ads=[]
        # new1=[]
        new=[]
        for j in alldis_ads:
            addis=jsondec.decode(j["ad_dis"])
            new.append(addis)
            for adis in new:
                d=(adis.get("sales_manager"))
                if id == d:
                    sm_ads.append(j)
                    break


        totalcoin=0
        for item in sm_ads:
            if item['coin'] != None:
                totalcoin+=int(item['coin'])
                

        print(totalcoin)
        context={
            'key':mydata,
            'current_path':request.get_full_path(),
            'ad_data':sm_ads[::-1],
            'totalcoin':totalcoin, 
        }

        return render(request,"sm_coindetails.html",context)
    except:
        new=[]
        mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]
        print(mydata)
        access = mydata['access_Privileges']
        # adprovider
        allads=requests.get("http://127.0.0.1:3000/adprovider_ads/").json()
        # addistributor
        alldis_ads=requests.get("http://127.0.0.1:3000/addistributor_ads/").json()
        sm_ads=[]
        # new1=[]
        new=[]
        for j in alldis_ads:
            addis=jsondec.decode(j["ad_dis"])
            new.append(addis)
            for adis in new:
                d=(adis.get("sales_manager"))
                if id == d:
                    sm_ads.append(j)
                    break


        totalcoin=0
        for item in sm_ads:
            if item['coin'] != None:
                totalcoin+=int(item['coin'])
                

        print(totalcoin)
        context={
            'key':mydata,
            'current_path':request.get_full_path(),
            'ad_data':sm_ads[::-1],
            'totalcoin':totalcoin,
            'access':access, 
        }

        return render(request,"sm_coindetails.html",context)

def hand_list(request,id):
    value = request.COOKIES.get('sales_manager')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/sales_manager/signin/")
    try:
        error = ""
        mydata = requests.get(f"http://127.0.0.1:3000/sm_my_data/{id}").json()[0]
        my_user = requests.get(f"http://127.0.0.1:3000/sm_my_users_data/{id}").json()
        print(my_user)
        access = ""
        idd = id
    except:
        error = ""
        mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]  
        print(mydata)
        my_user = requests.get(f"http://127.0.0.1:3000/sm_my_users_data/{mydata['aid']}").json()
        print(my_user)
        access = mydata['access_Privileges']
        idd = mydata['aid']
    jsondec = json.decoder.JSONDecoder()

    c=[]
    all_client_data= requests.get("http://127.0.0.1:3000/all_client_data/").json()

    for i in all_client_data:
        uid=jsondec.decode(i.get("sales_id"))
        id_value = uid["uid"]
        if id_value==idd:
            c.append(i)
    

    if request.method == "POST":
        
        if 'view_client' in request.POST:
            print(request.POST)
            global uid_client
            uid_client = request.POST['view_client']
            return redirect(f"/sales_manager/sm_client_details/{id}")
        
        elif 'active' in request.POST:
            a=request.POST["active"]
            print(a)
            active_response = requests.post(f"http://127.0.0.1:3000/active_satus/{a}", data=request.POST)
            response = requests.post(f"http://127.0.0.1:3000/client_otp_active/{idd}", data=request.POST )
            print(response)

        elif 'uid' in request.POST:
            print(request.POST)
            filter={
                'f_uid':request.POST['uid'].strip(),
                'f_client_name':request.POST['client_name'].strip().lower(),
                'f_email':request.POST['email'].strip().lower(),
                'f_phone_number':request.POST['phone_number'].strip(),
                'f_client_location':request.POST['client_location'].strip().lower(),
                'f_status':request.POST['active_status'].strip() 
            }
            print(filter)
            
            p = set()
            for x in c:
                
                if (filter['f_uid'] == x['uid'] or not filter['f_uid']) and \
                (filter['f_client_name'] == x['client_name'].lower() or not filter['f_client_name']) and \
                (filter['f_email'] == x['email'].lower() or not filter['f_email']) and \
                (filter['f_phone_number'] == x['phone_number'] or not filter['f_phone_number']) and \
                (filter['f_client_location'] == x['client_location'].lower() or not filter['f_client_location']) and \
                (filter['f_status'] == str(x['active_status']) or not filter['f_status']):
                    p.add(x['uid'])

            c= [ad for ad in all_client_data if ad['uid'] in p]
                 
            print(p)

        else:     
            print(request.POST)
            print(request.FILES)
            data={
                "sales_id":idd,
                'client_type':request.POST['client_type'],
                'client_name':request.POST['client_name'],
                'client_location':request.POST['client_location'],
                'category':request.POST['category'],
                'google_map':request.POST['google_map'],
                'phone_number':request.POST['phone_number'],
                'email':request.POST['email'],
                'picture':request.FILES

            }
        
            response = requests.post(f"http://127.0.0.1:3000/add_client_data/{idd}", data =data,files=request.FILES)

            print(response.status_code)
            print(response.text)
            uidd = (response.text[1:-1])
            if response.status_code == 200:
                return redirect(f"/sales_manager/sm_hand_list/{id}")
            
            else:
                pass
    context={
        'key':mydata,
        'current_path':request.get_full_path(),
        'all_client_data':c[::-1],
        'access':access,
        
        }

    return render(request,"sm_hand_list.html",context)


def otp_client(request,id):
    value = request.COOKIES.get('sales_manager')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/sales_manager/signin/")
    try:
        error = ""
        mydata = requests.get(f"http://127.0.0.1:3000/sm_my_data/{id}").json()[0]
        my_user = requests.get(f"http://127.0.0.1:3000/sm_my_users_data/{id}").json()
        print(my_user)
        access = ""
        idd = id
    except:
        error = ""
        mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]  
        print(mydata)
        my_user = requests.get(f"http://127.0.0.1:3000/sm_my_users_data/{mydata['aid']}").json()
        print(my_user)
        access = mydata['access_Privileges']
        idd = mydata['aid']
    context = {'invalid':"invalid"}
    new=[]
    if request.method == "POST":
        new.append(request.POST["otp1"])
        new.append(request.POST["otp2"])
        new.append(request.POST["otp3"])
        new.append(request.POST["otp4"])
        new.append(request.POST["otp5"])
        new.append(request.POST["otp6"])

        data = {
            'user_otp':int(''.join(new).strip())
           
        }
        print(data)
        response = requests.post(f"http://127.0.0.1:3000/client_otp/{idd}", data=data)

       
        print(response)
        print(response.status_code)
        print(data['user_otp'])
        print(response.text)
        uidd = (response.text[1:-1])
        
        if response.status_code == 200:
        # if get["otp"] == data['user_otp']:
            # return redirect(f"/profileidcard/{uidd}")
            return redirect(f"/sales_manager/sm_hand_list/{uidd}")

        else:
            invalid = "Invalid OTP"
            context = {'invalid':invalid}
    return render(request,"sm_hand_list.html",context)

#  sales_client_ads
def ads_list(request,id):
    value = request.COOKIES.get('sales_manager')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/sales_manager/signin/")
    try:
        error = ""
        mydata = requests.get(f"http://127.0.0.1:3000/sm_my_data/{id}").json()[0]
        my_user = requests.get(f"http://127.0.0.1:3000/sm_my_users_data/{id}").json()
        print(my_user)
        access = ""
        idd = id
    except:
        error = ""
        mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]  
        print(mydata)
        my_user = requests.get(f"http://127.0.0.1:3000/sm_my_users_data/{mydata['aid']}").json()
        print(my_user)
        access = mydata['access_Privileges']
        idd = mydata['aid']
    jsondec = json.decoder.JSONDecoder()
    c=[]
    client_activities=requests.get("http://127.0.0.1:3000/all_activities/").json()
    all_client_data= requests.get("http://127.0.0.1:3000/all_client_data/").json()

    for i in all_client_data:
        uid=jsondec.decode(i.get("sales_id"))
        id_value = uid["uid"]
        if id_value==idd:
            c.append(i)

    context={
        'key':mydata,
        'current_path':request.get_full_path(),
        'all_client_data':c[::-1],
        'client_activities':client_activities[::-1], 
        }
    if request.method == "POST":
        if 'semail' in request.POST:
            print(request.POST['semail'])

            response=requests.post(f"http://127.0.0.1:3000/sendmail/{request.POST['semail']}",data=request.POST)

        
        else:        
            print(request.POST)
            data={
                
                'types_of_activities':request.POST['types_of_activities'],
                'date':request.POST['date'],
                'time':request.POST['time'],
                'notes':request.POST['notes'],
                # 'status':request.POST['status'],       
                
            }
            
            response = requests.post(f"http://127.0.0.1:3000/add_client_activities/{request.POST['client_name']}", data =data)
            print(response.status_code)
            print(response.text)
            return redirect(f"/sales_manager/sm_ads_list/{id}")
    return render(request,"sm_ads_list.html",context)

def sm_client_details(request,id):
    value = request.COOKIES.get('sales_manager')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/sales_manager/signin/")
    try:
        error = ""
        mydata = requests.get(f"http://127.0.0.1:3000/sm_my_data/{id}").json()[0]
        my_user = requests.get(f"http://127.0.0.1:3000/sm_my_users_data/{id}").json()
        print(my_user)
        access = ""
        idd = id
    except:
        error = ""
        mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]  
        print(mydata)
        my_user = requests.get(f"http://127.0.0.1:3000/sm_my_users_data/{mydata['aid']}").json()
        print(my_user)
        access = mydata['access_Privileges']
        idd = mydata['aid']
    hand_list(request,id)
    print(uid_client)
    client_data=requests.get(f"http://127.0.0.1:3000/view_client_id/{uid_client}").json()
    print(client_data)
    context={

        'key':mydata,
        'current_path':request.get_full_path(),
        'client_data':client_data,
        
    }
    return render(request,"sm_client_details.html",context)

# ad_provider ads

def ad_details(request,id):
    value = request.COOKIES.get('sales_manager')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/sales_manager/signin/")
    try:
        error = ""
        mydata = requests.get(f"http://127.0.0.1:3000/sm_my_data/{id}").json()[0]
        my_user = requests.get(f"http://127.0.0.1:3000/sm_my_users_data/{id}").json()
        print(my_user)
        access = ""
        idd = id
    except:
        error = ""
        mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]  
        print(mydata)
        my_user = requests.get(f"http://127.0.0.1:3000/sm_my_users_data/{mydata['aid']}").json()
        print(my_user)
        access = mydata['access_Privileges']
        idd = mydata['aid']
    ads=[]
    ad_pro_ads(request,id) 
    viewid=requests.get(f"http://127.0.0.1:3000/view_adpro_id/{uid_view}").json()
    ads_data=requests.get("http://127.0.0.1:3000/adprovider_ads/").json()
    
   
    ad_pro_id=(viewid.get("uid"))
    for i in ads_data:
        a= jsondec.decode(i.get("ad_pro"))
        ads_id=a["uid"]
        if ads_id == ad_pro_id:
            ads.append(i)

    if 'ad_pro_list' in request.POST:
        print("ad_pro_list",request.POST)
        global adprolist_id
        adprolist_id = request.POST['ad_pro_list']
        return redirect(f"/sales_manager/sm_edit_adproDetail/{id}")
    
    context={
        'key':mydata,
        'current_path':request.get_full_path(),
        'viewid':viewid,
        'ad_data':ads,    
    }
    return render(request,"sm_ad_details.html",context)

# adprodetail
def edit_adpro_details(request,id):
    value = request.COOKIES.get('sales_manager')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/sales_manager/signin/")
    try:
        error = ""
        mydata = requests.get(f"http://127.0.0.1:3000/sm_my_data/{id}").json()[0]
        my_user = requests.get(f"http://127.0.0.1:3000/sm_my_users_data/{id}").json()
        print(my_user)
        access = ""
        idd = id
    except:
        error = ""
        mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]  
        print(mydata)
        my_user = requests.get(f"http://127.0.0.1:3000/sm_my_users_data/{mydata['aid']}").json()
        print(my_user)
        access = mydata['access_Privileges']
        idd = mydata['aid']
    ad_details(request,id)
    adspro=requests.get(f"http://127.0.0.1:3000/addpro_ads_id/{adprolist_id}").json()

    
    if 'approve' in request.POST:
        # print(request.POST['approve'])
        response=requests.post(f"http://127.0.0.1:3000/adspro_status_active/{request.POST['approve']}",data=request.POST)
        return redirect(f"/sales_manager/sm_ad_details/{id}")
    if "adpro_reject" in request.POST:
        print(request.POST['adpro_reject'])
        response=requests.post(f"http://127.0.0.1:3000/adspro_status_reject/{request.POST['adpro_reject']}",data=request.POST)
        return redirect(f"/sales_manager/sm_ad_details/{id}")


    context={
        'key':mydata,
        'current_path':request.get_full_path(),
        'ad_data':adspro,
        'access':access,
    }
    return render(request,"sm_edit_adproDetail.html",context)

# ad distributor ads
def ad_dis_details(request,id):
    value = request.COOKIES.get('sales_manager')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/sales_manager/signin/")
    try:
        error = ""
        mydata = requests.get(f"http://127.0.0.1:3000/sm_my_data/{id}").json()[0]
        my_user = requests.get(f"http://127.0.0.1:3000/sm_my_users_data/{id}").json()
        print(my_user)
        access = ""
        idd = id
    except:
        error = ""
        mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]  
        print(mydata)
        my_user = requests.get(f"http://127.0.0.1:3000/sm_my_users_data/{mydata['aid']}").json()
        print(my_user)
        access = mydata['access_Privileges']
        idd = mydata['aid']
    ads=[]
    ad_pro_ads(request,id)
    # print(uid_dis)
    view_id=requests.get(f"http://127.0.0.1:3000/view_addis_id/{uid_dis}").json()
    ad_dis_ads=requests.get("http://127.0.0.1:3000/addistributor_ads/").json()
    ad_dis_id=(view_id.get("uid"))

    if 'ad_list' in request.POST:
        print("ad_list",request.POST)
        global addlist_id
        addlist_id = request.POST['ad_list']
        return redirect(f"/sales_manager/sm_edit_adDetail/{id}")

    for i in ad_dis_ads:
        a= jsondec.decode(i.get("ad_dis"))
        ads_id=a["uid"]
        if ads_id == ad_dis_id:
            ads.append(i)
  
    context={
    'key':mydata,
    'current_path':request.get_full_path(),
    'view_id':view_id,
    'ad_data':ads,
    }
    return render(request,"sm_ad_dis_details.html",context)


# ad dis detail
def edit_ad_details(request,id):
    value = request.COOKIES.get('sales_manager')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/sales_manager/signin/")
    try:
        error = ""
        mydata = requests.get(f"http://127.0.0.1:3000/sm_my_data/{id}").json()[0]
        my_user = requests.get(f"http://127.0.0.1:3000/sm_my_users_data/{id}").json()
        print(my_user)
        access = ""
        idd = id
    except:
        error = ""
        mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]  
        print(mydata)
        my_user = requests.get(f"http://127.0.0.1:3000/sm_my_users_data/{mydata['aid']}").json()
        print(my_user)
        access = mydata['access_Privileges']
        idd = mydata['aid']
    ad_dis_details(request,id)
    ads=requests.get(f"http://127.0.0.1:3000/addis_ads_id/{addlist_id}").json()

    if 'approve_dis' in request.POST:
        print(request.POST['approve_dis'])
        response=requests.post(f"http://127.0.0.1:3000/adsdis_status_active/{request.POST['approve_dis']}",data=request.POST)
        return redirect(f"/sales_manager/sm_ad_dis_details/{id}")
    if 'addis_reject' in request.POST:
        # print(request.POST['addis_reject'])
        response=requests.post(f"http://127.0.0.1:3000/adsdis_status_reject/{request.POST['addis_reject']}",data=request.POST)
        print(response)
        return redirect(f"/sales_manager/sm_ad_dis_details/{id}")
        
    context={
        'key':mydata,
        'current_path':request.get_full_path(),
        'ad_data':ads,
        
    }
    return render(request,"sm_edit_adDetail.html",context)

def users(request,id):
    value = request.COOKIES.get('sales_manager')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/sales_manager/signin/")
    try:
        new=[]
        error = ""
        mydata = requests.get(f"http://127.0.0.1:3000/sm_my_data/{id}").json()[0]
        my_user = requests.get(f"http://127.0.0.1:3000/sm_my_users_data/{id}").json()
        print(my_user)
        access = ""
        for x in my_user:
            new.append(x)
    except:
        new=[]
        error = ""
        mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]  
        print(mydata)
        my_user = requests.get(f"http://127.0.0.1:3000/sm_my_users_data/{mydata['aid']}").json()
        print(my_user)
        access = mydata['access_Privileges']
        for x in my_user:
            new.append(x)

    if request.method== "POST":
        print(request.POST)
        if "delete" in request.POST:
            response = requests.post(f"http://127.0.0.1:3000/sm_add_user/{id}",data=request.POST)
            print(response.text)
            print(response.status_code)
            return redirect(f"/sales_manager/sm_users/{id}")

        elif "edit" in request.POST:
            print(request.POST)
            global user_uid
            user_uid = request.POST['edit']
            return redirect(f"/sales_manager/sm_user_edit/{id}")
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
            response = requests.post(f"http://127.0.0.1:3000/sm_add_user/{id}",data=data)
            # print(response.text)
            # print(response.status_code)
            if response.status_code == 200:
                return redirect(f"http://51.20.61.70:8001/sales_manager/sm_users/{id}")
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
    return render(request,"sm_users.html",context)


def add_users(request,id):
    value = request.COOKIES.get('sales_manager')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/sales_manager/signin/")
    error=""
    try:
        error = ""
        mydata = requests.get(f"http://127.0.0.1:3000/sm_my_data/{id}").json()[0]
        my_user = requests.get(f"http://127.0.0.1:3000/sm_my_users_data/{id}").json()
        print(my_user)
        access = ""
        idd = id
    except:
        error = ""
        mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]  
        print(mydata)
        my_user = requests.get(f"http://127.0.0.1:3000/sm_my_users_data/{mydata['aid']}").json()
        print(my_user)
        access = mydata['access_Privileges']
        idd = mydata['aid']

    try:
        mydata = requests.get(f"http://127.0.0.1:3000/sm_my_data/{id}").json()[0]
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
                                'work':"sales_manager",
                                'creator':id,
                                    # 'location':request.POST['location']
                }
            print(data)
            response = requests.post(f"http://127.0.0.1:3000/sm_add_user/{id}",data=data)
            print(response.text)
            print(response.status_code)
            if response.status_code == 200:
                return redirect(f"http://127.0.0.1:8001/sales_manager/sm_users/{id}")
            elif response.status_code == 203:
                print("user already exist")
                error = "User Already Exixts"
        context={
            'key':mydata,
            'current_path':request.get_full_path(),
            'error':error,
            'access':access   

        }

        return render(request,"sm_addusers.html",context)
    except:
        mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]
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
                                'work':"sales_manager",
                                'creator':mydata['aid']
                                    # 'location':request.POST['location']
                }
            print(data)
            response = requests.post(f"http://127.0.0.1:3000/sm_add_user/{id}",data=data)
            print(response.text)
            print(response.status_code)
            if response.status_code == 200:
                return redirect(f"http://127.0.0.1:3000/sales_manager/sm_users/{id}")
            elif response.status_code == 203:
                print("user already exist")
                error = "User Already Exixts"

        context={
            'key':mydata,
            'current_path':request.get_full_path(),
            'error':error,   
            'access' :access
        }

        return render(request,"sm_addusers.html",context)

def sm_user_edit(request,id):
    value = request.COOKIES.get('sales_manager')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/sales_manager/signin/")
    
    users(request,id)
    print(user_uid)
    error=""
    try:
        mydata = requests.get(f"http://127.0.0.1:3000/sm_my_data/{id}").json()[0]
        sm_my_users_data   = requests.get(f"http://127.0.0.1:3000/single_users_data/{user_uid}").json()[0]
        print(sm_my_users_data)
    except:
        mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]  
        print(mydata['aid'])
        sm_my_users_data   = requests.get(f"http://127.0.0.1:3000/single_users_data/{user_uid}").json()[0]

        # my_user = requests.get(f"http://127.0.0.1:3000/sm_my_users_data/{mydata['aid']}").json()
        # print(my_user)
       
        
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
           response = requests.post(f"http://127.0.0.1:3000/sm_add_user/{id}",data=data)
           print(response.text)
           print(response.status_code)
           if response.status_code == 200:
              return redirect(f"http://127.0.0.1:3000/sales_manager/sm_users/{id}")
           elif response.status_code == 203:
              print("user already exist")
              error = "User Already Exixts"
    context={
        'key':mydata,
        'current_path':request.get_full_path(),
        'error':error,
        'sm_my_users_data':sm_my_users_data,
        

    }

    return render(request,"sm_user_edit.html",context)


def setting(request,id):
    value = request.COOKIES.get('sales_manager')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/sales_manager/signin/")

    try:
        error = ""
        mydata = requests.get(f"http://127.0.0.1:3000/sm_my_data/{id}").json()[0]
        my_user = requests.get(f"http://127.0.0.1:3000/sm_my_users_data/{id}").json()
        print(my_user)
        access = ""
        idd = id
    except:
        error = ""
        mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]  
        print(mydata)
        my_user = requests.get(f"http://127.0.0.1:3000/sm_my_users_data/{mydata['aid']}").json()
        print(my_user)
        access = mydata['access_Privileges']
        idd = mydata['aid']
    mydata = requests.get(f"http://127.0.0.1:3000/sm_my_data/{id}").json()[0]  
   
    if request.method=="POST":
        print(request.POST)
        if 'pass_reset' in request.POST:
            
            a=request.POST["pass_reset"]
            print(a)
       
            response = requests.post(f"http://127.0.0.1:3000/password_reset/{id}",data=request.POST )
        else:
            # print(request.POST)
            response = requests.post(f"http://127.0.0.1:3000/sm_email_update/{id}", data = request.POST)
            print(response)
            print(response.status_code)
            print(response.text)
            return render(request,"sm_accountsetting.html",context)
        
    context={
        'key':mydata,
        'current_path':request.get_full_path(),
        'access':access
        }
    return render(request,"sm_accountsetting.html",context)


def password_reset(request,id):
#    value = request.COOKIES.get('sales_manager')
 #   if value != None:
  #      print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
   # else:
    #    return redirect("/sales_manager/signin/")
    print(id)
    if request.method=="POST":
        print(request.POST)
        if 'pass_reset' in request.POST:
            
            a=request.POST["pass_reset"]
            print(a)
        if request.POST['password'] == request.POST['confirm_password']:

            response = requests.post(f"http://127.0.0.1:3000/pass_sales_update/{id}",data=request.POST )
            messages.info(request,"Password Successfully Updated")
        else:
            messages.info(request,"Password Incorrect")
    return render(request,"password_reset.html")



def ad_pro_ads(request,id):
    value = request.COOKIES.get('sales_manager')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/sales_manager/signin/")
    try:
        error = ""
        mydata = requests.get(f"http://127.0.0.1:3000/sm_my_data/{id}").json()[0]
        my_user = requests.get(f"http://127.0.0.1:3000/sm_my_users_data/{id}").json()
        print(my_user)
        access = ""
        idd = id
    except:
        error = ""
        mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]  
        print(mydata)
        my_user = requests.get(f"http://127.0.0.1:3000/sm_my_users_data/{mydata['aid']}").json()
        print(my_user)
        access = mydata['access_Privileges']
        idd = mydata['aid']
    all_data=requests.get("http://127.0.0.1:3000/ad_pro_list/").json()
    ad_data=requests.get("http://127.0.0.1:3000/ad_dis_list/").json()
    # print(all_data)
    new=[]
    clients=[]
    for i in all_data:
        a=(i.get('sales_manager'))
        if idd == a: 
            new.append(i)
            clients.append(i)

    for i in ad_data:
        d=(i.get('sales_manager'))
        if idd == d:
            new.append(i)
            clients.append(i)
    
    if request.method == "POST":
        if 'view' in request.POST:
            # print(request.POST)
            global uid_view
            uid_view = request.POST['view']
            return redirect(f"/sales_manager/sm_ad_details/{id}")
        if 'view_dis' in request.POST:
            # print(request.POST)
            global uid_dis
            uid_dis=request.POST['view_dis']
            return redirect(f"/sales_manager/sm_ad_dis_details/{id}")
        
        elif "uid" in request.POST:
            filter = {
                'f_u_id': request.POST['uid'],
                'f_u_name': request.POST['client_name'].lower(),
                'f_u_email': request.POST['email'].lower(),
                'f_u_phone': request.POST['phone_number'],
                'f_google_map':request.POST['google_map'],
                
                }

            p = set()

            for x in new:
                
                if (filter['f_u_id'] == x['uid'] or not filter['f_u_id']) and \
                (filter['f_u_name'] == x['first_name'].lower() or not filter['f_u_name']) and \
                (filter['f_u_email'] == x['email'].lower() or not filter['f_u_email']) and \
                (filter['f_u_phone'] == x['mobile'] or not filter['f_u_phone']) and \
                (filter['f_google_map'] == x['personal_address'] or not filter['f_google_map']):
                    p.add(x['uid'])

            new = [ad for ad in clients if ad['uid'] in p]
            print(new)
        
    context={
        'key':mydata,
        'current_path':request.get_full_path(),
        'all_data':new[::-1], 
        'access':access     
   
    }
    return render(request,"sm_all_ads_list.html",context)

# forget password

def sales_forget_password(request):
#    value = request.COOKIES.get('sales_manager')
 #   if value != None:
  #      print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
   # else:
    #    return redirect("/sales_manager/signin/")
    error=""
    if request.method == "POST":
        
        print(request.POST)
        response = requests.post("http://127.0.0.1:3000/sales_forget_password/",data=request.POST)
        print(response)
        print(response.status_code)
        print(type(jsondec.decode(response.text)))
        print(jsondec.decode(response.text))
        uidd = jsondec.decode(response.text)
        
        if response.status_code == 200:
            return redirect(f"/sales_forgetpassword_otpp/{uidd}")
        elif response.status_code == 403:
            error = "User Doesn't Exist"

    context = {'error':error}
    return render(request,"sales_email.html",context)
    

def sales_forgetpassword_otp(request,id):
 #   value = request.COOKIES.get('sales_manager')
  #  if value != None:
   #     print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
   # else:
    #    return redirect("/sales_manager/signin/")
    mydata = requests.get(f"http://127.0.0.1:3000/sm_my_data/{id}").json()[0]
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
        response = requests.post(f"http://127.0.0.1:3000/sales_forget_password_otp/{id}", data=data)
       
        print(response)
        print(response.status_code)
        print(data['user_otp1'])
        print(response.text)
        uidd = (response.text[1:-1])
        
        if response.status_code == 200:
            return redirect(f"/sales_forgetpassword_resett/{uidd}")
        else:
            invalid = "Invalid OTP"
            context = {'invalid':invalid}
    return render(request,"sm_otpcheck.html",context)


def sales_forgetpassword_reset(request,id):
#    value = request.COOKIES.get('sales_manager')
 #   if value != None:
  #      print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
   # else:
    #    return redirect("/sales_manager/signin/")
    error=""
    mydata = requests.get(f"http://127.0.0.1:3000/sm_my_data/{id}").json()[0]
    print(id)
    if request.method=="POST":
        print(request.POST)
       # if request.POST['password'] == request.POST['confirm_password']:
        if request.POST['password']:
            response = requests.post(f"http://127.0.0.1:3000/pass_sales_update/{id}",data=request.POST )
            print(response)
            return redirect(f"/sales_manager/signin/")

        else:
            print(response)
            error="password mismatch"
    context = {'invalid':"invalid",
                'key':mydata,
                'error':error}
    return render(request,"sales_forgetpassword.html",context)




def verification_fee(request,id):
    value = request.COOKIES.get('sales_manager')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/sales_manager/signin/")
    if request.method == "POST":
            return redirect(f"/sales_manager/sm_salesdashboard/{id}")
    return render(request,"sm_verification_fee.html")


