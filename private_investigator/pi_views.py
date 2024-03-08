from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib import messages
# from .forms import *
# from private_investigator.models import *
# from chat.models import Thread
# from django.core.files.storage import FileSystemStorage
# from django.core.files.storage import default_storage
# import cv2
# from django.http import JsonResponse
import requests
import json
# from django.urls import reverse

# import random
# import string

# import PyPDF2
# import re
# import datetime

# import base64
# from io import BytesIO
# from PIL import Image

# from django.db import connections
# # Create your views here.
# from django.core import serializers
# from django.http import HttpResponse
jsondec = json.decoder.JSONDecoder()
all_url = "http://127.0.0.1:3000/"

def signin(request):
    value = request.COOKIES.get('private_investigator')
    print(value)
    error = ""
    if request.method == "POST":
        print(request.POST)
        # response = requests.post("http://54.159.186.219:8000/signin/",data=request.POST)
        response = requests.post(all_url+"pi_signin/",data=request.POST)
        print(response.status_code)
        print(response.text)
        uidd = (response.text[1:-1])
        print(uidd)
        if response.status_code == 200:
        # if get["otp"] == data['user_otp']:
            response = redirect(f"/pi_admin_dashboard/{uidd}")
            response.set_cookie("private_investigator",uidd)
            return response
        else:
            error = "YOUR EMAILID OR PASSWORD IS INCORRECT"
        
    context = {'error':error}
    return render(request,"pi_signin.html",context)


def signup(request):
    error = ""
    if request.method == "POST":
        
        if request.POST['password'] == request.POST['confirm_password']:
                # response = requests.post('http://54.159.186.219:8000/signup/',data=request.POST)
                response = requests.post(all_url+'pi_signup/',data=request.POST)
                print(response.status_code)
                print(response.text)
                uidd = (response.text[1:-1])
                print(uidd)
                if response.status_code == 302:
                   error = "User Already Exist"
                else:
                   return redirect(f"/pi_otpcheck/{uidd}")      
    context = {'error':error}
        
    return render(request,'pi_signup.html',context)

def opt_check(request,id):
    # form1 = ProfileOtpForm()
    # get = requests.get(f" http://127.0.0.1:3000/otp/{id}").json()
    # print(get['otp'])
    # print(get['uid'])
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
        response = requests.post(f"http://127.0.0.1:3000/pi_otp/{id}", data=data)

       
        print(response)
        print(response.status_code)
        print(data['user_otp'])
        print(response.text)
        uidd = (response.text[1:-1])
        
        if response.status_code == 200:
        # if get["otp"] == data['user_otp']:
            # return redirect(f"/profileidcard/{uidd}")
            return redirect(f"/pi_profilepicture/{uidd}")
        else:
            invalid = "Invalid OTP"
            context = {'invalid':invalid}

    return render(request,'pi_otpcheck.html',context)

def profile_picture(request,id):
    if request.method == "POST":
        print(request.POST)
        # response = requests.post(f"http://54.159.186.219:8000/profilepicture/{id}",files=request.FILES)
        response = requests.post(f"http://127.0.0.1:3000/pi_profilePicture/{id}",files=request.FILES)
        print(response)
        print(response.status_code)
        print(response.text)
        uidd = (response.text[1:-1])
        print(uidd)
        if response.status_code == 200:
        # if get["otp"] == data['user_otp']:
            return redirect(f"/pi_complete_profile/{uidd}")
        # else:
            # return HttpResponse("INVALID data")
    return render(request,"pi_profilepicture.html")

def complete_profile(request,id):
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
        dictio = dict(request.POST)
        print(dictio)
        # response = requests.post(f"http://54.159.186.219:8000/profilepicture/{id}",files=request.FILES)
        response = requests.post(f"http://127.0.0.1:3000/pi_complete_account/{id}",data = dictio,files=request.FILES)
        print(response)
        print(response.status_code)
        print(response.text)
        uidd = (response.text[1:-1])
        print(uidd)
        if response.status_code == 200:
        # if get["otp"] == data['user_otp']:
            return redirect(f"/pi_admin_dashboard/{uidd}")
        # else:
            # return HttpResponse("INVALID data")
    return render(request,"uploadprofile.html",context)

def pi_logout(request):
    print("logout")
    value = request.COOKIES.get('private_investigator')
    print(value)
    response = redirect("/pi_signin")
    # response = HttpResponse("delete cookie")
    response.delete_cookie("private_investigator")
    return response

def admin_dashboard(request,id):
        value = request.COOKIES.get('private_investigator')
        if value != None:
            print(value)
            # return redirect("/Dashboard_profile_finder/{value}")
        else:
            return redirect("/pi_signin")
        my = requests.get(f"http://127.0.0.1:3000/pi_my_data/{id}").json()[0]
        pf_users = requests.get("http://127.0.0.1:3000/alluserdata/").json()
        # print(pf_users)
        my_client = requests.get(f"http://127.0.0.1:3000/pi_my_clients/{id}").json()[id]
        filtered_clients = []
        for x in my_client:
            if "empty" not in x['answer']:
                filtered_clients.append(x)
        #closed investigation'
        closed=[]
        for x in my_client:
            # print(x['answer'])
            if x['answer'] is None:
                print("")
            elif "empty" not in x['answer']:
                closed.append("1")
        # print(len(closed))
        
        # pending investigation
        pending=[]
        for x in my_client:
            # print(x['answer'])
            if x['answer'] is None:
                pending.append("1")
            elif "empty" in x['answer']:
                pending.append("1")
        # print(len(pending))
        if len(filtered_clients) != 0:
            # percentage
            bad_review = []
            good_review=[]
            for j in filtered_clients:
                if j['rating'] == "empty":
                    bad_review.append(j['rating'])
                elif j['rating'] == "0":
                    bad_review.append(j['rating'])
                elif j['rating'] == "1.0":
                    bad_review.append(j['rating'])
                elif j['rating'] == "2.0":
                    bad_review.append(j['rating'])
                elif j['rating'] == "3.0":
                    good_review.append(j['rating'])
                elif j['rating'] == "4.0":
                    good_review.append(j['rating'])
                elif j['rating'] == "5.0":
                    good_review.append(j['rating'])
            badreview = int(len(bad_review)/len(filtered_clients)*100)
            goodreview = int(len(good_review)/len(filtered_clients)*100)
            
            #total ratings
            total_r = []
            one=[]
            two=[]
            three=[]
            four=[]
            five=[]
            
            for z in filtered_clients:
               print(z['rating'])
               if "empty" not in z['rating']:
                   total_r.append(z['rating'])
            print(total_r)
            
            for j in filtered_clients:
                if j['rating'] == "1.0":
                    one.append(j['rating'])
                elif j['rating'] == "2.0":
                    two.append(j['rating'])
                elif j['rating'] == "3.0":
                    three.append( j['rating'])
                elif j['rating'] == "4.0":
                    four.append(j['rating'])
                elif j['rating'] == "5.0":
                    five.append(j['rating'])
            score_total = len(five)*5 + len(four) * 4 + len(three) * 3 + len(two) * 2 + len(one) * 1
            response_total = len(five)+ len(four) + len(three) + len(two)+len(one)
            print(score_total)
            print("res",response_total)
            total_ratings = score_total/response_total
            print((total_ratings))
        else:
            total_ratings=0
            
    
        context={'key':my,
                 'current_path':request.get_full_path(),
                 'profile_finder':pf_users,
                 'my':my,
                 'my_client':my_client,
                 'closed':len(closed),
                 'pending':len(pending),
                'total_ratings':total_ratings,
                'filtered_clients':filtered_clients,

                 }
        return render(request,"admin_dashboard.html",context)

def profile(request,id):
        value = request.COOKIES.get('private_investigator')
        if value != None:
            print(value)
            # return redirect("/Dashboard_profile_finder/{value}")
        else:
            return redirect("/pi_signin")
        my = requests.get(f"http://127.0.0.1:3000/pi_my_data/{id}").json()[0]
        # print(my)
        education  = jsondec.decode(my['level_education'])
        study = jsondec.decode(my['field_study'])
        my_clients = requests.get(f"http://127.0.0.1:3000/pi_my_clients/{id}").json()[id]
        filtered_clients = []
        if len(my_clients) != 0:
            for x in my_clients:
                if "empty" not in x['answer']:
                    filtered_clients.append(x)
            if len(filtered_clients) != 0:
                # percentage
                bad_review = []
                good_review=[]
                for j in filtered_clients:
                    if j['rating'] == "empty":
                        bad_review.append(j['rating'])
                    elif j['rating'] == "0":
                        bad_review.append(j['rating'])
                    elif j['rating'] == "1.0":
                        bad_review.append(j['rating'])
                    elif j['rating'] == "2.0":
                        bad_review.append(j['rating'])
                    elif j['rating'] == "3.0":
                        good_review.append(j['rating'])
                    elif j['rating'] == "4.0":
                        good_review.append(j['rating'])
                    elif j['rating'] == "5.0":
                        good_review.append(j['rating'])
                badreview = int(len(bad_review)/len(filtered_clients)*100)
                goodreview = int(len(good_review)/len(filtered_clients)*100)
            
                print(len(bad_review))
                print(len(filtered_clients))
                print(badreview)
                print(goodreview)
           
                #total ratings
                total_r = []
                one=[]
                two=[]
                three=[]
                four=[]
                five=[]
                
                for z in filtered_clients:
                #    print(z['rating'])
                    if "empty" not in z['rating']:
                       total_r.append(z['rating'])
                # print(total_r)
                
                       for j in filtered_clients:
                           print(j['rating'])
                           if j['rating'] == "1.0":
                               one.append(j['rating'])
                           elif j['rating'] == "2.0":
                               two.append(j['rating'])
                           elif j['rating'] == "3.0":
                               three.append(j['rating'])
                           elif j['rating'] == "4.0":
                               four.append(j['rating'])
                           elif j['rating'] == "5.0":
                               five.append(j['rating'])
                       score_total = len(five)*5 + len(four) * 4 + len(three) * 3 + len(two) * 2 + len(one) * 1
                       response_total = len(five)+ len(four) + len(three) + len(two)+len(one)
                       total_ratings = score_total/response_total
                    else:
                        total_ratings=0
            else:
                badreview=0
                goodreview=0
                total_ratings=0
        else:
            badreview=0
            goodreview=0
            total_ratings=0
        print(total_ratings)
        context={'key':my,
                 'current_path':request.get_full_path(),
                 'my_clients':filtered_clients,
                 'bad_review':badreview,
                 'good_review':goodreview,
                 'total_ratings':total_ratings,
                 'education':education,
        'study':study,
                 }
        return render(request,"profile.html",context)

def edit_profile(request,id):
        value = request.COOKIES.get('private_investigator')
        if value != None:
            print(value)
            # return redirect("/Dashboard_profile_finder/{value}")
        else:
            return redirect("/pi_signin")
        my = requests.get(f"http://127.0.0.1:3000/pi_my_data/{id}").json()[0]
        # print(my)
        if request.method == "POST":
            print(request.POST)
            print(request.FILES)
            response = requests.post(f"http://127.0.0.1:3000/pi_edit_account/{id}",data=request.POST,files=request.FILES)
            return redirect(f"/pi_profile/{id}")
        context={'key':my,
                 'current_path':request.get_full_path()
                 }
        return render(request,"edit_profile.html",context)

def payment(request,id):
        value = request.COOKIES.get('private_investigator')
        if value != None:
            print(value)
            # return redirect("/Dashboard_profile_finder/{value}")
        else:
            return redirect("/pi_signin")
        my = requests.get(f"http://127.0.0.1:3000/pi_my_data/{id}").json()[0]
        print(my)
        context={'key':my,
                 'current_path':request.get_full_path()
                 }
        return render(request,"pi_payment1.html",context)

def client_list(request,id):
        value = request.COOKIES.get('private_investigator')
        if value != None:
            print(value)
            # return redirect("/Dashboard_profile_finder/{value}")
        else:
            return redirect("/pi_signin")
        my = requests.get(f"http://127.0.0.1:3000/pi_my_data/{id}").json()[0]
        # print(my)
        
        my_client = requests.get(f"http://127.0.0.1:3000/pi_my_clients/{id}").json()[id]
        if len(my_client) == 0:
            all_profinder_data_values = requests.get("http://127.0.0.1:3000/alluserdata/").json()
        else:
            all_profinder_data_values=[]
            all_profinder_data = requests.get("http://127.0.0.1:3000/alluserdata/").json()
            for x in all_profinder_data:
                if x['uid'] not in str(my_client):
                    print(x)
                    all_profinder_data_values.append(x)

        #post
        if "client_one" in request.POST:
            print(request.POST)
            global client_one
            client_one = request.POST['client_one']
            return redirect(f"/pi_client_details/{id}")
        
        elif "pf_id" in request.POST:
            print(request.POST)
            filter = {
            'f_u_id': request.POST['pf_id'].strip(),
            'f_u_name': request.POST['pf_name'].strip().lower(),
            'f_u_email': request.POST['pf_email'].strip().lower(),
            'f_u_phone': request.POST['pf_phone'].strip(),
            'f_u_location': request.POST['pf_location'].strip().lower(),
            'f_u_status': request.POST['pf_status'].strip().lower(),
            }

            p = set()

            for x in all_profinder_data_values:
                if (filter['f_u_id'] == x['uid'] or not filter['f_u_id']) and \
                (filter['f_u_name'] == x['name'].lower() or not filter['f_u_name']) and \
                (filter['f_u_email'] == x['email'].lower() or not filter['f_u_email']) and \
                (filter['f_u_phone'] == x['mobile'] or not filter['f_u_phone']) and \
                (filter['f_u_location'] == x['r_state'].lower() or not filter['f_u_location']) and \
                (filter['f_u_status'] == x['family_status'].lower() or not filter['f_u_status'] ):
                    p.add(x['uid'])

            all_profinder_data_values = [x for x in all_profinder_data_values if x['uid'] in p]
            print(all_profinder_data_values)

        context={'key':my,
                 'current_path':request.get_full_path(),
                 'all_profinder_data':all_profinder_data_values,
                 'my_client':my_client,
                 }
        return render(request,"Client_list.html",context)
def client_details(request,id):
        value = request.COOKIES.get('private_investigator')
        if value != None:
            print(value)
            # return redirect("/Dashboard_profile_finder/{value}")
        else:
            return redirect("/pi_signin")
        my = requests.get(f"http://127.0.0.1:3000/pi_my_data/{id}").json()[0]
        jsonDec = json.decoder.JSONDecoder()
        # print(my)
        client_list(request,id)
        print(client_one)
        all_profinder_data = requests.get("http://127.0.0.1:3000/alluserdata/").json()
        for x in all_profinder_data:
            if x['uid'] == client_one:
                specific_user = x
                if specific_user['Questin'] is not None:
                   question = jsonDec.decode(specific_user['Questin'])
                   print(question)
                else:
                    question=""
                # question_and_Answer = requests.get(f"http://127.0.0.1:3000/my_question_and_answer/{x['uid']}").json()[x['uid']]
             
        context={'key':my,
                 'current_path':request.get_full_path(),
                 'specific_user':[specific_user],
                 'question_and_Answer':question,
                 }
        return render(request,"client_details.html",context)

def subscription(request,id):
        value = request.COOKIES.get('private_investigator')
        if value != None:
            print(value)
            # return redirect("/Dashboard_profile_finder/{value}")
        else:
            return redirect("/pi_signin")
        my = requests.get(f"http://127.0.0.1:3000/pi_my_data/{id}").json()[0]
        print(my)
        context={'key':my,
                 'current_path':request.get_full_path()
                 }
        return render(request,"pi_subscription.html",context)

def payment_table(request,id):
        value = request.COOKIES.get('private_investigator')
        if value != None:
            print(value)
            # return redirect("/Dashboard_profile_finder/{value}")
        else:
            return redirect("/pi_signin")
        my = requests.get(f"http://127.0.0.1:3000/pi_my_data/{id}").json()[0]
        print(my)
        context={'key':my,
                 'current_path':request.get_full_path()
                 }
        return render(request,"pi_payment_table.html",context)


def add_client(request,id):
        value = request.COOKIES.get('private_investigator')
        if value != None:
            print(value)
            # return redirect("/Dashboard_profile_finder/{value}")
        else:
            return redirect("/pi_signin")
        my = requests.get(f"http://127.0.0.1:3000/pi_my_data/{id}").json()[0]
        # print(my)
        my_client = requests.get(f"http://127.0.0.1:3000/pi_my_clients/{id}").json()[id]
        # print(my_client[0]['answer'])
        if len(my_client) !=0:
            if "empty" not in str(my_client[0]['answer']):
                result= "complete"
            else:
                result= "empty"
        else:
            result="empty"
        if "my_client_one" in request.POST:
           print(request.POST)
           global my_client_one
           my_client_one = request.POST['my_client_one']  
           return redirect(f"/pi_client_feedback/{id}")
        
        elif "pf_id" in request.POST:
                    print(request.POST)
                    filter = {
                    'f_u_id': request.POST['pf_id'].strip(),
                    'f_u_name': request.POST['pf_name'].strip().lower(),
                    'f_u_email': request.POST['pf_email'].strip().lower(),
                    'f_u_phone': request.POST['pf_phone'].strip(),
                    'f_u_location': request.POST['pf_location'].strip().lower(),
                    'f_u_status': request.POST['pf_status'].strip().lower(),
                    }

                    p = set()

                    for x in my_client:
                        if (filter['f_u_id'] == x['uid'] or not filter['f_u_id']) and \
                        (filter['f_u_name'] == x['name'].lower() or not filter['f_u_name']) and \
                        (filter['f_u_email'] == x['email'].lower() or not filter['f_u_email']) and \
                        (filter['f_u_phone'] == x['mobile'] or not filter['f_u_phone']) and \
                        (filter['f_u_location'] == x['r_state'].lower() or not filter['f_u_location']) and \
                        (filter['f_u_status'] == x['family_status'].lower() or not filter['f_u_status']):
                            p.add(x['uid'])

                    my_client = [ad for ad in my_client if ad['uid'] in p]
                    print(my_client)

                    
        context={'key':my,
                 'current_path':request.get_full_path(),
                 'my_client':my_client,
                'result' :result,

                 }
        return render(request,"pi_add_new_client.html",context)


def client_feedback(request,id):
        value = request.COOKIES.get('private_investigator')
        if value != None:
            print(value)
            # return redirect("/Dashboard_profile_finder/{value}")
        else:
            return redirect("/pi_signin")
        my = requests.get(f"http://127.0.0.1:3000/pi_my_data/{id}").json()[0]
        # print(my)
        # add_client(request,id)
        # print(my_client_one)
        profile_finder_value = requests.get(f"http://127.0.0.1:3000/pi_my_clients/{id}").json()[id]
        
        # print(all_profile_finder)
        for x in profile_finder_value:
            if my_client_one == x['uid']:
                print(x)
                specific_user = x
                print( x['Questin'])
                all_profile_finder_Questin = x['Questin']
                all_profile_finder_answer = x['answer']
                all_profile_finder = zip(all_profile_finder_Questin,all_profile_finder_answer)
                # question_and_Answer = requests.get(f"http://127.0.0.1:3000/my_question_and_answer/{x['uid']}").json()[x['uid']]
                # situation_prediction = requests.get(f"http://127.0.0.1:3000/my_question_and_answer/{x['uid']}").json()[x['uid']]
                question_and_Answer = x
                situation_prediction = x
                # print(question_and_Answer)
                if "empty" not in str(question_and_Answer):
                    result= "complete"
                else:
                    result = "empty"
        
        #situation
        print("situation")
        # sit = []
        # for x in situation_prediction:
        #     sit.append(x['answer'])
        # if "empty" in sit:
        #     situation = "pending"
        # else:
        #     situation = "complete"
              
        #post
        if request.method=="POST":
            print(request.POST)
            data={
                'answer':request.POST['answer'],
                'question':request.POST['question'],
                'my_investigator':id
            }
            response = requests.post(f"http://127.0.0.1:3000/my_question_and_answer/{specific_user['uid']}",data=data)
            print(response)
            print(response.status_code)
            print(response.text)

        context={'key':my,
                 'current_path':request.get_full_path(),
                 'specific_user':[specific_user],
                 'question_and_Answer':question_and_Answer,
                 'result' :result,
                 'all_profile_finder':all_profile_finder,
                #  'situation':situation,
                 }
        return render(request,"pi_client_feedback.html",context)

def setting(request,id):
        value = request.COOKIES.get('private_investigator')
        if value != None:
            print(value)
            # return redirect("/Dashboard_profile_finder/{value}")
        else:
            return redirect("/pi_signin")
        my = requests.get(f"http://127.0.0.1:3000/pi_my_data/{id}").json()[0]
        print(my)
        context={'key':my,
                 'current_path':request.get_full_path()
                 }
        
        if request.method=="POST":
            print(request.POST)
            if 'pass_reset' in request.POST:
            
                a=request.POST["pass_reset"]
                print(a)
       
                response = requests.post(f"http://127.0.0.1:3000/privateinvest_password_reset/{id}",data=request.POST )
            else:
            
                response = requests.post(f"http://127.0.0.1:3000/pi_email_update/{id}", data = request.POST)
                print(response)
                print(response.status_code)
                print(response.text)
                return render(request,"pi_Account_Settings.html",context)
        return render(request,"pi_Account_Settings.html",context)


def password_reset(request,id):
#    value = request.COOKIES.get('private_investigator')
 #   if value != None:
  #      print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
   # else:
    #    return redirect("/pi_signin")
    print(id)
    if request.method=="POST":
        print(request.POST)
        if 'pass_reset' in request.POST:
            
            a=request.POST["pass_reset"]
            print(a)
        if request.POST['password'] == request.POST['confirm_password']:

            response = requests.post(f"http://127.0.0.1:3000/pass_privateInvestigator_update/{id}",data=request.POST )
            messages.info(request,"Password Successfully Updated")
        else:
            messages.info(request,"Password Incorrect")
    return render(request,"password_reset.html")



# forget password

def pi_forget_password(request):
#    value = request.COOKIES.get('private_investigator')
 #   if value != None:
  #      print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
   # else:
   #     return redirect("/pi_signin")
    error=""
    if request.method == "POST":
        
        print(request.POST)
        response = requests.post("http://127.0.0.1:3000/pi_forget_password/",data=request.POST)
        print(response)
        print(response.status_code)
        print(type(jsondec.decode(response.text)))
        print(jsondec.decode(response.text))
        uidd = jsondec.decode(response.text)
        
        if response.status_code == 200:
            return redirect(f"/pi_forgetpassword_otpp/{uidd}")
        elif response.status_code == 403:
            error = "User Doesn't Exist"

    context = {'error':error}
    return render(request,"pi_email.html",context)
    

def pi_forgetpassword_otp(request,id):
#    value = request.COOKIES.get('private_investigator')
 #   if value != None:
  #      print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
   # else:
    #    return redirect("/pi_signin")
    mydata = requests.get(f"http://127.0.0.1:3000/pi_my_data/{id}").json()[0]
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
        response = requests.post(f"http://127.0.0.1:3000/pi_forget_password_otp/{id}", data=data)
       
        print(response)
        print(response.status_code)
        print(data['user_otp1'])
        print(response.text)
        uidd = (response.text[1:-1])
        
        if response.status_code == 200:
            return redirect(f"/pi_forgetpassword_resett/{uidd}")
        else:
            invalid = "Invalid OTP"
            context = {'invalid':invalid}
    return render(request,"pi_otpcheck.html",context)


def pi_forgetpassword_reset(request,id):
#    value = request.COOKIES.get('private_investigator')
 #   if value != None:
  #      print(value)
        # return redirect("/Dashboard_profile_finder/{value}")
   # else:
    #    return redirect("/pi_signin")
    error=""
    mydata = requests.get(f"http://127.0.0.1:3000/pi_my_data/{id}").json()[0]
    print(id)
    if request.method=="POST":
        print(request.POST)
        if request.POST['password'] == request.POST['confirm_password']:
            response = requests.post(f"http://127.0.0.1:3000/pass_privateInvestigator_update/{id}",data=request.POST )
            print(response)
            return redirect(f"/pi_signin")

        else:
            print(response)
            error="password mismatch"
    context = {'invalid':"invalid",
                'key':mydata,
                'error':error}
    return render(request,"pi_forgetpassword.html",context)

