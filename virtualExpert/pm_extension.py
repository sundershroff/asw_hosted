from virtualExpert import models
from virtualExpert import pm_serializer
import random
import string
import yagmail
import json

def id_generate():
    id = str("".join(random.choices(string.ascii_uppercase+string.digits,k=11)))
    return id

def otp_generate():
    return int(random.randrange(1000,9999))

def validate_email(id):
    allData = models.Profilemanager.objects.all()
    profile = pm_serializer.ProfilemanagerSerializer(allData,many=True)
    #users
    usersData = models.users.objects.filter(work = "profile_manager").values()
    data = False
    for i in profile.data:
        if id==i['email']:
            data = True
            break
    for j in usersData:
        print(j['email'])
        if id==j['email']:
            data = True
            break
    print("ok")
    return data

def validate_otp(id, otp):
    specificUserData = models.Profilemanager.objects.get(uid = id)
    data = pm_serializer.ProfilemanagerSerializer(specificUserData)
    valid = False
    if data.data['otp'] == otp:
        valid = True
    return valid
        
def verify_user(email, password):
    try:
        specificData = models.Profilemanager.objects.get(email = email)
        data = pm_serializer.ProfilemanagerSerializer(specificData)
        authentication = False
        if data.data['email'] == email and data.data['password'] == password:
            authentication = True
        return authentication
    except:
        #users
        print("users")
        usersData = models.users.objects.filter(email = email).values()[0]
        print(usersData)
        authentication = False
        if usersData['email'] == email and usersData['password'] == password:
            authentication = True
            print(" correct password")
        return authentication

def verify_user_otp(email):
    try:
        specificData = models.Profilemanager.objects.get(email = email)
        data = pm_serializer.ProfilemanagerSerializer(specificData)
        authentication = False
        if data.data['otp'] == data.data['user_otp']:
            authentication = True
        return authentication
    except:
        authentication = True
        return authentication



        
def get_user_id(email):
    try:
        specificData = models.Profilemanager.objects.get(email = email)
        data = pm_serializer.ProfilemanagerSerializer(specificData)
        return data.data['uid']
    except:
        #users
        print("users")
        usersData = models.users.objects.filter(email = email).values()[0]
        creator = usersData['creator']
        data={
            'uid':creator,
            'access_Privileges':usersData['access_Privileges']
        }
        print(data)
        return data


def send_mail(receiver_email, otp):
    sender = 'abijithmailforjob@gmail.com'
    password = 'kgqzxinytwbspurf'
    subject = "Marriyo Sign Up OTP"
    content = f"""
    OTP : {otp}
    """
    yagmail.SMTP(sender, password).send(
        to=receiver_email,
        subject=subject,
        contents=content
    )