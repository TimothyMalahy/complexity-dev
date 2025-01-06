from django.shortcuts import render

# from django.http import HttpResponse
from polls.models import Topic
import random


# Create your views here.


def home(request):
    context = {}
    topics = list(Topic.objects.all())
    random.shuffle(topics)
    context["topics"] = topics[:25]
    context["total_extra"] = len(topics) - len(context["topics"])
    return render(request, "home/home.html", context=context)
