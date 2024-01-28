from virtualExpert import models
from virtualExpert import am_serializer
import random
import string
import yagmail

def id_generate():
    id = str("".join(random.choices(string.ascii_uppercase+string.digits,k=11)))
    return id

def otp_generate():
    return int(random.randrange(1000,9999))

def validate_email(id):
    allData = models.affliate_marketing.objects.all()
    profile = am_serializer.affliatemarketingSerializer(allData,many=True)
    # users
    usersData = models.users.objects.filter(work = "affiliate_marketing").values()
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
    specificUserData = models.affliate_marketing.objects.get(uid = id)
    data = am_serializer.affliatemarketingSerializer(specificUserData)
    valid = False
    print("done")
    print(data.data['otp'])
    if data.data['otp'] == otp:
        valid = True
    print(valid)
    return valid
        
def verify_user(email, password):
    try:
        specificData = models.affliate_marketing.objects.get(email = email)
        data = am_serializer.affliatemarketingSerializer(specificData)
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
        specificData = models.affliate_marketing.objects.get(email = email)
        data = am_serializer.affliatemarketingSerializer(specificData)
        authentication = False
        if data.data['otp'] == data.data['user_otp']:
            authentication = True
        return authentication
    except:
        authentication = True
        return authentication 
        
def get_user_id(email):
    try:
        specificData = models.affliate_marketing.objects.get(email = email)
        data = am_serializer.affliatemarketingSerializer(specificData)
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



def aff_id_generate():
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
        specificData = models.affliate_marketing.objects.get(uid = id)
        data = am_serializer.affliatemarketingSerializer(specificData)
        authentication = False
        if data.data['otp1'] == data.data['user_otp1']:
            authentication = True
        return authentication
    except:
        authentication = True
        return authentication
    
def validate_otp1(id, otp1):
    specificUserData = models.affliate_marketing.objects.get(uid = id)
    data =am_serializer.affliatemarketingSerializer(specificUserData)
    
    valid = False
    if data.data['otp1'] == otp1:
        valid = True 
    return valid