from django_htmx.http import trigger_client_event, retarget, reswap, HttpResponseClientRedirect
from django.shortcuts import render

from django.urls import reverse
from .models import Topic, Subject, TopicOwner
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect

from django_htmx.middleware import HtmxDetails
from django.utils import timezone


from django.db import IntegrityError


# Create your views here.
class HtmxHttpRequest(HttpRequest):
    htmx: HtmxDetails


def validate_topic(request: HtmxHttpRequest) -> HttpResponse:
    topic = request.POST.get("topic")
    if not topic:
        response = HttpResponse("Topic is required", status=400)
        response = retarget(response, "#topic-error")
        return response

    if Topic.objects.filter(topic_text__iexact=topic).exists():
        response = HttpResponse("Topic already exists", status=400)
        response = retarget(response, "#topic-error")
        return response

    response = HttpResponse("", status=200)
    response = retarget(response, "#topic-error")
    return response
