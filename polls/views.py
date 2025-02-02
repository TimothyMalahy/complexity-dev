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


MODAL_CONFIG = {
    # Pattern
    # "element-id": {"template": "path/to/template.html", "auth_required": True/False},
    # Auth not required
    # Auth Required
    "new-topic": {"template": "polls/partials/new-topic-modal.html", "auth_required": True},
    "edit-topic": {"template": "polls/partials/edit-topic-modal.html", "auth_required": True},
    "new-subject": {"template": "polls/partials/new-subject-modal.html", "auth_required": True},
}


def home(request: HtmxHttpRequest) -> HttpResponse:
    context = {}
    context["topic_count"] = Topic.objects.count()
    return render(request, "polls/home.html", context=context)


def topics_search(request: HtmxHttpRequest) -> HttpResponse:
    context = {}
    context["topics"] = Topic.objects.filter(topic_text__icontains=request.POST.get("search"))

    return render(request, "polls/partials/topics-search.html", context)


def topic_detail(request, topic_id):
    """
    Topic detail view. A topic is the high level item. CSS/Javascript/Woodworking/Math

    Subject is the lower level item. CSS -> Flexbox, Grid, etc.
    Math --> Algebra, Geometry, etc.
    """
    context = {}
    context["subjects"] = Subject.objects.filter(topic=topic_id).prefetch_related(
        "subjectlinks_set"
    )
    try:
        context["topic_owner"] = TopicOwner.objects.get(topic=topic_id).user.email
    except TopicOwner.DoesNotExist:
        context["topic_owner"] = "Unknown"
    context["topic"] = Topic.objects.get(id=topic_id)
    # context['newer_subjects'] = Subject.objects.filter(topic=topic_id, subjectscore__score__lt=10)

    return render(request, "polls/topic-detail.html", context=context)


def random_topic_detail(request):
    """
    randomly gets an ID to a topic, then redirects to the topic_detail view.
    """

    topic = Topic.objects.order_by("?").first()
    return HttpResponseRedirect(reverse("polls:topic_detail", args=[topic.id]))


def render_modal(request: HtmxHttpRequest) -> HttpResponse:
    trigger = request.htmx.trigger
    modal_config = MODAL_CONFIG.get(trigger)

    if not modal_config:
        return HttpResponse(status=404)

    if modal_config["auth_required"] and not request.user.is_authenticated:
        return render(request, "partials/render-modal-auth-required.html")

    template = modal_config["template"]
    print(modal_config)
    print(template)
    context = {}
    return render(request, template, context)


def add_topic(request: HtmxHttpRequest) -> HttpResponse:
    if request.POST:
        topic = request.POST.get("topic")
        reference_link = request.POST.get("reference-link")
        user = request.user

        try:
            topic, _ = Topic.objects.get_or_create(
                topic_text=topic, pub_date=timezone.now(), reference_link=reference_link
            )
        except IntegrityError:
            response = HttpResponse("Topic already exists", status=400)
            response = retarget(response, "#topic-error")
            return response

        topic_owner = TopicOwner.objects.get_or_create(user=user, topic=topic)

        if "btn-save-return" in request.POST:
            url = reverse("polls:topic_detail", args=[topic.id])
            response = HttpResponse(f"""<a class="topic" href="{url}">{ topic.topic_text }</a>""")
            response = reswap(response, "beforeend")

            response = retarget(response, "#topics__grid")
            response = trigger_client_event(response, "closeModal", after="swap")

            return response
        elif "btn-save-open" in request.POST:
            response = HttpResponseClientRedirect(reverse("polls:topic_detail", args=[topic.id]))
            return response
