import random
import string

from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _

from apps.users.models import User

code = random.randint(1000, 9999)
reset_password = random.randint(1000, 9999)


def send_email_confirmation(email):
    subject = _("Email Confirmation")
    message = _(
        f"Hello! Your email address was provided for logging into the Zarina application. "
        f"Please enter this code on the login page: {code}. "
        f"If this was not you or you did not register on the site, simply ignore this email."
    )
    email_from = "ttestdb01@gmail.com"
    send_mail(subject, message, email_from, [email])
    user_obj = User.objects.get(email=email)
    user_obj.otp = code
    user_obj.save()


def send_email_reset_password(email, reset_password):
    subject = _("Password Reset")
    message = _(
        f"Password reset code: {reset_password}. The code is valid for 5 minutes."
    )
    email_from = "proverkageeks@gmail.com"
    send_mail(subject, message, email_from, [email])


def generate_random_code(length=4):
    characters = string.octdigits + string.digits
    return "".join(random.choice(characters) for _ in range(length))
