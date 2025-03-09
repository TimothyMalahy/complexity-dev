from django_htmx.http import (
    trigger_client_event,
    retarget,
    reswap,
    HttpResponseClientRedirect,
)
from django.shortcuts import render
from user_app.views import render_register_modal, render_login_modal

from django.urls import reverse
from .models import Topic, Subject, TopicOwner, Vote, Ranking
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
    "suggest-topic": {
        "template": "polls/modals/suggest-topic.html",
        "auth_required": False,
    },
    # Auth Required
    "new-topic": {"template": "polls/modals/new-topic.html", "auth_required": True},
    "edit-topic": {"template": "polls/modals/edit-topic.html", "auth_required": True},
    "new-subject": {"template": "polls/modals/new-subject.html", "auth_required": True},
}


def home(request: HtmxHttpRequest) -> HttpResponse:
    # authenticated users can see the new topic button, suggest topic button, and my topics
    # unauthenticated users can see the search bar, the public topics, and "find a random topic"
    context = {}
    context["public_topic_count"] = Topic.objects.filter(publicly_visible=True).count()
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
    user = request.user
    if user.is_anonymous:
        context["anonymous"] = True
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
    context = {}

    if not modal_config:
        return HttpResponse(status=404)

    if modal_config["auth_required"] and not request.user.is_authenticated:
        return render_login_modal(request)

    template = modal_config["template"]
    response = render(request, template, context)
    response = trigger_client_event(response, "openModal", after="swap")
    return response


def add_topic(request: HtmxHttpRequest) -> HttpResponse:
    if request.POST:
        topic = request.POST.get("topic")
        reference_link = request.POST.get("reference-link")
        print(request.POST)
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


def suggest_topic(request: HtmxHttpRequest) -> HttpResponse:
    if request.POST:
        # TODO: Email the topic to the owner of the site
        # TODO add a message to the user that their suggestion has been submitted
        response = HttpResponse("Suggestion submitted")
        response = trigger_client_event(response, "closeModal", after="swap")
        return response


def add_subject(request: HtmxHttpRequest) -> HttpResponse:
    if request.POST:
        topic = Topic.objects.get(id=request.POST.get("topic"))
        subject_text = request.POST.get("subject")
        details = request.POST.get("details")

        subject = Subject.objects.create(
            topic=topic, subject_text=subject_text, details=details, pub_date=timezone.now()
        )

        if "btn-save-return" in request.POST:
            url = reverse("polls:topic_detail", args=[topic.id])
            response = HttpResponse(
                f"""<a class="subject" href="{url}">{ subject.subject_text }</a>"""
            )
            response = reswap(response, "beforeend")

            response = retarget(response, "#subjects__grid")
            response = trigger_client_event(response, "closeModal", after="swap")

            return response


def load_subjects(request: HtmxHttpRequest) -> HttpResponse:
    user = request.user
    community_list = request.GET.get("is-community-list", None)

    context = {}
    if community_list or user.is_anonymous:  # Checkbox is true or user is anonymous
        context["topic"] = Topic.objects.get(id=request.GET.get("topic"))
        context["subjects"] = context["topic"].subject_set.all()
        context["subjects"] = sorted(context["subjects"], key=lambda subject: subject.total_score)
        context["ignore_tag"] = "ignore-elements"

        return render(request, "polls/partials/subjects.html", context)
    else:
        try:
            context["topic"] = Topic.objects.get(id=request.GET.get("topic"))
            context["latest_vote"] = Vote.objects.filter(user=user, topic=context["topic"]).latest(
                "date_updated"
            )
            rankings = Ranking.objects.filter(vote=context["latest_vote"]).order_by("order")

            voted_subject_ids = [ranking.subject.id for ranking in rankings]
            context["subjects"] = [ranking.subject for ranking in rankings]
            voted_subject_ids = [ranking.subject.id for ranking in rankings]

            context["unvoted_subjects"] = context["topic"].subject_set.exclude(
                id__in=voted_subject_ids
            )
            context["ignore_tag"] = ""
        except Vote.DoesNotExist:
            # If the user has not voted before then do the following to render
            context["topic"] = Topic.objects.get(id=request.GET.get("topic"))
            context["subjects"] = context["topic"].subject_set.all()
            context["unvoted_subjects"] = context["topic"].subject_set.all()

    return render(request, "polls/partials/subjects.html", context)
    context = {}
    context["topic"] = Topic.objects.get(id=request.GET.get("topic"))
    context["subjects"] = context["topic"].subject_set.all()
    return render(request, "polls/partials/subjects.html", context)


def submit_ballot(vote, request: HtmxHttpRequest) -> HttpResponse:
    # This serves as when they hit the official submit button, it will save the order of the subjects
    now = timezone.now()
    vote.submitted = True
    vote.date_updated = now
    vote.save()

    return HttpResponse("")


def sort_subjects(request: HtmxHttpRequest) -> HttpResponse:
    # This serves as the in process state before submission so they can come back.

    # Check that the items being sorted are underneath the correct topic
    # This is a check that someone didn't change an input value to move an item to a different topic
    user = request.user
    if request.POST:
        topic = request.POST.get("topic")
        subjects = request.POST.getlist("subject")

        topic = Topic.objects.get(id=topic)
        subjects_json = [
            {"order": count, "subject": subject} for count, subject in enumerate(subjects, start=1)
        ]

        try:
            # TODO put in a process to check if that latest vote on the topic is equal to the currently being submitted/saved vote
            vote = Vote.objects.create(user=user, topic=topic)
            Ranking.objects.bulk_create(
                [
                    Ranking(vote=vote, order=ranking["order"], subject_id=ranking["subject"])
                    for ranking in subjects_json
                ]
            )
            if request.htmx.trigger_name == "save-ballot-btn":
                response = HttpResponse("Ballot Saved but not submitted")
            if request.htmx.trigger_name == "submit-ballot-btn":
                vote = Vote.objects.filter(user=user, topic=topic, submitted=False).latest(
                    "date_updated"
                )
                response = submit_ballot(vote, request)
            response = retarget(response, "#ballot-status")
            return response
        except Exception as e:
            print(e)

    return HttpResponse("")
