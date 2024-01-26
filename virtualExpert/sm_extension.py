from virtualExpert import models
from virtualExpert import sm_serializer
import random
import string
import yagmail

def id_generate():
    id = str("".join(random.choices(string.ascii_uppercase+string.digits,k=11)))
    return id

def otp_generate():
    return int(random.randrange(1000,9999))

def validate_email(id):
    allData = models.salesmanager.objects.all()
    profile = sm_serializer.salesmanagerSerializer(allData,many=True)
    # users
    usersData = models.users.objects.filter(work = "sales_manager").values()

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
    specificUserData = models.salesmanager.objects.get(uid = id)
    data = sm_serializer.salesmanagerSerializer(specificUserData)
    valid = False
    if data.data['otp'] == otp:
        valid = True
    return valid
        
def verify_user(email, password):
    try:
        specificData = models.salesmanager.objects.get(email = email)
        data = sm_serializer.salesmanagerSerializer(specificData)
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
        specificData = models.salesmanager.objects.get(email = email)
        data = sm_serializer.salesmanagerSerializer(specificData)
        authentication = False
        if data.data['otp'] == data.data['user_otp']:
            authentication = True
        return authentication

    except:
        authentication = True
        return authentication        
def get_user_id(email):
    try:
        specificData = models.salesmanager.objects.get(email = email)
        data = sm_serializer.salesmanagerSerializer(specificData)
        return data.data['uid']
    except:
        #users
        print("users")
        usersData = models.users.objects.filter(email = email).values()[0]
        print(usersData['uid'])
        return usersData['uid']


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


def otp_client_generate():
    return int(random.randrange(100000,999999))

def validate_client_otp(id,otp):
    specificUserData = models.ad_client.objects.get(uid = id)
    data = sm_serializer.add_client_serializer(specificUserData)
    valid = False
    if data.data['otp'] == otp:
        valid = True
    return valid

def verify_client_otp(email):
    specificData = models.ad_client.objects.get(email = email)
    data = sm_serializer.add_client_serializer(specificData)
    authentication = False
    if data.data['otp'] == data.data['user_otp']:
        authentication = True
    return authentication

def send_mail(receiver_email, otp):
    sender = 'abijithmailforjob@gmail.com'
    password = 'kgqzxinytwbspurf'
    subject = "Marriyo client OTP"
    content = f"""
    OTP : {otp}
    """
    yagmail.SMTP(sender, password).send(
        to=receiver_email,
        subject=subject,
        contents=content
    )


def sales_id_generate():
    id = str("".join(random.choices(string.ascii_uppercase+string.digits,k=11)))
    return id

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
        specificData = models.salesmanager.objects.get(uid = id)
        data = sm_serializer.salesmanagerSerializer(specificData)
        authentication = False
        if data.data['otp1'] == data.data['user_otp1']:
            authentication = True
        return authentication
    except:
        authentication = True
        return authentication
    
def validate_otp1(id, otp1):
    specificUserData = models.salesmanager.objects.get(uid = id)
    data =sm_serializer.salesmanagerSerializer(specificUserData)
    
    valid = False
    if data.data['otp1'] == otp1:
        valid = True
   
    return valid