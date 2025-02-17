from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Sum
from urllib.parse import urlparse
from user_app.models import CustomUser  # Import CustomUser
from django.utils import timezone
from django.db.models import Q
from django.db.models import Sum, F
from django.db.models.functions import Cast
from django.db.models import FloatField
from django.db.models.fields.json import KT
from django.db.models.expressions import RawSQL
# Create your models here.


class Topic(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["topic_text", "owner"],
                name="unique_topic_text_owner",
                condition=models.Q(topic_text__iexact=models.F("topic_text")),
            )
        ]

    topic_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    reference_link = models.URLField(max_length=250, blank=True, null=True)
    publicly_visible = models.BooleanField(
        default=False, help_text="Should this topic be visible to all users?"
    )
    publicly_votable = models.BooleanField(
        default=False, help_text="Should this topic be votable by all users?"
    )
    public_new_subjects = models.BooleanField(
        default=False, help_text="Should this topic allow new subjects to be added by all users?"
    )
    owner = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="owner", blank=True, null=True
    )

    def __str__(self):
        if self.owner:
            return f"{self.owner}/{self.topic_text}"
        else:
            return f"ComplexityIndex/{self.topic_text}"
        return self.topic_text

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not TopicGroup.objects.filter(topic=self).exists():
            if not self.publicly_visible:
                reader_group = TopicGroup.objects.create(
                    topic=self, name="Reader", description="Readers of the topic"
                )
            if not self.publicly_votable:
                voting_group = TopicGroup.objects.create(
                    topic=self, name="Voting", description="Voters of the topic"
                )
            if not self.public_new_subjects:
                new_subjects_creators_group = TopicGroup.objects.create(
                    topic=self,
                    name="New Subject Creators",
                    description="Users who can create new subjects",
                    can_create_subjects=True,
                )
                new_subjects_suggestors_group = TopicGroup.objects.create(
                    topic=self,
                    name="New Subject Suggestors",
                    description="Users who can suggest new subjects",
                    can_suggest_subjects=True,
                )
                admin_group = TopicGroup.objects.create(
                    topic=self, name="Admin", description="Administrators of the topic"
                )


class TopicGroup(models.Model):
    """This is a group of users that have permissions to do certain things in a topic.

    Args:
        models (_type_): _description_
    """

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    owners = models.ManyToManyField(CustomUser, related_name="group_owners")
    members = models.ManyToManyField(CustomUser, related_name="group_members")
    # Group Management
    can_create_group = models.BooleanField(
        default=False, help_text="Can create groups for the topic."
    )
    can_update_group = models.BooleanField(
        default=False, help_text="Can update groups for the topic."
    )
    can_add_users_to_group = models.BooleanField(
        default=False, help_text="Can add users to groups."
    )
    can_set_group_permissions = models.BooleanField(
        default=False, help_text="Can set permissions for groups."
    )

    # Topic Management
    can_rename_topic = models.BooleanField(default=False, help_text="Can rename the topic.")
    can_delete_topic = models.BooleanField(default=False, help_text="Can delete the topic.")
    can_update_topic_visible = models.BooleanField(
        default=False, help_text="Can update the topic visibility from public to private."
    )
    can_update_topic_votable = models.BooleanField(
        default=False, help_text="Can update the topic to be votable."
    )
    can_update_topic_subject_rules = models.BooleanField(
        default=False, help_text="Can update the rules for subjects in the topic."
    )

    # Subject Management
    can_create_subjects = models.BooleanField(
        default=False, help_text="Can create subjects in the topic."
    )
    can_suggest_subjects = models.BooleanField(
        default=False, help_text="Can suggest subjects in the topic."
    )
    can_delete_subjects = models.BooleanField(
        default=False, help_text="Can delete subjects in the topic."
    )
    can_vote_on_subjects = models.BooleanField(
        default=False, help_text="Can vote on subjects in the topic."
    )


class Subject(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    subject_text = models.CharField(max_length=200)
    details = models.TextField(blank=True, null=True)
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    current_score = models.IntegerField(
        default=0, help_text="This is regularly updated based on submitted votes."
    )

    def __str__(self):
        return self.subject_text

    @property
    def total_score(self):
        users_voted = (
            Vote.objects.filter(topic=self.topic, submitted=True, date_voted__isnull=False)
            .values_list("user", flat=True)
            .distinct()
        )  # Get all the IDs of the users that voted AND submitted on this topic
        votes_to_count = Vote.objects.filter(
            user__in=users_voted,
            topic=self.topic,
            date_voted__isnull=False,
            submitted=True,
        )
        latest_votes = (
            votes_to_count.order_by("user", "-date_voted")
            .distinct("user")
            .values_list("id", flat=True)
        )
        rankings = Ranking.objects.filter(vote__in=latest_votes, subject=self)
        total = rankings.aggregate(Sum("order"))["order__sum"] or 0

        return total

        # return self.subjectscore_set.aggregate(Sum("score"))["score__sum"] or 0

    # I can do the scoring for new topics with a star that says "These are in less than 10% of votes because its a new topic."
    # I can also then let them filter for a time range of votes to see how the scores have changed over time or ensure they're included in the options


class SubjectScore(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.score


class SubjectLinks(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    link_text = models.CharField(max_length=200)
    link_url = models.URLField(max_length=200)
    pub_date = models.DateTimeField("date published", auto_now_add=True)

    def __str__(self):
        return self.link_text

    def save(self, *args, **kwargs):
        if self.subject.subjectlinks_set.count() >= 3:
            raise ValidationError("A subject can have at most 3 links.")
        super().save(*args, **kwargs)

    def get_source_domain(self):
        domain = urlparse(self.link_url).netloc
        return domain


class Vote(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    submitted = models.BooleanField(default=False)
    date_voted = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Date the vote was submitted - null if they didn't submit from last change",
    )
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Vote by {self.user} on {self.topic} on {self.date_updated}"

    def save(self, *args, **kwargs):
        if self.submitted and not self.date_voted:
            self.date_voted = timezone.now()
        super().save(*args, **kwargs)

    ## Always return the latest voted date for each user


class Ranking(models.Model):
    vote = models.ForeignKey(Vote, on_delete=models.CASCADE)
    order = models.IntegerField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["vote", "order"], name="unique_vote_order"),
            # TODO make a constraint so that the order can never be higher than the number of subjects in a given topic
        ]

    def __str__(self):
        return f"Ranking {self.order} for subject {self.subject}"


class TopicOwner(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} owns {self.topic}"
