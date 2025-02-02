from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Sum
from urllib.parse import urlparse
from user_app.models import CustomUser  # Import CustomUser

# Create your models here.


class Topic(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["topic_text"],
                name="unique_topic_text_lower",
                condition=models.Q(topic_text__iexact=models.F("topic_text")),
            )
        ]

    topic_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    reference_link = models.URLField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.topic_text


class Subject(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    subject_text = models.CharField(max_length=200)
    details = models.TextField(blank=True, null=True)
    pub_date = models.DateTimeField("date published", auto_now_add=True)

    def __str__(self):
        return self.subject_text

    def total_score(self):
        return self.subjectscore_set.aggregate(Sum("score"))["score__sum"] or 0

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
    date_voted = models.DateTimeField(auto_now_add=True)
    rankings = models.JSONField()

    def __str__(self):
        return f"Vote by {self.user} on {self.topic}"

    ## Always return the latest voted date for each user


class TopicOwner(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} owns {self.topic}"
