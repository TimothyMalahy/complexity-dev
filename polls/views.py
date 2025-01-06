from django_htmx.http import trigger_client_event
from django.shortcuts import render
from .models import Topic, Subject
from django.http import HttpResponse

# Create your views here.


def home(request):
    # return HttpResponse("Hello, world. You're at the home page.")
    context = {}
    context["topics"] = Topic.objects.all()
    return render(request, "polls/home.html", context=context)


def vote(request, topic_id):
    context = {}
    context["subjects"] = Subject.objects.filter(topic=topic_id).prefetch_related(
        "subjectlinks_set"
    )
    # context['newer_subjects'] = Subject.objects.filter(topic=topic_id, subjectscore__score__lt=10)

    return render(request, "polls/vote.html", context=context)


def render_modal(request):
    response = render(request, "polls/render_modal.html")
    return trigger_client_event(response, "modal:show", after="swap")
    # if request.method == "POST":
    #     return HttpResponse("")  # close modal
    # context = {}
    # return render(request, "polls/render_modal.html", context=context)
