from apiapp import models
from apiapp import pi_serializer
import random
import string
import yagmail

def id_generate():
    id = str("".join(random.choices(string.ascii_uppercase+string.digits,k=11)))
    return id

def otp_generate():
    return int(random.randrange(1000,9999))

def validate_email(id):
    allData = models.private_investigator.objects.all()
    profile = pi_serializer.PrivateinvestigatorSerializer(allData,many=True)
    data = False
    for i in profile.data:
        if id==i['email']:
            data = True
            break
    return data

def validate_otp(id, otp):
    specificUserData = models.private_investigator.objects.get(uid = id)
    data = pi_serializer.PrivateinvestigatorSerializer(specificUserData)
    valid = False
    if data.data['otp'] == otp:
        valid = True
    return valid
        
def verify_user(email, password):
    specificData = models.private_investigator.objects.get(email = email)
    data = pi_serializer.PrivateinvestigatorSerializer(specificData)
    authentication = False
    if data.data['email'] == email and data.data['password'] == password:
        authentication = True
    return authentication
def verify_user_otp(email):
    specificData = models.private_investigator.objects.get(email = email)
    data = pi_serializer.PrivateinvestigatorSerializer(specificData)
    authentication = False
    if data.data['otp'] == data.data['user_otp']:
        authentication = True
    return authentication

        
def get_user_id(email):
    specificData = models.private_investigator.objects.get(email = email)
    data = pi_serializer.PrivateinvestigatorSerializer(specificData)
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