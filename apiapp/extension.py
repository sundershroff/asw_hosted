from apiapp import models
from apiapp import serializer
import random
import string
import yagmail

def id_generate():
    id = str("".join(random.choices(string.ascii_uppercase+string.digits,k=11)))
    return id

def otp_generate():
    return int(random.randrange(1000,9999))

def validate_email(id):
    allData = models.ProfileFinder.objects.all()
    profile = serializer.ProfileFinderSerializer(allData,many=True)
    data = False
    for i in profile.data:
        if id==i['email']:
            data = True
            break
    return data

def validate_otp(id, otp):
    specificUserData = models.ProfileFinder.objects.get(uid = id)
    data = serializer.ProfileFinderSerializer(specificUserData)
    valid = False
    if data.data['otp'] == otp:
        valid = True
    return valid
        
def verify_user(email, password):
    specificData = models.ProfileFinder.objects.get(email = email)
    data = serializer.ProfileFinderSerializer(specificData)
    authentication = False
    if data.data['email'] == email and data.data['password'] == password:
        authentication = True
    return authentication
def verify_user_otp(email):
    specificData = models.ProfileFinder.objects.get(email = email)
    data = serializer.ProfileFinderSerializer(specificData)
    authentication = False
    if data.data['otp'] == data.data['user_otp']:
        authentication = True
    return authentication

        
def get_user_id(email):
    specificData = models.ProfileFinder.objects.get(email = email)
    data = serializer.ProfileFinderSerializer(specificData)
    return data.data['uid']


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




def pf_id_generate():
    id = str("".join(random.choices(string.ascii_uppercase+string.digits,k=11)))
    return id


# forget password
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
        specificData = models.ProfileFinder.objects.get(uid = id)
        data = serializer.ProfileFinderSerializer(specificData)
        authentication = False
        if data.data['otp1'] == data.data['user_otp1']:
            authentication = True
        return authentication
    except:
        authentication = True
        return authentication
    
def validate_otp1(id, otp1):
  
    specificUserData = models.ProfileFinder.objects.get(uid = id)
    data =serializer.ProfileFinderSerializer(specificUserData)
    valid = False
    if data.data['otp1'] == otp1:
        valid = True
    return valid