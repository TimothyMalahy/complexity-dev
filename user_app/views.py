from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import HttpResponse
from .models import CustomUser
from django.conf import settings

from post_office import mail


def send_test_email(request):
    mail.send(
        recipients=["timothymalahy@protonmail.com"],
        sender="donotreply@localhost.com",
        subject="sample",
        message=f"sample test",
        priority="now",
    )
    return HttpResponse("Email sent")


def send_verification_email(user):
    token = user.generate_verification_token()
    verification_link = f"{settings.SITE_URL}/verify/{token}"
    mail.send(
        recipients=user.email,
        sender=f"donotreply@{settings.SITE_URL}",
        subject="Verify your account",
        message=f"Click the link to verify your account: {verification_link}",
    )


def verify_user(request, token):
    try:
        user = CustomUser.objects.get(verification_token=token, token_expiration__gt=timezone.now())
        user.is_verified = True
        user.verification_token = None
        user.token_expiration = None
        user.save()
        return HttpResponse("Your account has been verified.")
    except CustomUser.DoesNotExist:
        return HttpResponse("Verification link is invalid or has expired.")
