from django.shortcuts import render,redirect
from django.contrib.auth import logout
from django.urls import reverse
from django.http import JsonResponse,HttpResponse
from django.contrib import messages
import requests
import json
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

jsondec = json.decoder.JSONDecoder()
global access_Privileges
access_Privileges = ""
# Create your views here.
def dashboard(request):
    return render(request,"dashboard.html")

def signup(request):
    error = ""
    if request.method == "POST":
        if request.POST['password'] == request.POST['confirm_password']:
                # response = requests.post('http://54.159.186.219:8000/signup/',data=request.POST)
                response = requests.post("http://127.0.0.1:3000/pm_signup/",data=request.POST)
                print(response.status_code)
                print(response.text)
                uidd = (response.text[1:-1])
                print(uidd)
                if response.status_code == 200:
                   return redirect(f"/profile_manager/otp/{uidd}")
                elif response.status_code == 302:
                    error = "User Already Exist"
        else:
            print("password doesn't match")
    context = {'error':error}
    return render(request,"signup.html",context)

def signin(request):
    value = request.COOKIES.get('profilemanager')
    print(value)
    # a= requests.get("http://127.0.0.1:3000/pm_alldata/").json()
    # print("YBJ2FMOZN2P" in a)
    # current_path =  request.get_full_path()
    # print(current_path)
    # form1 = ProfileSigninForm()
    error = ""
    if request.method == "POST":
        print(request.POST)
        # response = requests.post("http://54.159.186.219:8000/signin/",data=request.POST)
        response = requests.post("http://127.0.0.1:3000/pm_signin/",data=request.POST)
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
            response = redirect(f"/profile_manager/admin_dashboard/{uid}")
            response.set_cookie("profilemanager",uid)
            return response
            # return redirect(f"/profile_manager/admin_dashboard/{uid}")
        else:
          error = "YOUR EMAILID OR PASSWORD IS INCORRECT"
    context = {'error':error}
    return render(request,"signin.html",context)


def logout_view(request):
    print("logout")
    value = request.COOKIES.get('profilemanager')
    print(value)
    response = redirect("/profile_manager/signin/")
    # response = HttpResponse("delete cookie")
    response.delete_cookie("profilemanager")
    return response

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
        response = requests.post(f"http://127.0.0.1:3000/pm_otp/{id}", data=data)

       
        print(response)
        print(response.status_code)
        print(data['user_otp'])
        print(response.text)
        uidd = (response.text[1:-1])
        
        if response.status_code == 200:
        # if get["otp"] == data['user_otp']:
            # return redirect(f"/profileidcard/{uidd}")
            return redirect(f"/profile_manager/profile_picture/{uidd}")
        else:
            invalid = "Invalid OTP"
            context = {'invalid':invalid}
    return render(request,"otpcheck.html",context)

def profile_picture(request,id):
#    value = request.COOKIES.get('profilemanager')
 #   if value != None:
  #      print(value)
   #     # return redirect("/Dashboard_profile_finder/{value}")
   # else:
    #    return redirect("/profile_manager/signin")
    if request.method == "POST":
        print(request.FILES)
        # response = requests.post(f"http://54.159.186.219:8000/profileidcard/{id}",   files=request.FILES)
        response = requests.post(f"http://127.0.0.1:3000/pm_profile_picture/{id}",   files=request.FILES)
        print(response)
        print(response.status_code)
        print(response.text)
        uidd = (response.text[1:-1])
        if response.status_code == 200:
        # if get["otp"] == data['user_otp']:
            return redirect(f"/profile_manager/upload_acc/{uidd}")
        else:
            return HttpResponse("INVALId")
    return render(request,"profilepicture.html")

def upload_acc(request,id):
   # value = request.COOKIES.get('profilemanager')
    #if value != None:
     #   print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
  #  else:
   #     return redirect("/profile_manager/signin")
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
            # print(request.FILES)
            dictio = dict(request.POST)
            print(dictio)
            # response = requests.post(f"http://54.159.186.219:8000/profileidcard/{id}",   files=request.FILES)
            response = requests.post(f"http://127.0.0.1:3000/pm_complete_account/{id}",   data = dictio,files=request.FILES)
            print(response)
            print(response.status_code)
            print(response.text)
            uidd = (response.text[1:-1])
            if response.status_code == 200:
            # if get["otp"] == data['user_otp']:
                # return redirect(f"/profile_manager/admin_dashboard/{uidd}")
                pass
            else:
               return redirect(f"/profile_manager/upload_acc/{uidd}")
        return render(request,"upload_acc.html",context)
    except:
        context = {'response': "response", 'region': "response",'all':"al",
                    'country': "countryname",'states': "states",'hiring_manager':"hiring_manager"}
        return render(request,"upload_acc.html",context)

def admin_dashboard(request,id):
    value = request.COOKIES.get('profilemanager')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/profile_manager/signin")
    try: 
        mydata = requests.get(f"http://127.0.0.1:3000/pm_my_data/{id}").json()[0]  
        access = ""
        my_profile_finder = requests.get(f"http://127.0.0.1:3000/pm_my_clients/{id}").json()[id]

    except:
        mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]  
        access = mydata['access_Privileges']
        print(mydata['aid'])
        my_profile_finder = requests.get(f"http://127.0.0.1:3000/pm_my_clients/{mydata['aid']}").json()[mydata['aid']]

    finally:
        print(access)  
        print("hi")
        complaints_list = []
        for i in my_profile_finder:
            if i['complaints'] != "empty":
                complaints_list.append(i)
        #approve or Reject
        approve_list = []
        for i in my_profile_finder:
            if i['status'] == "Approve":
                approve_list.append(i)
        context={
            'key':mydata,
            'current_path':request.get_full_path(),
            'all_profile_finder':my_profile_finder,
            'complaints_list':complaints_list,
            'approve_list':approve_list,
            'access_Privileges':"",

        }
    return render(request,"pm_admin_dashboard.html",context)

def profile_account(request,id):
    value = request.COOKIES.get('profilemanager')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/profile_manager/signin")
   
    mydata = requests.get(f"http://127.0.0.1:3000/pm_my_data/{id}").json()[0]
    print(mydata)
    education  = jsondec.decode(mydata['level_education'])
    study = jsondec.decode(mydata['field_study'])
    context={
        'key':mydata,
        'current_path':request.get_full_path(),
        'access_Privileges':access_Privileges,
        'education':education,
        'study':study,
    }

    return render(request,"profile_account.html",context)

def edit_acc(request,id):
    value = request.COOKIES.get('profilemanager')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/profile_manager/signin")
    try:
        mydata = requests.get(f"http://127.0.0.1:3000/pm_my_data/{id}").json()[0] 
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
    
        context = {'response': response, 'region': response,'all':al,
                    'country': countryname,'states': states,'key':mydata,
                    'current_path':request.get_full_path()}
        
        if request.method=="POST":
            print(request.POST)
            response = requests.post(f"http://127.0.0.1:3000/pm_edit_account/{id}", data = request.POST,files=request.FILES)
            print(response)
            print(response.status_code)
            print(response.text)
    
        return render(request,"edit_acc.html",context)
    except:
        return render(request,"edit_acc.html")


def acc_balance(request,id):
    value = request.COOKIES.get('profilemanager')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/profile_manager/signin")
    mydata = requests.get(f"http://127.0.0.1:3000/pm_my_data/{id}").json()[0]  
    context={
        'key':mydata,
        'current_path':request.get_full_path()
    }

    return render(request,"acc_balance.html",context)

def profile_finders(request,id):
    value = request.COOKIES.get('profilemanager')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/profile_manager/signin")
    try: 
        mydata = requests.get(f"http://127.0.0.1:3000/pm_my_data/{id}").json()[0]  
        access = ""
        my_profile_finder = requests.get(f"http://127.0.0.1:3000/pm_my_clients/{id}").json()[id]

    except:
        mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]  
        access = mydata['access_Privileges']
        print(mydata['aid'])
        my_profile_finder = requests.get(f"http://127.0.0.1:3000/pm_my_clients/{mydata['aid']}").json()[mydata['aid']]
    finally:
        context={
            'key':mydata,
            'current_path':request.get_full_path(),
            'all_profile_finder':my_profile_finder,
            'access_Privileges':access,
        }
        if request.method == "POST":
            if 'uid' in request.POST:
                print(request.POST)
                global uid
                uid = request.POST['uid']
                return redirect(f"/profile_manager/view_details/{mydata['uid']}")
            else:
                print(request.POST)
                print("ok")
                if "Approve" in request.POST:
                    data={
                        'uid':request.POST["Approve"],
                        'status':"Approve",
                        'reason':"empty"
                    }
                elif "Reject" in request.POST:
                    data={
                        'uid':request.POST["Reject"],
                        'status':"Reject",
                        'reason':request.POST['reason']
                    }
                print(data)
                response = requests.post(f"http://127.0.0.1:3000/status/{id}",data = data)
                print(response)
        
    return render(request,"profile_finders.html",context)
    
def view_details(request,id):
    value = request.COOKIES.get('profilemanager')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/profile_manager/signin")
    try: 
        mydata = requests.get(f"http://127.0.0.1:3000/pm_my_data/{id}").json()[0]  
        access = ""

    except:
        mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]  
        access = mydata['access_Privileges']
        print(mydata['aid'])
    finally:

        profile_finders(request,id)
        print(uid) 
        specific_data = requests.get(f"http://127.0.0.1:3000/alldata/{uid}").json()
        my = requests.get(f"http://127.0.0.1:3000/alldata/{uid}").json()
        #sibling details
        sibling_name_value=[]
        sibling_relation_value=[]
        sibling_occupation_value=[]
        sibling_name = my['sibling_name'][1:-1].split(", ")
        sibling_relation = my['sibling_relation'][1:-1].split(", ")
        sibling_occupation = my['sibling_occupation'][1:-1].split(", ")
        for sibling_name_x in sibling_name:
            sibling_name_value.append(sibling_name_x[1:-1])
        for sibling_relation_x in sibling_relation:
            sibling_relation_value.append(sibling_relation_x[1:-1])
        for sibling_occupation_x in sibling_occupation:
            sibling_occupation_value.append(sibling_occupation_x[1:-1])
        sibling={}
        sib = [sibling]
        for i, sibling_name_data in enumerate(sibling_name_value):
                sibling[f'sibling_name_{i}'] = sibling_name_data
        for i, sibling_relation_data in enumerate(sibling_relation_value):
                sibling[f'sibling_relation_{i}'] = sibling_relation_data
        for i, sibling_occupation_data in enumerate(sibling_occupation_value):
                sibling[f'sibling_occupation_{i}'] = sibling_occupation_data
        
        print(sib)

        #education
        education_school_value=[]
        education_year_value=[]
        education_course_value=[]
        education_school = my['education_school'][1:-1].split(", ")
        education_year = my['education_year'][1:-1].split(", ")
        education_course = my['education_course'][1:-1].split(", ")
        for education_school_x in education_school:
            education_school_value.append(education_school_x[1:-1])
        for education_year_x in education_year:
            education_year_value.append(education_year_x[1:-1])
        for education_course_x in education_course:
            education_course_value.append(education_course_x[1:-1])
        education={}
        edu = [education]
        for i, education_school_data in enumerate(education_school_value):
                education[f'education_school_{i}'] = education_school_data
        for i, education_year_data in enumerate(education_year_value):
                education[f'education_year_{i}'] = education_year_data
        for i, education_course_data in enumerate(education_course_value):
                education[f'education_course_{i}'] = education_course_data
        
        # print(edu)

        #working experience
        company_name_value=[]
        position_value=[]
        salary_range_value=[]
        profession_value = []
        company_name = my['company_name'][1:-1].split(", ")
        position = my['position'][1:-1].split(", ")
        salary_range = my['salary_range'][1:-1].split(", ")
        profession = my['profession'][1:-1].split(", ")
        for company_name_x in company_name:
            company_name_value.append(company_name_x[1:-1])
        for position_x in position:
            position_value.append(position_x[1:-1])
        for salary_range_x in salary_range:
            salary_range_value.append(salary_range_x[1:-1])
        for profession_x in profession:
            profession_value.append(profession_x[1:-1])
        working={}
        wor = [working]
        for i, company_name_data in enumerate(company_name_value):
                working[f'company_name_{i}'] = company_name_data
        for i, position_data in enumerate(position_value):
                working[f'position_{i}'] = position_data
        for i, salary_range_data in enumerate(salary_range_value):
                working[f'salary_range_{i}'] = salary_range_data
        for i, profession_data in enumerate(profession_value):
                working[f'profession_{i}'] = profession_data
        # print(wor)

    #intrest
        
        
        your_intrest_value=[]
        your_intrest = my['your_intrest'][1:-1].split(", ")
        for i, your_intrest_data in enumerate(your_intrest):
                your_intrest_value.append({'intrest':your_intrest_data[1:-1]})
    
        inte=your_intrest_value
        # print(your_intrest_value)

        yourinterest = my['your_intrest']
        x = yourinterest.replace("[", "").replace("]","").replace("'","").replace(" ","")
        lengthyourinterest = x.split(",")
        # print(lengthyourinterest)

        interestlist = ["Music","Travel","Gaming","Reading","Photograph","Writing","Sports","Artist",
                        "Singing","Custom","Dancer","Speaking"]

        #non intrest
        
        
        non_intrest_value=[]
        non_intrest = my['non_intrest'][1:-1].split(", ")
        for i, non_intrest_data in enumerate(non_intrest):
                non_intrest_value.append({'non_intrest':non_intrest_data[1:-1]})
    
        non_inte=non_intrest_value
        # print(non_inte)

        yournoninterest = my['non_intrest']
        non = yournoninterest.replace("[", "").replace("]","").replace("'","").replace(" ","")
        lengthyournoninterest = non.split(",")

        #complexion
        complexion = my['complexion']
        com = complexion.replace("[", "").replace("]","").replace("'","").replace(" ","")
        lengthcomplexion= com.split(",")
        # print(lengthcomplexion)

        complexionlist = ["Dark","Medium","ModerateFaIr","FaIr","VeryFair"]

        #food taste
        food_taste = my['food_taste']
        ft = food_taste.replace("[", "").replace("]","").replace("'","").replace(" ","")
        lengthfood_taste= ft.split(",")
        # print(lengthfood_taste)

        food_tastelist = ["Sweezt","Bitter","UmamI","Salt","Sour","Spicy"]

        #gallery

        gall = my['gallery']
        ga = gall.replace("[", "").replace("]","").replace("'","").replace(" ","")
        lengthgallery= ga.split(",")

        
        context={
            'key':mydata,
            'current_path':request.get_full_path(),
            'specific_data':specific_data,
            'sibling':sib,
        'education':edu,
        'working':wor,
        'intrest':inte,
        'interestlist':interestlist,
        'lengthyourinterest':lengthyourinterest,
        'non_intrest':non_inte,
        'lengthyournoninterest':lengthyournoninterest,
        'complexionlist':complexionlist,
        'lengthcomplexion':lengthcomplexion,
        'lengthfood_taste':lengthfood_taste,
        'food_tastelist':food_tastelist,
            'lengthgallery':lengthgallery,
            'access_Privileges':access,
        }
        if request.method == "POST":
            print(request.POST)
            print("yes")
            response = requests.post(f"http://127.0.0.1:3000/status/{id}",data = request.POST)
            print(response)
            return redirect(f"profile_manager/profile_finders/{id}")
        
        else:
            pass
    return render(request,"view_details.html",context)

def complaints(request,id):
    value = request.COOKIES.get('profilemanager')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/profile_manager/signin")
    try: 
        mydata = requests.get(f"http://127.0.0.1:3000/pm_my_data/{id}").json()[0]  
        access = ""
        my_profile_finder = requests.get(f"http://127.0.0.1:3000/pm_my_clients/{id}").json()[id]

    except:
        mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]  
        access = mydata['access_Privileges']
        print(mydata['aid'])
        my_profile_finder = requests.get(f"http://127.0.0.1:3000/pm_my_clients/{mydata['aid']}").json()[mydata['aid']]

    finally:
        complaints_list = []
        for i in my_profile_finder:
            if i['complaints'] != "empty":
                complaints_list.append(i)
        context={
            'key':mydata,
            'current_path':request.get_full_path(),
            'my_profile_finder':my_profile_finder,
            'complaints_list':complaints_list,
            'access_Privileges':access,

        }
        if request.method == "POST":
            print(request.POST)
            data = {
                'complaints_replay': request.POST['complaints_replay'],
                'pf_complaints': request.POST['pf_complaints'],
                'my_manager':id,
                'access_Privileges':access_Privileges,
            }
            response = requests.post(f"http://127.0.0.1:3000/my_complaints/{request.POST['uid']}",data = data)
            print(data)
    return render(request,"complaints.html",context)




def profile_finders_approved_list(request,id):
    value = request.COOKIES.get('profilemanager')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/profile_manager/signin")
    try:
        signin(request)
    #     access_Privileges = access_Privileges
    # except:
    #     access_Privileges=""
    finally:
    
        mydata = requests.get(f"http://127.0.0.1:3000/pm_my_data/{id}").json()[0]  
        my_profile_finder = requests.get(f"http://127.0.0.1:3000/pm_my_clients/{id}").json()[id]
        approved_list=[]
        for i in my_profile_finder:
            if i['status'] == "Approve":
                approved_list.append(i)

        context={
            'key':mydata,
            'current_path':request.get_full_path(),
            'all_profile_finder':my_profile_finder,
            'approved_list':approved_list,
            'access_Privileges':access_Privileges,
        }
        if request.method == "POST":
            if 'uid' in request.POST:
                print(request.POST)
                global uid
                uid = request.POST['uid']
                return redirect(f"/profile_manager/view_details/{mydata['uid']}")
            else:
                print(request.POST)
                print("ok")
                if "Approve" in request.POST:
                    data={
                        'uid':request.POST["Approve"],
                        'status':"Approve",
                        'reason':"empty"
                    }
                elif "Reject" in request.POST:
                    data={
                        'uid':request.POST["Reject"],
                        'status':"Reject",
                        'reason':request.POST['reason']
                    }
                print(data)
                response = requests.post(f"http://127.0.0.1:3000/status/{id}",data = data)
                print(response)
    return render(request,"profile_finders_appovedlist.html",context)


def users(request,id):
    value = request.COOKIES.get('profilemanager')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/profile_manager/signin")
    error = ""
    try:
        mydata = requests.get(f"http://127.0.0.1:3000/pm_my_data/{id}").json()[0]  
        my_user = requests.get(f"http://127.0.0.1:3000/pm_my_users_data/{id}").json()
        access = ''
    except:
        mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]  
        my_user = requests.get(f"http://127.0.0.1:3000/pm_my_users_data/{mydata['aid']}").json()
        access = mydata['access_Privileges']
    print(mydata)
    # print(mydata['access_Privileges'])
    # print(my_user)
    if request.method== "POST":
        print(request.POST)
        if "delete" in request.POST:
            response = requests.post(f"http://127.0.0.1:3000/add_user/{id}",data=request.POST)
            print(response.text)
            print(response.status_code)
            return redirect(f"/profile_manager/users/{id}")
        elif "edit" in request.POST:
            global user_uid
            user_uid = request.POST['edit']
            return redirect(f"/profile_manager/user_edit/{id}")
        elif "edit_user" in request.POST:
            print(request.POST)
            if request.POST['password'] == request.POST['confirm_password']:
                data={
                    'first_name': request.POST['first_name'],
                    'last_name':request.POST['last_name'],
                        'email': request.POST['email'],
                        'mobile':request.POST['mobile'],
                            'password': request.POST['password'],
                                'access_Privilegess':  request.POST.getlist('access_Privileges'),
                                'edit':request.POST['edit_user'],
                }
            print(data)
            response = requests.post(f"http://127.0.0.1:3000/add_user/{id}",data=data)
            # print(response.text)
            # print(response.status_code)
            if response.status_code == 200:
                return redirect(f"http://127.0.0.1:8001/profile_manager/users/{id}")
            elif response.status_code == 203:
                print("user already exist")
                error = "User Already Exixts"
    context={
        'key':mydata,
        'current_path':request.get_full_path(),
        'my_user':my_user,
        'error':error,
        'access_Privileges':access,
        
    }

    return render(request,"users.html",context)

def add_user(request,id):
    value = request.COOKIES.get('profilemanager')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/profile_manager/signin")
    error=""
    try:
        mydata = requests.get(f"http://127.0.0.1:3000/pm_my_data/{id}").json()[0]
        if request.method=="POST":
            print(request.POST)
            if request.POST['password'] == request.POST['confirm_password']:
                data={
                    'first_name': request.POST['first_name'],
                    'last_name':request.POST['last_name'],
                        'email': request.POST['email'],
                        'mobile':request.POST['mobile'],
                            'password': request.POST['password'],
                                'access_Privilegess':  request.POST.getlist('access_Privileges'),
                                'work':"profile_manager",
                                'creator':id
                }
            print(data)
            response = requests.post(f"http://127.0.0.1:3000/add_user/{id}",data=data)
            print(response.text)
            print(response.status_code)
            if response.status_code == 200:
                return redirect(f"http://127.0.0.1:8001/profile_manager/users/{id}")
            elif response.status_code == 203:
                print("user already exist")
                error = "User Already Exixts"
        context={
            'key':mydata,
            'current_path':request.get_full_path(),
            'error':error,
            'access_Privileges':access_Privileges,
        }
        return render(request,"add_user.html",context)
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
                                'access_Privilegess':  request.POST.getlist('access_Privileges'),
                                'work':"profile_manager",
                                'creator':mydata['aid']
                }
            print(data)
            response = requests.post(f"http://127.0.0.1:3000/add_user/{id}",data=data)
            print(response.text)
            print(response.status_code)
            if response.status_code == 200:
                return redirect(f"http://127.0.0.1:3000/profile_manager/users/{id}")
            elif response.status_code == 203:
                print("user already exist")
                error = "User Already Exixts"
        context={
            'key':mydata,
            'current_path':request.get_full_path(),
            'error':error,
            'access_Privileges':access_Privileges,
        }
        return render(request,"add_user.html",context)


        

def user_edit(request,id):
    value = request.COOKIES.get('profilemanager')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/profile_manager/signin")
    users(request,id)
    print(user_uid)
    error=""
    try:
        mydata = requests.get(f"http://127.0.0.1:3000/pm_my_data/{id}").json()[0]
        pm_my_users_data   = requests.get(f"http://127.0.0.1:3000/single_users_data/{user_uid}").json()[0]
    except:
        mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]  
        pm_my_users_data   = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]

    finally:   
        print(pm_my_users_data)
        if request.method=="POST":
            print(request.POST)
            if request.POST['password'] == request.POST['confirm_password']:
                data={
                    'first_name': request.POST['first_name'],
                    'last_name':request.POST['last_name'],
                        'email': request.POST['email'],
                        'mobile':request.POST['mobile'],
                            'password': request.POST['password'],
                                'access_Privilegess':  request.POST.getlist('access_Privileges'),
                                'edit':request.POST['edit_user'],
                }
            print(data)
            response = requests.post(f"http://127.0.0.1:3000/add_user/{id}",data=data)
            print(response.text)
            print(response.status_code)
            if response.status_code == 200:
                return redirect(f"http://127.0.0.1:3000/profile_manager/users/{id}")
            elif response.status_code == 203:
                print("user already exist")
                error = "User Already Exixts"
        context={
            'key':mydata,
            'current_path':request.get_full_path(),
            'error':error,
            'pm_my_users_data':pm_my_users_data,
            'access_Privileges':access_Privileges,
        }

    return render(request,"user_edit.html",context)


def settings(request,id):
    value = request.COOKIES.get('profilemanager')
    if value != None:
        print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
    else:
        return redirect("/profile_manager/signin")
    mydata = requests.get(f"http://127.0.0.1:3000/pm_my_data/{id}").json()[0]  
    context={
        'key':mydata,
        'current_path':request.get_full_path()

    }
    if request.method=="POST":
        print(request.POST)
        if 'pass_reset' in request.POST:
            a=request.POST["pass_reset"]
            print(a)
            response = requests.post(f"http://127.0.0.1:3000/pm_password_reset/{id}",data=request.POST )
        else:
            print(request.POST)
            response = requests.post(f"http://127.0.0.1:3000/pm_email_update/{id}", data = request.POST)
            print(response)
            print(response.status_code)
            print(response.text)
            return render(request,"settings.html",context)
        
    return render(request,"settings.html",context)

# //// Password Reset////
def pm_password_reset(request,id):
 #   value = request.COOKIES.get('profilemanager')
  #  if value != None:
   #     print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
   # else:
    #    return redirect("/profile_manager/signin")
    print(id)
    if request.method=="POST":
        print(request.POST)
        if 'pass_reset' in request.POST:
            a=request.POST["pass_reset"]
            print(a)

        if request.POST['password'] == request.POST['confirm_password']:
            response = requests.post(f"http://127.0.0.1:3000/pm_password_update/{id}",data=request.POST )
            messages.info(request,"Password Successfully Updated")
        else:
            messages.info(request,"Password Incorrect")
    return render(request,"pm_password_reset.html")

# /// Forget password////
def pm_forget_password(request):
#    value = request.COOKIES.get('profilemanager')
 #   if value != None:
  #      print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
 #   else:
  #      return redirect("/profile_manager/signin")
    error=""
    if request.method == "POST":
        
        print(request.POST)
        response = requests.post("http://127.0.0.1:3000/pm_forget_password/",data=request.POST)
        print(response)
        print(response.status_code)
        print(type(jsondec.decode(response.text)))
        print(jsondec.decode(response.text))
        uidd = jsondec.decode(response.text)
        
        if response.status_code == 200:
            return redirect(f"/pm_forgetpassword_otpp/{uidd}")
        elif response.status_code == 403:
            error = "User Doesn't Exist"

    context = {'error':error}
    return render(request,"pm_email_send.html",context)
    

def pm_forgetpassword_otp(request,id):
#    value = request.COOKIES.get('profilemanager')
 #   if value != None:
  #      print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
   # else:
    #    return redirect("/profile_manager/signin")
    mydata = requests.get(f"http://127.0.0.1:3000/pm_my_data/{id}").json()[0]
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
        response = requests.post(f"http://127.0.0.1:3000/pm_forget_password_otp/{id}", data=data)
       
        print(response)
        print(response.status_code)
        print(data['user_otp1'])
        print(response.text)
        uidd = (response.text[1:-1])
        
        if response.status_code == 200:
            return redirect(f"/pm_forgetpassword_resett/{uidd}")
        else:
            invalid = "Invalid OTP"
            context = {'invalid':invalid}
    return render(request,"otpcheck.html",context)


def pm_forgetpassword_reset(request,id):
 #   value = request.COOKIES.get('profilemanager')
  #  if value != None:
   #     print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
   # else:
    #    return redirect("/profile_manager/signin")
    error=""
    mydata = requests.get(f"http://127.0.0.1:3000/pm_my_data/{id}").json()[0]
    print(id)
    if request.method=="POST":
        print(request.POST)
        if request.POST['password'] == request.POST['confirm_password']:
            response = requests.post(f"http://127.0.0.1:3000/pm_password_update/{id}",data=request.POST )
            print(response)
            return redirect(f"/profile_manager/signin/")

        else:
            print(response)
            error="password mismatch"
    context = {'invalid':"invalid",
                'key':mydata,
                'error':error}
    return render(request,"pm_forgetpassword.html",context)




