from superadmin import models
from superadmin import serializer
import random
import string
import yagmail

def id_generate():
    id = str("".join(random.choices(string.ascii_uppercase+string.digits,k=11)))
    return id

def otp_generate():
    return int(random.randrange(1000,9999))

def validate_email(id):
    print("sunder")
    allData = models.superadmin_data.objects.all()
    print(allData)
    profile = serializer.superadminSerializer(allData,many=True)
        #users
    usersData = models.third_party_user.objects.all()
    print(usersData)
    data = False
    for i in profile.data:
        if id==i['email']:
            data = True
            break
    for j in usersData:
        if id==j.email:
            data = True
            break
    return data

def validate_otp(id, otp):
    specificUserData = models.superadmin_data.objects.get(uid = id)
    data = serializer.superadminSerializer(specificUserData)
    valid = False
    if data.data['otp'] == otp:
        valid = True
    return valid
        
def verify_user(email, password):
    try:
        print("verify user")
        specificData = models.superadmin_data.objects.get(email = email)
        data = serializer.superadminSerializer(specificData)
        authentication = False
        if data.data['email'] == email and data.data['password'] == password:
            authentication = True
        return authentication
    except:
        #users
        print("users")
        usersData = models.third_party_user.objects.filter(email = email).values()[0]
        print(usersData)
        print(password)
        authentication = False
        if usersData['email'] == email and usersData['password'] == password:
            authentication = True
            print(" correct password")
        return authentication
def verify_user_otp(email):
    try:
        print("verify user otp")
        specificData = models.superadmin_data.objects.get(email = email)
        data = serializer.superadminSerializer(specificData)
        authentication = False
        if data.data['otp'] == data.data['user_otp']:
            authentication = True
        return authentication
    except:
        authentication = True
        return authentication

        
def get_user_id(email):
    try:
        print("ready")
        specificData = models.superadmin_data.objects.get(email = email)
        data = serializer.superadminSerializer(specificData)
        print(data.data['id'])
        return data.data['id']
    except:
        #users
        print("users")
        usersData = models.third_party_user.objects.filter(email = email).values()[0]
        # creator = usersData['creator']
        print(usersData['id'])
        return usersData['id']


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