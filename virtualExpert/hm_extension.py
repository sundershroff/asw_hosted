from virtualExpert import models
from virtualExpert import hm_serializer
import random
import string
import yagmail

def id_generate():
    id = str("".join(random.choices(string.ascii_uppercase+string.digits,k=11)))
    return id

def otp_generate():
    return int(random.randrange(1000,9999))

def validate_email(id):
    allData = models.hiringmanager.objects.all()
    profile = hm_serializer.hiringmanagerSerializer(allData,many=True)
    # users
    usersData = models.users.objects.filter(work = "hiring_manager").values()


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
    specificUserData = models.hiringmanager.objects.get(uid = id)
    data = hm_serializer.hiringmanagerSerializer(specificUserData)
    valid = False
    if data.data['otp'] == otp:
        valid = True
    return valid
        
def verify_user(email, password):
    try:
        specificData = models.hiringmanager.objects.get(email = email)
        data = hm_serializer.hiringmanagerSerializer(specificData)
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
        specificData = models.hiringmanager.objects.get(email = email)
        data = hm_serializer.hiringmanagerSerializer(specificData)
        authentication = False
        if data.data['otp'] == data.data['user_otp']:
            authentication = True
        return authentication
    except:
        authentication = True
        return authentication

        
def get_user_id(email):
    try:
        specificData = models.hiringmanager.objects.get(email = email)
        data = hm_serializer.hiringmanagerSerializer(specificData)
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

def send_mail_password(receiver_email, otp):
    sender = 'abijithmailforjob@gmail.com'
    password = 'kgqzxinytwbspurf'
    subject = "Marriyo Forget Password OTP"
    content = f"""
    OTP : {otp}
    """
    yagmail.SMTP(sender, password).send(
        to=receiver_email,
        subject=subject,
        contents=content
    )

def verify_forget_otp(id):
    try:
        specificData = models.hiringmanager.objects.get(uid = id)
        data = hm_serializer.hiringmanagerSerializer(specificData)
        authentication = False
        if data.data['otp1'] == data.data['user_otp1']:
            authentication = True
        return authentication
    except:
        authentication = True
        return authentication
    
def validate_otp1(id, otp1):
    specificUserData = models.hiringmanager.objects.get(uid = id)
    data = hm_serializer.hiringmanagerSerializer(specificUserData)
    
    valid = False
    if data.data['otp1'] == otp1:
        valid = True
   
    return valid