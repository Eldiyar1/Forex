import random

from django.core.mail import send_mail

from apps.users.models import User

code = random.randint(1000, 9999)
reset_password = random.randint(1000, 9999)


def send_email_confirmation(email):
    subject = "Подтверждение регистрации"
    message = (
        f"Здравствуйте! Ваш адрес электронной почты был указан для входа на приложение Zarina Пожалуйста, введите этот код на странице авторизации:/"
        f"{code}/"
        f" Если это не вы или вы не регистрировались на сайте, то просто проигнорируйте это письмо"
    )
    email_from = "ttestdb01@gmail.com"
    send_mail(subject, message, email_from, [email])
    user_obj = User.objects.get(email=email)
    user_obj.otp = code
    user_obj.save()


def send_email_reset_password(email, reset_password):
    subject = "Восстановление пароля"
    message = (
        f"Код для восстановления пароля: {reset_password} Код действителен в течении 5 минут"
    )
    email_from = "proverkageeks@gmail.com"
    send_mail(subject, message, email_from, [email])
