

import random
import string
from django.core.mail import send_mail
from django.conf import settings
from .models import User

def generate_otp(length=4):
    characters = string.digits
    otp = ''.join(random.choice(characters) for _ in range(length))
    return otp

def send_otp_email(email):
    otp = generate_otp()
    subject = 'Your OTP for Login'
    message = f'Your OTP is: {otp}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)
    user = User.objects.get(email = email)
    user.otp = otp
    user.save()