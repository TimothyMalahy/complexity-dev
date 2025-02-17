from django.contrib.auth.password_validation import validate_password as django_validate_password
from django.core.exceptions import ValidationError

from django_htmx.http import trigger_client_event, retarget, reswap, HttpResponseClientRedirect
from django.shortcuts import render

from django.urls import reverse
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect

from django_htmx.middleware import HtmxDetails
from django.utils import timezone

from .models import CustomUser


from django.db import IntegrityError
import re


# Create your views here.
class HtmxHttpRequest(HttpRequest):
    htmx: HtmxDetails


def user_registration_email(request: HtmxHttpRequest) -> HttpResponse:
    print("USER REGISTRATION EMAIL")
    email = request.POST.get("email")
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if CustomUser.objects.filter(email=email).exists():  # If the email is already in use
        response = HttpResponse("Email is already in use", status=200)
        response = retarget(response, "#email-error")
        return response
    if not re.match(email_regex, email):  # If the email does not match the regex
        response = HttpResponse("Invalid email format", status=200)
    else:
        response = HttpResponse("", status=200)
    response = retarget(response, "#email-error")
    return response


def user_registration_pass(request: HtmxHttpRequest) -> HttpResponse:
    password = request.POST.get("password")
    confirm_password = request.POST.get("confirm-password")
    response = HttpResponse("", status=200)
    trigger_name = request.htmx.trigger_name
    errors = []
    if password == "":
        response = HttpResponse("", status=200)
        response = retarget(response, "#password-error")
        return response
    try:
        django_validate_password(password)
    except ValidationError as e:
        for error in e.messages:
            errors.append(error)

    if errors:
        response = HttpResponse("<br>".join(errors), status=200)
    if trigger_name == "password":
        response = retarget(response, "#password-error")
    if trigger_name == "confirm-password":
        if password != confirm_password:
            response = HttpResponse("Passwords do not match", status=200)
        else:
            response = HttpResponse("", status=200)
        response = retarget(response, "#confirm-password-error")
    return response


def validate_email(request: HtmxHttpRequest) -> HttpResponse:
    print("VALIDATE EMAIL")
    print(request.POST)
    trigger_name = request.htmx.trigger_name
    if "confirm-password" in request.POST:
        if CustomUser.objects.filter(email=request.POST.get("email")).exists():
            response = HttpResponse("Email is already in use", status=200)
        else:
            response = HttpResponse("Email is available", status=200)
        response = retarget(response, "#email-error")
        return response
    else:
        response = HttpResponse("Emails match", status=200)
    response = HttpResponse("", status=200)
    return response


def validate_password(request: HtmxHttpRequest) -> HttpResponse:
    print(request.POST)
    trigger_name = request.htmx.trigger_name
    if trigger_name == "confirm-password":
        response = HttpResponse("Passwords match", status=200)
    response = HttpResponse("", status=200)

    return response
