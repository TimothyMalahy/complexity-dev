from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from .models import CustomUser
from django.conf import settings

from post_office import mail
import json


from django_htmx.http import trigger_client_event, retarget, reswap, HttpResponseClientRedirect
from django_htmx.middleware import HtmxDetails
import random
import string


class HtmxHttpRequest(HttpRequest):
    htmx: HtmxDetails


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


def render_register_modal(request: HtmxHttpRequest) -> HttpResponse:
    def generate_random_email():
        domains = ["example.com", "test.com", "sample.org"]
        username = "".join(random.choices(string.ascii_lowercase + string.digits, k=10))
        domain = random.choice(domains)
        return f"{username}@{domain}"

    email = generate_random_email()
    request.POST = request.POST.copy()
    request.POST["email"] = email
    return render(request, "user_app/partials/register-modal.html", {"email": email})


def render_login_modal(request: HtmxHttpRequest) -> HttpResponse:
    context = {}
    random_user = CustomUser.objects.order_by("?").first()
    context["email"] = random_user.email
    context["password"] = "abcdefgh12"
    return render(request, "user_app/partials/login-modal.html", context=context)


def login_user(request: HtmxHttpRequest) -> HttpResponse:
    email = request.POST.get("email")
    password = request.POST.get("password")
    user = authenticate(request, email=email, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseClientRedirect("/")
    else:
        return HttpResponse("Invalid login credentials", status=401)
    pass


def register_user(request: HtmxHttpRequest) -> HttpResponse:
    response = HttpResponse("", status=200)
    errors = request.POST.get("errors")
    errors_response = []

    if errors:
        errors_dict = json.loads(errors)
        for key, value in errors_dict.items():
            if value:
                errors_response.append(value)
    if errors_response:
        errors_response.append("<strong>Please correct the errors above</strong>")
        response = HttpResponse("<br>".join(errors_response), status=200)
        response = retarget(response, "#form-errors")
        return response
    new_user = CustomUser.objects.create_user(
        email=request.POST.get("email"), password=request.POST.get("password")
    )
    new_user.first_name = request.POST.get("first-name")
    new_user.last_name = request.POST.get("last-name")
    new_user.save()

    response = trigger_client_event(response, "closeModal", after="receive")
    return response
