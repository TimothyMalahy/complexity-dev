# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Topic, Subject, SubjectScore, SubjectLinks, Vote
from guardian.admin import GuardedModelAdmin


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("id", "topic_text", "pub_date")
    list_filter = ("pub_date",)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("id", "topic", "subject_text", "details", "pub_date")
    list_filter = ("topic", "pub_date")


@admin.register(SubjectScore)
class SubjectScoreAdmin(admin.ModelAdmin):
    list_display = ("id", "subject", "score")
    list_filter = ("subject",)


@admin.register(SubjectLinks)
class SubjectLinksAdmin(GuardedModelAdmin):
    list_display = ("id", "subject", "link_text", "link_url", "pub_date")
    list_filter = ("subject", "pub_date")


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "topic", "rankings")
    list_filter = ("user", "topic")
